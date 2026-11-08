# AI 路线选择

核查日期：2026-11-08。执行时先检查当前 README/安装文档；版本、套餐和插件入口可能变化。只安装用户选定的一条进阶路线。

| 需求 | 路线 | 主要成本与数据边界 |
| --- | --- | --- |
| 先用起来，不另接服务 | 本地 Markdown + WorkBuddy 检索 | 本包默认；资料片段可能发送到宿主云模型，关键词检索不是语义 RAG |
| 独立桌面文档问答 | AnythingLLM Desktop | MIT；需配置 LLM、embedding、向量库；分别检查本地/云位置 |
| 在 Obsidian 里调用 Agent | Copilot | AGPL-3.0；当前 V4 Agent Chat 架构，按新文档配置，不能照搬旧版 Vault QA |
| 写作时找相似笔记 | Smart Connections | 本地 embedding 的语义关联；当前 source-available 自定义许可证，聊天已拆分 |
| 自托管服务及多端接入 | Khoj | AGPL-3.0；涉及服务、模型及索引，放在进阶阶段 |
| 编辑器也必须开源 | Logseq 等 + 明确的数据导出方案 | 改用实际版本的存储/导出格式；不能把本包的 Vault 双链布局直接当作 Logseq 原生模型 |

## AnythingLLM Desktop：首次文档问答

1. 查看 [桌面安装入口](https://docs.anythingllm.com/installation-desktop/overview) 的系统要求，下载对应桌面版。安装是否成功以能打开设置和工作区为准。
2. 按机器内存和下载条件选模型。配置 LLM、embedding 与向量数据库；完全本地要求三者都是本地，关闭所选流程的联网检索/云工具。首次下载模型需要联网；模型是否适配当前硬件以实际小样测试为准。
3. 新建测试 workspace；按当前界面上传 1–3 篇脱敏 Markdown，再执行界面中的加入工作区/保存与嵌入操作。只有上传而未嵌入不能算已可检索。可从 [文档中心](https://docs.anythingllm.com/) 找当前 uploading/embedding 指南，不编造过期按钮名。
4. 选择依赖工作区资料的问答模式，执行 `acceptance.md` 中的有答案/无答案/跨篇测试，并打开引用片段核对来源。
5. 修改一篇来源后，手动替换对应资料并重新嵌入，验证新答案；记录 Vault 来源文件与工作区文档对应关系，避免重复导入旧版本。

官方 [自动同步说明](https://docs.anythingllm.com/beta-preview/active-features/live-document-sync) 仍列 beta，不能监视整个目录。基础路径不承诺整个 Vault 实时同步。不把云托管版与本地桌面版混为一谈。仓库：[Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)。

## Obsidian 插件

按 [官方社区插件流程](https://help.obsidian.md/community-plugins) 到设置 → 第三方插件，检索确切插件名，核对作者与仓库后安装并启用。只为当前用户选定的插件关闭相应限制；不下载不明转载包，不向导入 ZIP 内捆绑插件二进制。

- [Copilot 仓库](https://github.com/logancyang/obsidian-copilot)：先读当前 V4 README 与 [settings](https://github.com/logancyang/obsidian-copilot/blob/master/docs/settings.md)，核实 Agent、模型配置和费用。云模型会接收相关内容。密钥使用应用密钥设置或用户秘密存储，不写进笔记/共享 skill。
- [Smart Connections](https://github.com/brianpetro/obsidian-smart-connections)：先完成本地 embedding 并用相似笔记检索验收。Smart Chat 是另外的插件，其高级模型集成与价格要单独核对；不能将本插件描述为默认免费聊天工具。[许可证](https://github.com/brianpetro/obsidian-smart-connections/blob/main/LICENSE) 存在竞争用途限制，不能标为 MIT 或无条件开源。
- [Khoj](https://github.com/khoj-ai/khoj)：用户已明确选择自托管时，按当前 Docker/pip 官方路线进行小库导入测试，记录服务地址、存储位置、模型来源及重启方式；不默认向公网开放服务。

## 完全离线或全开源的分支

这是两个独立要求。Obsidian 本体 [不是开源软件](https://github.com/obsidianmd/obsidian-releases)，但 [默认本地存储 Markdown](https://help.obsidian.md/Files+and+folders/How+Obsidian+stores+data)。免费使用也不等于开源。

用户要求全开源时，说明 [Logseq](https://github.com/logseq/logseq) 与 AnythingLLM 的用途差异，让用户选知识编辑器或文档问答为主，再查该版本存储与导出规则。用户只要求离线时，可保留 Obsidian，选择本地模型路线。在本地工具里断网测试检索问答；当前 WorkBuddy 云会话不参与私密正文推理。尚未通过断网与网络配置核查时，只能交接“本地模型待验证”。
