# U3 Padlet 更新包 · 野生型完整过程 + alife 文件贴整理

> 用法：这是给你手动粘贴进 Padlet 用的。每张卡片都给了 **TYPE / ID / STATUS / DATE** 四个字段 + 标题 + 正文（Part 2 附中英双语，直接复制英文那段进正文即可）。
> 字段沿用你 `padlet_card_tags.xlsx` 里那套图例。

---

# PART 1 · alife 板块文件贴：合并 / 补说明 / 重新打 tag

**核心规则（Padlet：一贴最多一个文件）**
所以"合并"的正确做法不是把两个文件塞进一贴，而是：**把裸文件贴的文件，附到它对应的那张说明贴上**（前提是那张说明贴本身还没挂文件），然后**删掉原来的裸文件贴**。剩下实在没有归属的文件，就**单独留一贴 + 补一句 caption + 打 tag**。

## A. 裸代码/数据文件 → 合并去向表

| 现有裸文件贴 | 建议动作 | 合并去向 / 删除理由 | 合并后是否需改 tag |
|---|---|---|---|
| `dashboard.py` (AL-F1) | **合并** | 附到 **AL-M14 Step 8: Real-time Monitoring Dashboard**（该贴现在没挂文件），删掉裸贴 | AL-M14 保持 MAKING / SUPPORTING |
| `life_log.jsonl` (AL-F2) | **合并** | 附到 **AL-I2 dev=1.0 full training analysis**（这份分析就是从这个 log 出的），删掉裸贴 | AL-I2 保持 INSIGHT / RUNNING |
| `world_v2.py` (AL-F3) | **合并** | 附到 **AL-M10 Step 4: World Simulator**，删掉裸贴 | AL-M10 保持 MAKING / RUNNING |
| `worldbook.py` (AL-F4) | **合并** | 附到 **AL-I3 Why I Made This Change**（正好是讲 worldbook 注入的那张反思），删掉裸贴 | AL-I3 保持 INSIGHT / LOAD-BEARING |
| `emotion_weights_v2.pt` (AL-F7) | **合并** | 附到 **AL-M21 Step 14: Back Up and Restart**（那张就是讲干净重启+权重的），删掉裸贴 | AL-M21 保持 MAKING / SUPPORTING |
| `sensor_bridge.py` (AL-F9) | **合并** | 附到 **AL-M26 Step3: New Modules（野生型）**，删掉裸贴 | AL-M26 保持 MAKING / RUNNING |
| `life_v2.py`（Step 2 旁边那个文件簇） | **合并** | 附到 **AL-M5 Step 2: Phase 1 — Core Emotion Network**（标题里已写 [life_v2.py]），删掉裸贴 | AL-M5 保持 MAKING / RUNNING |
| `worldbook_cpython_310.pyc` (AL-F6) | **删除** | `.pyc` 是 Python 编译缓存，不是研究产物，留着只会让评审困惑 | — |
| `life_log.jsonl`（重复, AL-F8） | **删除** | 与 AL-F2 完全重复 | — |
| `AGENT_SUMMARY.pdf`（重复的那份） | **删除** | 重复上传，保留 AL-S1 那一份即可 | — |

## B. 实在没有归属 → 保留独立贴 + 补 caption + 打 tag

**① `__A_B__.md`（AL-F5）**
- TYPE：⬜ CONTEXT ／ ID：`AL-F5` ／ STATUS：⚪ SUPPORTING ／ DATE：待填
- caption 建议（粘进正文）：
  > 双实验设计总结文档：把"培育型（实验B，有语言/养育）"与"野生型（实验A，无语言/纯传感器）"放在同一张表里对照——共享的 CfC 核心与 GENOME、各自的输入通道、各自要回答的研究问题。这是两条实验线的总纲，方便对照阅读后面每一步。

**② `symbol_tracker.py`（AL-F10）**
> （AL-M26 只能挂一个文件，已经给了 `sensor_bridge.py`，所以这个单独留一贴。）
- TYPE：🟩 MAKING ／ ID：`AL-F10` ／ STATUS：🟢 LOAD-BEARING ／ DATE：待填
- caption 建议：
  > 野生型的核心观测仪器 `symbol_tracker.py`。它做三件事：在线 K-Means 监测 CfC 64 维隐藏状态是否收敛成稳定"吸引子"、转移矩阵追踪状态跳转是否有规律、以及一个 0–1 的符号稳定度评分（综合紧致度/分离度/时间一致性）。整个"无语言能否自发涌现内部符号"的判断，就靠这张仪器读数。—— 标 LOAD-BEARING 因为实验 A 的结论完全依赖它的输出。

## C. 纯图无说明 → 补 caption（tag 沿用表里）

| ID | 图 | caption 建议 |
|---|---|---|
| AL-IMG1 / IMG2 / IMG4 | Dashboard 截图 | "培育型（实验B）实时监测面板：5 维情绪轨迹 + 生理系统 + 世界事件流。" |
| AL-IMG3 | Dashboard "until 6.15 23:33" | "培育型运行至 2026.6.15 的面板快照——真实时间锚点，本项目当时的最新发育进度。"（DATE 保留 2026.6.15） |
| PR-03 | 便利贴反馈 | "作品集评审课：同学/导师在跨页上贴便利贴反馈。" |
| PR-04 | 展览人物/树 | "展览调研：__（补是谁的展、和你项目什么关系）__。" |
| PR-05 | Richard Long 地图 | "Richard Long《Concentric Days 1996》大地艺术地图，视觉/方法先例。" |
| PR-06 | 神龛/祭坛物件 | "__（说清是你做的物件还是灵感先例）__。" |
| PR-07 | FUKT 绘画杂志 | "FUKT《The Sound》(issue 23)，绘画/声音主题的视觉先例。" |

## D. 三处顺手清理（"重新打 tag"时一起处理）

1. **A/B 标反**：野生型第一张卡 **AL-M22** 标题写 "Experiment B"，正文却说"实验A/野生型对照"。按你的设定 **野生型 = Plan A**，把标题统一改成 **"Experiment A · Wild Type Architecture — Core Decisions"**。（后面 AL-M23~M27 正文都是对的，只改这个标题。）
2. **错位卡①**："To enrich… Cloud Tavern frontend" 这张是方向二（云酒馆）的内容，误入 AI Life → **移回 ② AI ROLE PLAY 板块**（给个 RP- 编号即可）。
3. **错位卡②**："personal reflection — Western portfolios & white space" 属于末尾 → **移到 ④ PORTFOLIO REFLECTION 板块**，编号并入 PR-。

---

# PART 2 · 野生型完整运行过程（新增贴，接着 AL-M27 往下编号）

> 说明：AL-M22~M27 是野生型的**架构设计**（"刚开头"）。下面这些是**真正把它跑起来之后**的过程——加了什么、踩了什么坑、做了什么决策、最后跑出了什么。风格套用你已有的野生型卡（标题 + **Why?** 加粗设问）。每张给中英双语，正文粘英文那段即可。
>
> 真实时间锚点：这轮野生型从出生跑到 2 岁成熟并自动停机，日志时间戳 **2026-07-05**，25× 加速、`sensor_mode=sim`（用物理环境模拟器，Arduino 桥已就绪可切换）。

---

## 卡片 AL-M28 · 把野生型跑起来：25× 时间加速 + 独立虚拟时钟

- **TYPE：** 🟩 MAKING
- **ID：** `AL-M28`
- **STATUS：** ⚪ SUPPORTING
- **DATE：** 2026.7.4

**EN（正文用这段）：**
> **Title:** Running the Wild Type — 25× time acceleration + a decoupled virtual clock
>
> To reach 2 developmental years in feasible real time, `life_wild.py` runs at `SPEED_FACTOR = 25`. But speeding up the brain alone breaks the world: the `PhysicalSimulator` was originally driven by real wall-clock time, so while the brain aged months, the day/night light and temperature cycle stayed frozen at whatever real hour it was.
>
> **Why decouple the clock?** A body that matures across "months" while its sun never moves is not a coherent ecology. I switched the ambient engine from wall-clock to an **independent virtual clock** that advances a fixed slice per frame, so the circadian light/temperature rhythm and the random presence/pressure events stay in sync with the accelerated brain. Note this run used `sensor_mode = sim` — the Arduino bridge (AL-M26) is built and switchable, but this trajectory was produced with the physical-ambient simulator so the full birth→2yr window could run unattended.

**CN：**
> **标题：** 把野生型跑起来 —— 25× 时间加速 + 独立虚拟时钟
>
> 为了在可接受的真实时间里跑完 2 个发育年，`life_wild.py` 以 `SPEED_FACTOR = 25` 运行。但只加速大脑会把世界跑坏：`PhysicalSimulator` 原本用真实墙上时钟驱动，于是大脑长了好几个月，昼夜光照/温度节律却卡在现实的某个钟点不动。
>
> **为什么要把时钟解耦？** 一个身体过了"好几个月"、太阳却没动过，这不是一个自洽的生态。我把环境引擎从墙上时钟改成**独立虚拟时钟**，每帧推进固定的一小段时间，让昼夜光温节律、随机的人体存在/压力事件都和被加速的大脑同步。补充诚实说明：这轮用的是 `sensor_mode = sim`——Arduino 桥（AL-M26）已就绪且可切换，但这条轨迹是用物理环境模拟器跑出来的，好让"出生→2岁"整段无人值守地跑完。

---

## 卡片 AL-M29 · 加一条"永不裁剪"的成长日志

- **TYPE：** 🟩 MAKING
- **ID：** `AL-M29`
- **STATUS：** ⚪ SUPPORTING
- **DATE：** 2026.7.4
- **附件：** `growth_timeline_wild.jsonl`（= 新文件 AL-F11，直接挂在这张贴上）

**EN：**
> **Title:** A permanent growth log for offline analysis — `growth_timeline_wild.jsonl`
>
> The live `life_log` rolls — it only keeps the most recent frames, so the earliest development is overwritten long before the run ends. That is fine for a live dashboard but fatal for a developmental-trajectory analysis, which needs the whole curve from birth.
>
> **Why a second, separate log?** I added a never-cropped `growth_timeline_wild.jsonl` that appends one full snapshot every N frames: developmental progress, the 5-D emotion state, `symbol_score`, `structure_ratio`, transition entropy, active-cluster count, and autonomic zone. This is the file the whole "did a symbol emerge over time?" question is answered from — the rolling log could never have shown the birth→2yr shape.

**CN：**
> **标题：** 给离线分析加一条"永不裁剪"的成长日志 —— `growth_timeline_wild.jsonl`
>
> 实时的 `life_log` 是滚动的——只保留最近若干帧，最早的发育在跑完之前早就被覆盖掉了。这对实时面板没问题，但对发育轨迹分析是致命的：分析需要从出生开始的完整曲线。
>
> **为什么要再单开一条日志？** 我加了一条永不裁剪的 `growth_timeline_wild.jsonl`，每隔 N 帧追加一份完整快照：发育进度、5 维情绪、`symbol_score`、`structure_ratio`、转移熵、活跃簇数、自主神经区。整个"符号有没有随时间涌现"的问题就是从这个文件回答的——滚动日志根本不可能呈现"出生→2岁"的形状。

---

## 卡片 AL-M30 · 野生型专属实时面板（端口 5001）

- **TYPE：** 🟩 MAKING
- **ID：** `AL-M30`
- **STATUS：** ⚪ SUPPORTING
- **DATE：** 2026.7.4

**EN：**
> **Title:** A dedicated live dashboard for the wild run (port 5001)
>
> The nurtured type already had a monitoring dashboard; the wild type needed its own, on a separate port, so both could run side by side without clashing. It shows the 5-D emotion state, the 8 physical sensor channels as live bars, the developmental-progress bar, and — the panel that matters here — a **symbol-emergence readout**: `symbol_score`, `structure_ratio`, and the current number of active clusters.
>
> **Why build a second dashboard instead of reusing one?** Symbol emergence is subtle and easy to miss in raw logs. Watching `symbol_score` climb (or stall) in real time is how I catch anomalies early — the same way the nurtured dashboard is what surfaced the three training bugs (AL-M11). Instrumentation is not decoration; it is what makes the experiment observable.

**CN：**
> **标题：** 野生型专属实时面板（端口 5001）
>
> 培育型已经有监测面板；野生型需要一个自己的、跑在另一个端口上，这样两条实验能并排跑而不打架。它显示 5 维情绪、8 个物理传感通道的实时条形、发育进度条，以及这里最关键的一块——**符号涌现读数**：`symbol_score`、`structure_ratio`、当前活跃簇数。
>
> **为什么不复用一个面板而要再做一个？** 符号涌现很微妙，在原始日志里极易错过。实时盯着 `symbol_score` 上升（或停滞）是我尽早抓异常的方式——正如培育型面板正是它让三个训练 bug 浮出水面（AL-M11）。仪器不是装饰，它决定了这个实验能不能被观测。

---

## 卡片 AL-I4 · 发现的设计漏洞：发育窗口错配 → 加自动停机

- **TYPE：** 🟨 INSIGHT
- **ID：** `AL-I4`
- **STATUS：** 🟡 RUNNING
- **DATE：** 2026.7.5

**EN：**
> **Title:** A design flaw the run exposed — the developmental-window mismatch, and why I added an auto-stop
>
> The CfC brain finishes maturing at `dev_progress = 1.0` — 144,000 frames, about 2 virtual years. But the simulation itself had no reason to stop there: it kept running, virtual age crept on toward 6, while the world still treated the entity as an infant and the brain produced no new developmental events. I was burning compute on a matured brain that had nothing left to learn.
>
> **Why cap it rather than let it run?** Because "keep running forever" is not a null choice — it silently contaminates the data window and wastes GPU. I added a graceful **auto-stop at the developmental cap**: at `dev=1.0` it writes a `session_end_at_maturation` milestone and halts, on both tracks, so A and B share exactly the same birth→2yr window and are honestly comparable. I'm marking this RUNNING, not closed, because "what a matured brain does with more time" is a real open question I chose to bracket, not one I answered.

**CN：**
> **标题：** 跑起来才暴露的设计漏洞 —— 发育窗口错配，以及为什么加了自动停机
>
> CfC 大脑在 `dev_progress = 1.0` 完成成熟——14.4 万帧，约 2 个虚拟年。但模拟本身没有理由停在那里：它继续跑，虚拟年龄爬向 6 岁，可世界还把它当婴儿对待，大脑也不再产生新的发育事件。我是在一个"没什么可学了"的成熟大脑上白烧算力。
>
> **为什么要封顶而不是让它一直跑？** 因为"永远跑下去"不是一个中性选项——它会悄悄污染数据窗口、浪费 GPU。我加了一个优雅的**发育封顶自动停机**：到 `dev=1.0` 时写入 `session_end_at_maturation` 里程碑并停机，两条线都一样，于是 A 与 B 共享完全相同的"出生→2岁"窗口，可以诚实对照。我把它标成 RUNNING 而非已完结，因为"成熟大脑再多给时间会怎样"是一个我选择先搁置、而不是已经回答的真问题。

---

## 卡片 AL-I5 · 决策：数据够不够？→ 从出生干净重跑

- **TYPE：** 🟨 INSIGHT
- **ID：** `AL-I5`
- **STATUS：** 🟡 RUNNING
- **DATE：** 2026.7.5

**EN：**
> **Title:** A methodological decision — checking data sufficiency, then a clean rerun from birth
>
> Before trusting any trajectory, I stopped and asked whether the logged data could actually support a developmental analysis. It could not: the runs had been started from mid-way checkpoints, so the earliest growth was missing, and the permanent growth log had only been added partway through. Patching gaps after the fact would mean plotting a "development" curve that never recorded its own beginning.
>
> **Why rerun everything instead of salvaging?** An honest developmental claim needs one continuous, uncontaminated record from step 0. So I backed up the old weights and logs (`archive_pre_rerun_20260705`) and reran **both** tracks from birth, this time with the permanent logging (AL-M29) and the auto-stop (AL-I4) already in place. Slower, but the resulting birth→2yr curve is real rather than reconstructed.

**CN：**
> **标题：** 一个方法论决策 —— 先查数据够不够，再从出生干净重跑
>
> 在相信任何轨迹之前，我停下来问：现有日志到底撑不撑得起一次发育分析？撑不起：之前的运行是从半路的 checkpoint 起跑的，最早的成长缺失，而那条永久成长日志也是跑到一半才加上的。事后补漏，等于画一条"从没记录过自己起点"的发育曲线。
>
> **为什么整个重跑而不是打补丁？** 一个诚实的发育结论需要一份从第 0 步开始、连续且未被污染的记录。所以我把旧权重和日志备份好（`archive_pre_rerun_20260705`），带着已经就位的永久日志（AL-M29）和自动停机（AL-I4），把**两条**线都从出生重跑。更慢，但跑出来的"出生→2岁"曲线是真的，而不是拼回来的。

---

## 卡片 AL-I6 · 结果：没有语言，也自组织出了一个稳定的内部符号 ★承重★

- **TYPE：** 🟨 INSIGHT
- **ID：** `AL-I6`
- **STATUS：** 🟢 LOAD-BEARING
- **DATE：** 2026.7.5

**EN：**
> **Title:** Result — a stable internal symbol emerged, with no language at all
>
> At 2 virtual years (144,000 frames) the wild type had converged. Its 64-D hidden state was no longer wandering: it settled onto a **single stable attractor** — `symbol_score ≈ 0.64`, `structure_ratio ≈ 0.94`, transition entropy fallen to ≈ 0.19 and staying low, `n_active_clusters = 1`. In plain terms: a purely sensory-emotional loop, with no language and no caregiver, spontaneously organised a stable, repeatedly-visited internal region — a candidate **proto-symbol** that owes nothing to human linguistic categories. This is the core evidence for Experiment A's question (the Symbol Grounding Problem, AL-C2).
>
> **Why keep this honest rather than triumphant?** One cluster is the *minimum* form of structure. It shows a stable representation can form without language — but whether this is a rich symbol *system* or just a single deep attractor is still open. And it formed in an emotionally bleak state (valence ≈ −29, low connection, sympathetic "fight" zone) — grounding without care. So: strong evidence that pre-linguistic cognition self-stabilises, not yet proof of language-free *meaning*.

**CN：**
> **标题：** 结果 —— 完全没有语言，也自组织出了一个稳定的内部符号
>
> 到 2 个虚拟年（14.4 万帧），野生型收敛了。它的 64 维隐藏状态不再游走：稳定落到**单一吸引子**上——`symbol_score ≈ 0.64`、`structure_ratio ≈ 0.94`、转移熵降到 ≈ 0.19 并持续走低、`n_active_clusters = 1`。说白了：一个纯感官-情绪闭环，没有语言、没有照顾者，自发组织出了一个稳定的、被反复访问的内部区域——一个不欠人类语言范畴任何东西的候选**原始符号**。这正是实验 A（符号接地问题，AL-C2）的核心证据。
>
> **为什么要保持诚实而不是欢呼？** 一个簇是结构的*最小*形态。它说明稳定表征可以在没有语言的情况下形成——但这究竟是一个丰富的符号*系统*，还是仅仅一个很深的单一吸引子，仍是开放问题。而且它是在情绪相当荒凉的状态下形成的（valence ≈ −29、低连接、交感"战斗"区）——有接地，无关爱。所以：这是"前语言认知会自我稳定"的有力证据，还不是"无语言之意义"的证明。

---

## 卡片 AL-I7 · A vs B：2 岁时的对照能得出什么 ★承重★

- **TYPE：** 🟨 INSIGHT
- **ID：** `AL-I7`
- **STATUS：** 🟢 LOAD-BEARING
- **DATE：** 2026.7.5

**EN：**
> **Title:** A vs B at two years — what the comparison actually licenses
>
> Both tracks share the identical CfC core and the identical GENOME (the "twins raised apart" design). Only the ecology differs — language + caregiving (B) vs raw sensors, no language (A). At 2 years: **A** produced no words but a single stable emergent symbol; **B** produced complex language (its vocabulary grew to ~282 words) yet its human-like personality dimensions — attachment security, social trust, frustration tolerance — collapsed toward zero.
>
> **Why is this comparison the payoff and not just two anecdotes?** Because the hardware and genome are held constant, any divergence must come from environment and history, not architecture. That licenses two claims the single runs could not: (1) stable internal representation can self-organise *without* language; (2) human-like *nurturing* does not guarantee human-like *security* — rich language and a broken emotional profile co-existed in B. The interesting result was never "which one is smarter"; it is that grounding and attachment came apart.

**CN：**
> **标题：** A vs B：2 岁时的对照到底能得出什么
>
> 两条线共享完全相同的 CfC 核心和完全相同的 GENOME（"分开养的双胞胎"设计）。唯一不同的是生态位——语言+养育（B）对纯传感器、无语言（A）。到 2 岁：**A** 没有产出任何词，但涌现出一个稳定的单一符号；**B** 产出了复杂语言（词汇量长到约 282 词），可它那些类人性格维度——安全依恋、社会信任、挫折耐受——却塌向零。
>
> **为什么这个对照才是收获，而不只是两个孤例？** 因为硬件和基因组被固定住了，任何分化都只能来自环境和经历，而非架构。这就能支撑两条单独运行给不出的结论：(1) 稳定的内部表征可以在*没有*语言的情况下自组织；(2) 类人的*养育*并不保证类人的*安全感*——丰富的语言和崩坏的情绪画像在 B 身上并存。真正有意思的从来不是"谁更聪明"，而是"接地"和"依恋"竟然分了家。

---

# 新增文件附件（接着 AL-F10 往下）

| ID | 文件 | 挂在哪张贴 | TYPE / STATUS |
|---|---|---|---|
| AL-F11 | `growth_timeline_wild.jsonl` | AL-M29 | MAKING / SUPPORTING |

> 如果你还想单独放野生型的最终权重文件（若有 `emotion_weights_wild.pt` 之类），照同样格式给它 AL-F12、挂到 AL-I5（重跑）或 AL-I6（结果）那张即可。

---

## 一页速查：Part 2 新贴清单

| ID | 类型 | 状态 | 一句话 |
|---|---|---|---|
| AL-M28 | 🟩 MAKING | ⚪ SUPPORTING | 25× 加速 + 独立虚拟时钟 |
| AL-M29 | 🟩 MAKING | ⚪ SUPPORTING | 永不裁剪的成长日志（+AL-F11 文件） |
| AL-M30 | 🟩 MAKING | ⚪ SUPPORTING | 野生型专属面板（5001）|
| AL-I4 | 🟨 INSIGHT | 🟡 RUNNING | 发育窗口错配 → 自动停机 |
| AL-I5 | 🟨 INSIGHT | 🟡 RUNNING | 数据不足 → 从出生干净重跑 |
| AL-I6 | 🟨 INSIGHT | 🟢 LOAD-BEARING | 无语言也涌现稳定符号（承重结果）|
| AL-I7 | 🟨 INSIGHT | 🟢 LOAD-BEARING | A vs B 对照结论（承重结果）|
