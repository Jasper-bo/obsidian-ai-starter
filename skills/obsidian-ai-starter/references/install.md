# 安装 Obsidian（核查日期 2026-11-08）

## 官方安装路线

权威入口：[官方下载](https://obsidian.md/download)、[安装文档](https://help.obsidian.md/install)。先核对当前系统/CPU对应的安装包，不固定版本号。安装前检查已装应用，避免重复装第二份。

### Windows

优先已有 `winget`：先 `winget show --id Obsidian.Obsidian --exact --source winget`，确认显示 Obsidian 及安装来源，再执行 `winget install --id Obsidian.Obsidian --exact --source winget`。包标识参考 [Microsoft manifests](https://github.com/microsoft/winget-pkgs/tree/master/manifests/o/Obsidian/Obsidian)。这不表示微软为应用背书。

没有 winget 或企业政策阻止包管理器时，用官方下载 Windows 安装器。让系统显示正常的 UAC/签名提示；不要为安装修改执行策略、关闭杀毒或签名验证。安装完成，从开始菜单打开并检查首页。用户路径用实际账户路径，不把 `%USERPROFILE%` 写进 PowerShell 当已展开路径。

### macOS

已有 Homebrew 时用 `brew info --cask obsidian` 核对，再执行 `brew install --cask obsidian`，参考 [Homebrew cask](https://formulae.brew.sh/cask/obsidian)。不要仅为本任务给零基础用户额外装 Homebrew。

没有 Homebrew 时按官方下载 DMG，拖入 Applications 并打开。遇到系统拦截按 Apple 正常授权界面处理，不运行 `xattr` 清除隔离属性。可用 `open -a Obsidian` 启动，但需要界面证据才能确认首页可用。

### Linux（补充）

先检查当前 Agent 是否能访问目标 Linux 机器；Obsidian 的 AppImage/发行版安装分支见官方安装页。不要将 Windows/macOS 测试结论推广为 Linux 实测。

## 可选 CLI

[Obsidian CLI 官方说明](https://help.obsidian.md/cli) 以运行时为准。需支持 CLI 的较新桌面安装器，在设置 → 通用 → Command line interface 中启用/注册。先 `obsidian help` 检查，不假设安装应用就有 PATH 命令。不满足时直接读写 Vault Markdown，基础建库不依赖 CLI。

## Python 与权限

先试 `python3 --version`、`python --version` 或 Windows 的 `py -3 --version`，任选确实可用者。脚本只用 Python 标准库，无需 pip。都没有时走 `manual-vault.md`，不必因脚本补装开发环境。

脚本与安装操作受当前 Agent 的工具权限、运行环境和操作系统规则约束，使用当前任务所需权限。无法执行终端或操作安装器时，给出对应官方页面与具体手动步骤；手机、浏览器或远程会话若不能访问目标桌面，交付明确的桌面续接步骤，不声称已经装软件。
