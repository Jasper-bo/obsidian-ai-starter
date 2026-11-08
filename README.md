# Obsidian AI Starter

先了解你想怎样使用知识库，再帮你搭建它。

这是一个可导入 **WorkBuddy** 的 Agent Skill：通过对话了解用户的身份、实际任务、资料和组织偏好，设计相应的 Obsidian 知识库，再完成安装引导、建库、资料入库与带来源的 AI 问答。也提供标准 `SKILL.md` 源目录，便于其他支持 Agent Skills 的宿主使用。

## 在 WorkBuddy 使用

**当前版本：1.1.0**

直接把这个 GitHub 链接发给 WorkBuddy：

**https://github.com/Jasper-bo/obsidian-ai-starter**

可以连同下面的话一起发送：

> 请读取这个 GitHub 项目中的 `skills/obsidian-ai-starter/SKILL.md`，获取同目录的完整参考资料和脚本，将这个 skill 安装到我当前项目的 `.codebuddy/skills/obsidian-ai-starter/`。确认技能可用后，先了解我的需求，设计适合我的知识库，再帮我搭建。

- [Skill 入口](skills/obsidian-ai-starter/SKILL.md)
- [完整 Skill 目录](skills/obsidian-ai-starter)

WorkBuddy 按项目配置读取 `.codebuddy/skills/` 中的技能，每款技能是包含 `SKILL.md` 的独立目录。获取时保留 `references/` 和 `scripts/`，不要只复制入口文字。安装后检查技能列表，随后在对话中使用。

Obsidian 应用本身从 [官方下载页](https://obsidian.md/download) 获取；skill 会先检查你的系统与已有安装，带你按实际情况继续。

官方说明：[项目级技能目录](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project)、[技能入口](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。

## 如何定制知识库

Skill 会先了解：

1. 你主要做什么，最希望知识库帮你完成哪件事。
2. 现在有哪些资料、已有怎样的分类。
3. 你喜欢按主题、项目、工作流程组织，还是少分类直接搜索。
4. 你愿意怎样维护，日常从哪里进入。

已知信息会直接沿用，每轮围绕一个问题补充。需求明确后给出文本目录树、每个区域的用途，以及一份真实资料怎样进入、被找到和复用的例子。已有知识库优先保留，迁移旧文件另行决定。

例如同样是自媒体用户：

- 经常读文章、积累观点，希望极简：可以采用 `首页 / 主题资料 / 我的想法 / 内容草稿 / 系统`。
- 经常围绕一条内容组织制作：可以按需要增加选题、内容项目与复用素材，项目里连接脚本、资料和制作记录。
- 未提出排期、商业化或复盘需求时，不提前创建这些模块。

学生、研究阅读者、工作项目用户同样按实际任务设计；这些示例不是必须套用的模板。具体引导见 [知识库设计参考](skills/obsidian-ai-starter/references/knowledge-design.md)。

## 从设计到可用

```text
了解用途与偏好 → 展示适配结构 → 检查/安装 Obsidian
      → 按方案建库 → 导入真实资料 → 检索并给出引用 → 验收和交接
```

个性化结构通过宿主文件工具创建，不要求安装 Python。包内 Python 工具只使用标准库：

- `init`：用户选择通用资料整理布局时，预览并补充缺失文件，保留已有内容。
- `doctor`：检查上述固定通用布局，不用于强制约束个性化目录。
- `search`：在不同目录结构的 Markdown 中做关键词检索，返回文件、行号和上下文；个性化系统/模板目录由 Agent 另行过滤。

问答必须读取原文、保留引用；无依据时明确资料不足。关键词检索不是向量 RAG。需要语义关联、库内聊天或独立文档问答时，再按 [AI 路线参考](skills/obsidian-ai-starter/references/ai-routes.md) 选择适当的扩展。

## 验证状态与边界

- 已通过官方 Skill 格式校验、5项脚本行为测试和资源检查。
- 独立 Agent 已试用：信息不足时先提问；需求充分时建立个性化主题库，完成来源查询、无答案处理与增量更新测试。
- WorkBuddy 实机安装识别、Obsidian 界面、可选 AI 插件及 Windows 实机尚未验证；不能把文件已生成当作这些环节全部成功。
- Obsidian 应用本体不是开源软件；本项目是独立的开源 Skill，与 Obsidian、WorkBuddy 无官方隶属关系。参考 [Obsidian 官方发布说明](https://github.com/obsidianmd/obsidian-releases)。
- 文件在本地不代表 AI 推理在本地。云模型可能收到读取的资料片段；完全离线需要单独配置并验证本地模型。软件、模型、付费服务和系统安装权限需要按实际环境配置。

## 开发与检查

运行时脚本不需要 pip 或第三方 Python 库：

```bash
python3 -m unittest discover -s tests -v
```

原脚本的测试覆盖 dry-run、不覆盖已有笔记、中文路径与检索、增量更新、符号链接边界及编码错误。

## 来源与许可

本项目原创实现，按 MIT 许可发布，见 [LICENSE](LICENSE)。调研参考包括 [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)、[AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) 与各软件的官方文档；没有捆绑上游插件、模型或软件。上游软件分别适用各自许可。
