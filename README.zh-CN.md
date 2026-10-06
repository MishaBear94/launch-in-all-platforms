# launch-in-all-platforms（中文说明）

让 AI agent 帮你把产品发布到几十个 launch 平台和创业目录站，人工只做极少的几步；发布完之后，统一收集所有产品页链接，并持续维护 upvote。

来自一次真实发布：一个 SaaS 产品两天内提交了约 70 个平台。创始人每批只花几分钟，做 agent 不能代做的事（Google 授权登录、人机验证、给别的产品点赞）。这次的经验都整理成了数据、模板、脚本和 agent skill。

## 六个问题，对应的位置

| 问题 | 看这里 |
|---|---|
| 可以在哪些平台 launch（免费 / 收费、免费档要求、排队时长、能不能投票） | `data/platforms.yaml` → `docs/platforms.md`（89 个平台，57 个有免费档） |
| 创始人要提前准备哪些物料和基础信息（结构化 / 非结构化） | `templates/product.yaml`（结构化，脚本可校验）、`templates/founder-notes.md`（非结构化）、`docs/intake.md`；用 `scripts/check_intake.py` 做发布前闸门检查 |
| 怎么让 agent 高效地操作 | `docs/playbook.md`（流程与效率规则）、`skills/launch-in-all-platforms/SKILL.md`、`docs/platform-families.md`（同一套建站模板 = 同一套流程）、`docs/agent-gotchas.md`、`scripts/agent/` |
| 官网要加徽章，怎么高效做 | `docs/badges.md`；`scripts/badges.py render` 把所有徽章一次生成组件，一批只部署一次；`verify` 按平台爬虫的方式检查线上页面 |
| 经典回复模板 | `templates/replies.md`（24 个：给别人留言、自己产品页回复、拉票话术） |
| 发布完怎么批量收集链接、维护 upvote | `docs/upvotes.md`；台账 `templates/listings.yaml`；`scripts/check_listings.py` 批量检查是否上线 / 票数；`scripts/upvote_kit.py` 生成"现在可投 / 发布日开放"的链接页、发布日日历（.ics）和分享文案 |

完整示例：`examples/dailyhook/`（问卷、素材、57 个平台的台账）。

## 人和 agent 的分工

- **创始人只做：** 一次性回答问卷；每批 5–7 个平台时选 Google 账号授权；偶尔的人机验证；部分平台免费档要求的"先给别人点赞 / 评论"；发邮件；付费。
- **agent 做其余全部：** 找平台、写各种长度的文案、填表（优先用平台的 AI 自动填写再纠错）、选免费档和最近日期、收集徽章、改官网、部署、验证、记台账、上线后跟踪票数。

## 原则

- 只用免费档、只写真实信息（AI 自动填写常编造"每天早上更新""每天 10 条"之类，要按自己的文案纠正）。
- 不刷票、不互刷、不用小号：在发布日找真实用户，用直达链接。
- 平台规则每周都在变，`data/platforms.yaml` 记录"什么时候看到的什么"，欢迎 PR 更新。
