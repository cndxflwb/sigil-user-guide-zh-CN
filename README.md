# <center>本仓库是 Sigil 用户指南的源代码仓库</center>

<br/>

[在线阅读本用户指南](https://sigil-ebook.com/sigil-user-guide)

<br/>

## <center>贡献指南</center>

<br/>

1. __请勿进行美术/审美方面的改动！__ 我们只接受内容更新与勘误，或者展示新菜单、新功能的截图更新。如果你想"把它做得更花哨"，或者按照个人风格、排版偏好重做这本 epub 的样式，那你多半要失望了。包含样式改动或"升级"的 Pull Request 会被拒绝（当然，事先获得批准的工作除外）。

2. __少即是好__。若干个小而聚焦的 Pull Request，永远比那种对整个手册大范围"大刀阔斧"改动的 PR 更受欢迎。我们不想在每次评审新的 Pull Request 时都要把整本手册读一遍，换作是你也一样。如果你希望自己的贡献被采纳，请多为他人着想。

3. __不要破坏任何东西__。导致生成的 epub 损坏或引发校验问题的改动会被拒绝。确保 epub 结构完整且符合规范，是你自己的责任。

<br/>
<br/>

## <center>推荐的工作流程</center>

<br/>

- 将本仓库 Fork 到你自己的 GitHub 账号，并克隆一份本地副本到你的电脑上。

- 使用 [FolderIn Sigil 插件](https://www.mobileread.com/forums/showthread.php?t=293649)，将本地已克隆仓库中 "src" 目录的内容载入 Sigil。

- 开始编辑（如有需要，可把改动先保存到本地某个临时 epub 中）。完成后记得执行"Mend and Prettify（整理并美化）"，并始终确保 epub 校验无错误。准备就绪后，使用 [FolderOut Sigil 插件](https://www.mobileread.com/forums/showthread.php?t=293649)把内容保存回本地已克隆仓库的 "src" 目录。

- 使用常规的 git 工具检查你的差异，确认无误后提交并推送到你 Fork 的 GitHub 仓库。

- 从你的 GitHub 账号发起一个新的 Pull Request，以便我们评审并（希望如此）将你的改动合并进本项目。

<br/>

----

<br/>

如果遇到问题，欢迎到 [Mobileread 上的 Sigil 支持论坛](https://www.mobileread.com/forums/forumdisplay.php?f=203)寻求帮助。
