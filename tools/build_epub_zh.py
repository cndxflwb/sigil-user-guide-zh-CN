#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 src/ 目录打包为《Sigil 用户指南》中文版 epub。

与官方 .github/workflows/build_guide.py 的构建逻辑一致（mimetype 以 ZIP_STORED
存储并置于包内首个条目，其余文件 deflate），唯一区别是：

    zip 条目名统一规范化为正斜杠 "/"

官方脚本用 os.path.join 生成归档名，在 Windows 上会写出反斜杠条目名
（形如 OEBPS\\Text\\introduction.xhtml），不符合 OCF 规范，产物实际无效；
官方 CI 跑在 ubuntu-latest 上，所以该问题一直未暴露。

用法（参数请只使用 ASCII 字符，中文一律硬编码在脚本内）：

    python tools/build_epub_zh.py                       # 构建 + 结构自检
    python tools/build_epub_zh.py --date 20250927        # 指定文件名里的日期
    python tools/build_epub_zh.py --version "2.6.2+"     # 指定文件名里的版本
    python tools/build_epub_zh.py --out out.epub         # 自定义输出路径
    python tools/build_epub_zh.py --check-only           # 只对已有产物做自检

默认输出到仓库根目录：Sigil 用户指南中文版（<version> <date>）.epub
（与官方一致，产物不入库：.gitignore 已忽略 *.epub，只作为 Release 附件分发）
"""

import argparse
import datetime
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
SKIP_BASENAMES = {"encryption.xml", "rights.xml", ".gitignore", ".gitattributes"}
NAME_TEMPLATE = "Sigil 用户指南中文版（{version} {date}）.epub"
DEFAULT_VERSION = "2.6.2+"

CONTAINER_NS = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
OPF_NS = {"o": "http://www.idpf.org/2007/opf"}


def collect_source_files(src_dir):
    """列出待打包文件，归档名一律使用 "/" 分隔。"""
    rv = []
    for base, dirs, names in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in names:
            if name in SKIP_BASENAMES:
                continue
            rel = os.path.relpath(os.path.join(base, name), src_dir)
            rel = rel.replace(os.sep, "/").replace("\\", "/")
            if rel == "mimetype":
                continue
            rv.append(rel)
    return sorted(rv)


def build_epub(src_dir, epub_path):
    """按 EPUB 2/3 通用规则打包，返回写入的文件数（不含 mimetype）。"""
    mimetype = os.path.join(src_dir, "mimetype")
    if not os.path.isfile(mimetype):
        raise SystemExit("构建失败：%s 下缺少 mimetype 文件" % src_dir)

    files = collect_source_files(src_dir)
    out_dir = os.path.dirname(os.path.abspath(epub_path))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    with zipfile.ZipFile(epub_path, "w") as z:
        z.write(mimetype, "mimetype", zipfile.ZIP_STORED)
        for rel in files:
            z.write(os.path.join(src_dir, *rel.split("/")), rel, zipfile.ZIP_DEFLATED)
    return len(files)


def check_epub(epub_path):
    """结构自检，返回问题列表（空列表表示通过）。"""
    problems = []
    with zipfile.ZipFile(epub_path) as z:
        infos = z.infolist()
        names = z.namelist()
        if not names:
            return ["包内没有任何条目"]
        if names[0] != "mimetype":
            problems.append("mimetype 不是首个条目（首个为 %s）" % names[0])
        if infos[0].compress_type != zipfile.ZIP_STORED:
            problems.append("mimetype 未以 ZIP_STORED 存储")
        if z.read("mimetype") != b"application/epub+zip":
            problems.append("mimetype 内容不是 application/epub+zip")
        bad_crc = z.testzip()
        if bad_crc:
            problems.append("CRC 校验失败：%s" % bad_crc)
        bad_sep = [n for n in names if "\\" in n]
        if bad_sep:
            problems.append("条目名含反斜杠（不符合 OCF）：%s" % bad_sep[:3])
        if len(names) != len(set(names)):
            problems.append("存在重复条目名")

        if "META-INF/container.xml" not in names:
            problems.append("缺少 META-INF/container.xml")
            return problems
        root = ET.fromstring(z.read("META-INF/container.xml"))
        rootfile = root.find(".//c:rootfile", CONTAINER_NS)
        opf_path = rootfile.get("full-path") if rootfile is not None else None
        print("rootfile: %s" % opf_path)
        if opf_path not in names:
            problems.append("rootfile 不在包内：%s" % opf_path)
            return problems

        opf_dir = os.path.dirname(opf_path)
        opf = ET.fromstring(z.read(opf_path))
        manifest = {}
        for item in opf.findall(".//o:manifest/o:item", OPF_NS):
            href = item.get("href")
            manifest[item.get("id")] = (opf_dir + "/" + href) if opf_dir else href

        missing = sorted(h for h in manifest.values() if h not in names)
        if missing:
            problems.append(
                "清单中 %d 个文件在包内缺失，例如：%s" % (len(missing), missing[:5])
            )

        spine_ids = [i.get("idref") for i in opf.findall(".//o:spine/o:itemref", OPF_NS)]
        bad_spine = [i for i in spine_ids if i not in manifest]
        if bad_spine:
            problems.append("spine 引用了不存在的 id：%s" % bad_spine[:5])

        cover = None
        for meta in opf.findall(".//o:metadata/o:meta", OPF_NS):
            if meta.get("name") == "cover":
                cover = meta.get("content")
        if cover:
            if cover not in manifest:
                problems.append("cover 元数据指向的 id 不在清单中：%s" % cover)
            elif manifest[cover] not in names:
                problems.append("封面文件不在包内：%s" % manifest[cover])
            else:
                print("cover   : %s -> %s (OK)" % (cover, manifest[cover]))
        else:
            print("cover   : 未声明")

        print("entries : %d" % len(names))
        print("spine   : %d 项" % len(spine_ids))
    return problems


def default_out_path(version, date):
    return os.path.join(REPO_ROOT, NAME_TEMPLATE.format(version=version, date=date))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="打包《Sigil 用户指南》中文版 epub（参数请只用 ASCII 字符）"
    )
    parser.add_argument("--src", default=SRC_DIR, help="源码目录，默认 <repo>/src")
    parser.add_argument("--out", default=None, help="输出 epub 路径")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="文件名中的适用版本")
    parser.add_argument(
        "--date",
        default=datetime.date.today().strftime("%Y%m%d"),
        help="文件名中的日期，默认今天（YYYYMMDD）",
    )
    parser.add_argument("--check-only", action="store_true", help="只自检已有产物，不重新构建")
    args = parser.parse_args(argv)

    epub_path = args.out or default_out_path(args.version, args.date)

    if not args.check_only:
        count = build_epub(args.src, epub_path)
        print("built   : %s" % epub_path)
        print("size    : %.2f MB" % (os.path.getsize(epub_path) / 1048576.0))
        print("src 文件: %d (+mimetype)" % count)
    elif not os.path.isfile(epub_path):
        raise SystemExit("自检失败：文件不存在 %s" % epub_path)

    print("\n---- verify ----")
    problems = check_epub(epub_path)
    if problems:
        print("\nFAILED:")
        for p in problems:
            print("  - %s" % p)
    print("\nRESULT  : %s" % ("PASS" if not problems else "FAIL"))
    print("提示：结构自检不替代规范的 EPUBCheck 校验，发布前建议另行运行 epubcheck。")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
