# Launch 平台之间的流量与链接关系：洞察报告

_2026 年 10 月 · 基于 105 个 launch 平台 / 创业目录站的首页链接抓取，以及一次真实产品在约 70 个平台的发布经历_

English version with diagram: [docs/ecosystem.md](../docs/ecosystem.md) · 原始数据：[data/link-graph.json](../data/link-graph.json)

---

## 一句话结论

**主流 launch 平台分成两个几乎不互通的世界**：少数头部平台有真实受众但彼此孤立；约 80 个长尾平台之间大量互链，构成一张"反向链接交换网"，它们交换的主要是 SEO 权重，而不是真实访客。

## 研究方法与局限

- **测的是链接关系，不是访客流量。** 以未登录访客身份打开 105 个平台首页，记录指向其他平台的所有链接（徽章、页脚、合作伙伴、"Featured on" 区块、资源推荐），共 980 条。
- **没有用 Similarweb、Ahrefs 等付费工具**，因此无法给出真实的引荐流量规模和来源占比。
- 文中的流量数字均来自平台**首页上的自我宣称**，未经核实。
- 小平台变化很快（本次发布中就有两个平台的产品页在几周内变成 404），本报告是 2026 年 10 月的快照。

---

## 洞察 1：头部平台是孤岛

| 头部平台 | 被长尾平台链接的数量 | 链向长尾平台的数量 |
|---|---|---|
| Product Hunt | 8 | 0 |
| Uneed | 1 | 0 |
| Peerlist | 1 | 0 |
| BetaList | 0 | 0 |
| Indie Hackers | 0 | 0 |
| There's An AI For That | 0 | 0 |
| DevHunt | 0 | 0 |
| Hacker News、Futurepedia | 抓取被拒，未计入 | — |

- 头部平台不链接任何长尾平台，长尾平台也很少链接它们。
- **含义：** 它们的受众彼此独立，长尾平台不会把流量导过去。每个头部平台都要单独准备一次发布日。

## 洞察 2：长尾平台是一张"反向链接交换网"

- 大多数免费档要求**把它的徽章放到你的官网首页**；同时这些平台自己的首页也挂着彼此的徽章。
- 结果是网里的链接**大多指向平台首页，而不是具体产品页**。
- **含义：** 在长尾平台上架的主要价值是 SEO：提升 Domain Rating、增加可被搜索引擎和 AI 助手发现的页面，而不是直接带来大量访客。

## 洞察 3：长尾平台的访客主要是其他创始人

- 很多平台用"先给 3–5 个产品点赞 / 留评论，才能免费发布"来驱动活跃度（ShipBoost、StackLedge、StartupBase、KittyLaunch、Launch List、Maidensail、Launch Llama 等）。
- 这形成了一个**创始人互访的闭环**：浏览你产品页的人，大多也是来发布自己产品的创始人。
- **含义：** 面向创始人、营销人员的 B2B 工具，这批受众很对口；面向普通消费者的产品，这里的受众很薄。

## 洞察 4：枢纽平台（被最多平台链接）

| 平台 | 被多少个平台链接 | 备注 |
|---|---|---|
| Twelve Tools | 34 | 与 Wired Business（29）、Ramen Tools、500.Tools 同一作者；徽章遍布几十个目录站 |
| Startup Fame | 30 | |
| Wired Business | 29 | |
| Findly.tools | 27 | 同时出售"代提交 100+ 目录"服务 |
| Nick Launches | 24 | **互相链接最多（10 对）**，独立开发者发布站圈子的社交中心 |
| Turbo0 | 24 | 一套目录站建站系统作者自己的目录 |
| Fazier | 20 | 自称 DR 83+ |
| saasfame / toolfame | 19 / 16 | 同一系统，彼此互链 |
| Dofollow.Tools | 17 | 姊妹站 DeepLaunch、Wayfindio、AgentWork |
| FrogDR | 16 | 不是发布站，而是很多目录站展示的 DR 检测徽章 |

## 洞察 5：链出最多的聚合站

| 平台 | 链向多少个平台 |
|---|---|
| LaunchAF | 87 |
| VibeCodingList | 50 |
| ShipBoost | 48（首页 "Featured on" 区块） |
| ListBulb | 45 |
| Wonderlaunch | 36 |

在这些站上架，等于离整张网只有一跳；但它们带来的主要是外链，不是买家。

## 洞察 6：抱团的小圈子（同一作者或同一套建站系统）

- **Twelve Tools 系**：Twelve Tools、Wired Business、Ramen Tools、500.Tools。
- **Mkdirs 建站系统**：Turbo0、aitoolfame、toolfame、saasfame、ToolRain、NewTool.site、aihuntlist、DodoDirectory；其中几个 *fame* 站互链。
- **LaunchIgniter 网络**：LaunchIgniter、StartupTrusted、SaaSGrow 三站互链，排期页还会互相推荐。
- **同一模板三站**：EasyLaunch、EasyDoFollow、LemonLaunch。
- **get-started 模板**：Good AI Tools、We Like Tools、Unite List、Trustiner、Acid Tools、ShinyLaunch、Startup Benchmarks。
- **Dofollow.Tools 系**：Dofollow.Tools、DeepLaunch、Wayfindio、AgentWork.Tools（同样的每日免费名额限制）。
- **Aura++ 合作圈**：Aura++、EarlyHunt、IndieHunt、MakerHunt、SideHunt、Uno Directory。
- **独立开发者社交圈**：Nick Launches 与 OpenHunts、SaaSCity、ScrollLaunch、StartupTrusted、SaaSGrow、Launch Llama、VibeCodingList、Commune、DanielLaunches、Aura++ 互链；LaunchIt 与 LaunchAF、Launch Llama、Wonderlaunch、VibeCodingList、Founder.best 互链。

同一圈子 = 同一套表单流程，批量提交时放在一起做效率最高。

## 洞察 7：各平台自报的影响力（未核实）

| 平台 | 自报数据 |
|---|---|
| Submit Hunt | 100–200 万 |
| Whatsthebigdata | 月访问 100 万以上，订阅 5 万以上 |
| SaaSCity | 30 天 52.1 万访问，日均 Google 展示 1.4 万，DR 65 |
| aitoolfame | 月访问 223,847（Cloudflare 统计） |
| Launch Llama | 15.4 万以上活跃用户，Newsletter 6.5 万，DA 73 |
| ProductWatch | 月访问 10 万以上，DR 72 |
| AI Directories | 月访问 6.5 万，展示 325 万次，DR 70 |
| LaunchIgniter | DR 75（付费档） |
| TinyShelf | DR 74 |
| Maidensail | DR 65 |
| LetsLaunch | DR 49 |

---

## 对发布策略的建议

1. **把头部平台当成真正的发布。** Product Hunt、Hacker News、Indie Hackers、BetaList；AI 工具再加 There's An AI For That 和 Futurepedia。每个都需要单独准备发布日、文案和支持者，长尾平台不会帮你导流过去。
2. **把长尾平台当成 SEO 和 AI 搜索的基础设施。** 40–60 个收录 + dofollow 外链能提升 Domain Rating（还能解锁要求 DR ≥ 10 / 20 的免费档），并产生可被搜索引擎和 AI 助手引用的页面。用自动化批量完成，不值得花创始人的时间。
3. **长尾里优先做枢纽和高 DR 平台**：Twelve Tools / Wired Business、Nick Launches、Fazier、Turbo0、Startup Fame、Findly、SaaSCity、ProductWatch、LaunchIgniter、StartupBase；再做聚合站（LaunchAF、ShipBoost、VibeCodingList），覆盖剩下的网。
4. **按受众判断值不值得投入长尾。** 访客主要是创始人：B2B / 面向创始人的工具收益大，面向消费者的产品收益小。
5. **你的官网首页会成为这张网的一个节点。** 挂 30–40 个徽章是常态；用一个服务端渲染的区块统一管理（横向滚动条即可），每次改版后重新验证，徽章被删会被对方下架。
6. **每半年重新抓一次关系图。** 小平台出现和消失都很快，规划新一轮发布前先刷新数据。

## 下一步可以补的数据

- 接入 Similarweb / Ahrefs，为每个节点补上真实流量、引荐来源、DR，验证"长尾平台主要交换外链而非访客"的判断。
- 用发布后的官网分析数据（来源域名统计）反推每个平台实际带来的访客和注册数，把这张链接网变成真正的"流量地图"。
