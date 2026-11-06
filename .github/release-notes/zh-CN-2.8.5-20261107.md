Sigil 用户指南中文版第二个发布版本，内容同步至官方 Sigil User Guide 2026.11.01。

- 基线：官方 Sigil User Guide 2026.11.01（适用 Sigil 2.8.5 及更高版本）
- 全书正文与界面文案中文化，元数据：书名《Sigil 用户指南》、语言 zh-CN
- 已用 EPUBCheck 5.4.0 校验：未报告错误或警告（EPUB 3）
- 源码：https://github.com/cndxflwb/sigil-user-guide-zh-CN （分支 zh-CN）
- 与上版对比：https://github.com/cndxflwb/sigil-user-guide-zh-CN/compare/zh-CN-2.6.2-20250927...zh-CN-2.8.5-20261106

### 相对 2.6.2 版的主要更新

**版本与安装**
- 全书目标版本更新为 Sigil 2.8.5，版权年份更新至 2026
- Linux 安装方式改写：改用 AppImage，与 Windows/macOS 版本功能对齐（含插件支持）
- macOS 最低版本由 11 提高到 13

**新功能**
- 图像标签页内置简单编辑：保存、缩放、撤销/重做、左右旋转、裁剪、调整尺寸
- 支持用 special_characters.xml 自定义“插入特殊字符”对话框，新增“高级用户”一节
- 新增拖放区（Drop Zone），可直接把文件拖进 EPUB
- 自动化列表改由“自动化=>管理自动化列表”统一管理，支持任意数量列表，并可从“运行”菜单直接执行

**界面与工具**
- 新增“重新开始当前搜索”“使用标准文件扩展名”
- 新增三条 NAV 阅读顺序工具（移除 / 加入 / 以 `linear="no"` 加入）
- 生成 NCX/Guide 时同时补写 EPUB2 封面元数据，移除时一并清除
- 工具栏新增“自动化列表”，主菜单新增“自动化”
- 状态栏新增光标处字符说明与拖放区
- 环境变量新增 SIGIL_ONLY_USE_LANGCODES
- 首选项目录新增 prettyprint.xml、replace_funtions.json、special_characters.xml 条目

**文档修正**
- 正则教程示例改为 `\s*CHAPTER\s+(\d+)\s*`，补充 `*` 与 `+` 的说明
- 正则参考表中 `\s` 条目移入字符类一节
- 更新 7 张界面截图，新增“管理自动化列表”对话框截图，移除已被替代的旧截图
- 下载提示中补充中文版仓库地址

### 说明
上游英文版个别表述存在笔误（如自动化列表文件名说明前后不一致、“重新开始当前搜索”句子不完整），中文版按语义处理，未机械照搬。
