# AI Life 板块 · 按博客顺序的干净标签表（颜色 = ID 前缀）

> 依据：`Padlet - Investigate Blog.pdf`（你重排+合并后的版本）里的真实顺序。
> 规则：**每帖的颜色(TYPE)必须和 ID 前缀一致**。映射见下。`AL-S`(文档)/`AL-F`(文件)是"角色前缀",颜色可变通（文档可以是灰/紫）。
> 用法：对照你 Padlet 逐帖核对"TYPE 色块 + ID"两个字段。⚠ 标记处是需要你动手的改动。

**前缀↔颜色：** 🟦QUESTION=AL-Q ｜ 🟪PRECEDENT=AL-R/AL-C ｜ 🟨INSIGHT=AL-I ｜ 🟩MAKING=AL-M ｜ 🟧PRIMARY=AL-P ｜ ⬜CONTEXT=AL-S

---

## 一 · 推理主链（Plan A / B 共用的骨架，顺序 OK）

| # | 帖子标题 | TYPE | ID | STATUS | 备注 |
|---|---|---|---|---|---|
| 概览 | SUMMARY〔AGENT_SUMMARY.pdf〕 | ⬜ CONTEXT | `AL-S1` | SUPPORTING | ✓ |
| 1 | Can you keep an AI "alive" like a pet? | 🟦 QUESTION | `AL-Q1` | LOAD-BEARING | ✓ |
| 2 | Why doesn't an AI think when no one is talking? | 🟦 QUESTION | `AL-Q2` | LOAD-BEARING | ✓ |
| — | ANSWER 1 ｜ DMN (Raichle 2001) | 🟪 PRECEDENT | `AL-C1` | SUPPORTING | ✓ |
| — | ANSWER 2 ｜ Symbol Grounding (Harnad; Bender&Koller) | 🟪 PRECEDENT | `AL-C2` | SUPPORTING | ✓ |
| 3 | What if I wire it up to sensors? | 🟦 QUESTION | `AL-Q3` | LOAD-BEARING | ✓ |
| 4 | Are the three problems separate, or one? | 🟦 QUESTION | `AL-Q4` | LOAD-BEARING | ✓ |
| 5 | What would the smallest system look like? | 🟦 QUESTION | `AL-Q5` | LOAD-BEARING | ✓ |
| 6 | When the model "remembers," what changed? | 🟦 QUESTION | `AL-Q6` | LOAD-BEARING | ✓ |
| — | From Text to Life (Nisioti 2024) | 🟪 PRECEDENT | `AL-R0` | SUPPORTING | ✓ |
| — | Why I went looking for this paper | 🟪 PRECEDENT | `AL-R1` | LOAD-BEARING | ✓ |
| — | The paper gave me a definition | 🟪 PRECEDENT | `AL-R2` | LOAD-BEARING | ✓ |
| — | Does an LLM have internal states? | 🟪 PRECEDENT | `AL-R3` | LOAD-BEARING | ✓ |
| — | R4) ELM | 🟪 PRECEDENT | `AL-R4` | SUPPORTING | ✓ |
| — | R5) LMX | 🟪 PRECEDENT | `AL-R5` | SUPPORTING | ✓ |
| — | R6) Learning lives in the population | 🟪 PRECEDENT | `AL-R6` | LOAD-BEARING | ✓ |
| — | R7) A sharper question | 🟪 PRECEDENT | `AL-R7` | LOAD-BEARING | ✓ |
| 7 | Does it develop behaviour never designed in? | 🟦 QUESTION | `AL-Q7` | LOAD-BEARING | ✓ |

> 说明：Q1–Q7 每张标题都是**问句**，所以统一 🟦 QUESTION 蓝，与 `AL-Q` 前缀一致，且保住"读 Q1→Q7 就是整条论证"这条主线。R 线是论文精读=文献，统一 🟪 PRECEDENT 紫。

---

## 二 · Plan A 培育型：INSIGHT 与 MAKING（这里是重灾区）

### 2.1 INSIGHT 线（🟨 AL-I）— 按阅读顺序重排

| 帖子标题 | TYPE | 新 ID | 原 ID | STATUS | 改动 |
|---|---|---|---|---|---|
| Why I replaced the GRU emotion core with CfC + AutoNCP | 🟨 INSIGHT | `AL-I1` | **AL-L1** | LOAD-BEARING | ⚠ `L` 前缀不存在，改回 `AL-I1` |
| Step 1: Design Concept & Technology Selection〔phase_en.pdf〕 | 🟨 INSIGHT | `AL-I2` | 无ID | SUPPORTING | ⚠ 是设计/选型决策，不是动手做→INSIGHT，补 ID |
| Developmental stage dev=1.0 — full training analysis | 🟨 INSIGHT | `AL-I3` | AL-I2 | RUNNING | ⚠ 号右移（原 I2→I3） |
| Why I Made This Change (worldbook / injection / restart) | 🟨 INSIGHT | `AL-I4` | AL-I3 | LOAD-BEARING | ⚠ 号右移（原 I3→I4） |

> 如果你不想动 dev 分析(I2)和 Why I Made(I3)这两号，也可以把 Step 1 设计卡放到 `AL-I5`(接在最后)——只是号和阅读顺序会对不上。推荐按上表阅读顺序重排。

### 2.2 MAKING 线（🟩 AL-M）— 去重 + 按顺序重排为 M1…M16

| 顺序 | 帖子标题 | TYPE | 新 ID | 原 ID | 改动 |
|---|---|---|---|---|---|
| 1 | Built a Python AI-life simulator (build overview) | 🟩 MAKING | `AL-M1` | AL-M1 | ✓ |
| 2 | Step 2: Phase 1 — Core Emotion Network | 🟩 MAKING | `AL-M2` | AL-M5 | 号 5→2 |
| 3 | Step 3: Phase 2 — Layering Biological Systems | 🟩 MAKING | `AL-M3` | AL-M6 | 号 6→3 |
| — | 〔短卡〕Added three physiological regulation systems | — | — | AL-M8 | ⚠ 与 Step 3 内容重复→**合并/删除**（这是最早的旧摘要卡） |
| 4 | Supplementary: Pre-Integration Smoke Test | 🟩 MAKING | `AL-M4` | AL-M7 | SUPPORTING；号 7→4 |
| — | 〔短卡〕Added MBTI + attachment style to parents | — | — | AL-M8 | ⚠ 内容并入 Step 4 世界模拟器→**合并/删除**（旧摘要卡） |
| 5 | Step 4: World Simulator | 🟩 MAKING | `AL-M5` | AL-M9 | 号 9→5 |
| 6 | Step 5: Discovering & Fixing Three Training Bugs | 🟩 MAKING | `AL-M6` | AL-M10 | 号 10→6 |
| 7 | Step 6: Phase 3/4 Interface Placeholders | 🟩 MAKING | `AL-M7` | AL-M11 | 号 11→7 |
| 8 | Step 7: Scheduled Task — Automated Code Injection | 🟩 MAKING | `AL-M8` | AL-M12 | 号 12→8 |
| 9 | Step 8: Real-time Monitoring Dashboard | 🟩 MAKING | `AL-M9` | AL-M13 | SUPPORTING；号 13→9 |
| 10 | Dashboard: Full Bilingual UI | 🟩 MAKING | `AL-M10` | AL-M13 | ⚠ 独立帖，别和上面共号；SUPPORTING |
| 11 | Step 9: Switching to a Local LLM via Ollama | 🟩 MAKING | `AL-M11` | AL-M14 | 号 14→11 |
| 12 | step 10: Discover the Missing Injection | 🟩 MAKING | `AL-M12` | AL-M15 | 号 15→12 |
| 13 | Step 11: Reconnect the World Setting | 🟩 MAKING | `AL-M13` | 无ID | ⚠ 补 ID |
| 14 | Step 12: Expand the Context Window (num_ctx 16384) | 🟩 MAKING | `AL-M14` | 无ID | ⚠ 补 ID |
| 15 | Step 13: Reinforce the Bilingual Rule | 🟩 MAKING | `AL-M15` | 无ID | ⚠ 补 ID |
| 16 | Step 14: Back Up and Restart Clean & Verify | 🟩 MAKING | `AL-M16` | 无ID | ⚠ 补 ID |

### 2.3 文件附件（🔗 不单独给号，挂到对应帖）

| 文件 | 处理 |
|---|---|
| `life_v2.py` | 挂到 `AL-M2`(Step 2) |
| `world_v2.py` | 挂到 `AL-M5`(Step 4) |
| `dashboard.py` | 挂到 `AL-M9`(Step 8) |
| `life_log.jsonl` | 挂到 `AL-I3`(dev 分析) |
| `phase_status.json` | 挂到 `AL-M8`(Step 7) |
| `emotion_weights_v2.pt` | 挂到 `AL-M16`(Step 14) |
| `worldbook.py` | 挂到 `AL-I4`(Why I Made This Change) |
| `__A_B__.md` | 独立帖，⬜ CONTEXT，`AL-F5`（双实验设计总纲） |
| `worldbook_cpython_310.pyc` | ⚠ **删除**（编译缓存，非研究产物） |
| `life_log.jsonl`（重复那份） | ⚠ **删除**（重复） |

### 2.4 走错板块的卡

| 帖子 | 处理 |
|---|---|
| "personal reflection — Western portfolios & white space"（夹在 Step 11/12 之间） | ⚠ 移到末尾 **PORTFOLIO REFLECTION** 板块，🟨 INSIGHT，编 `PR-##` |

---

## 三 · Plan B 野生型（架构帖目前**全部没 ID**，以下为建议）

> 说明：这几张是"设计决策/为什么这么设计"→ 属 🟨 INSIGHT，不是绿色 MAKING；只有真正**新建了模块**的 Step3 是 🟩 MAKING。A/B 标签也要修（见备注）。

| 顺序 | 帖子标题 | TYPE | 建议 ID | STATUS | 备注 |
|---|---|---|---|---|---|
| 1 | ~~Experiment B~~ · Wild Type Architecture — Core Decisions | 🟨 INSIGHT | `AL-I5` | LOAD-BEARING | ⚠ 标题"Experiment B"改 **Experiment A**（野生型=A） |
| 2 | Step1: CfC Neural Core — 22D vs 36D〔life_wild.py〕 | 🟨 INSIGHT | `AL-I6` | LOAD-BEARING | 控制变量的设计论证 |
| 3 | Step2: Removed Modules — Stripping Language & Narrative | 🟨 INSIGHT | `AL-I7` | LOAD-BEARING | 删除决策的论证 |
| 4 | Step3: New Modules — Sensor Bridge + Symbol Tracker | 🟩 MAKING | `AL-M17` | RUNNING | ✅ 真新建模块→保持 MAKING；挂 `sensor_bridge.py`、`symbol_tracker.py` |
| 5 | Step4: Preserved Core Mechanisms — Comparable Baseline | 🟨 INSIGHT | `AL-I8` | LOAD-BEARING | 保留理由的论证 |
| 6 | Perception Source — Arduino Physical Sensors | 🟨 INSIGHT | `AL-I9` | LOAD-BEARING | 建议移到 Step1 前面（它是感知层的总述） |

> `symbol_tracker.py` 若想单独强调，可另建一帖 🟩 MAKING `AL-M18`（核心观测仪器），STATUS LOAD-BEARING。

---

## 四 · 一句话总结要改什么

1. `AL-L1` → `AL-I1`（前缀笔误）。
2. INSIGHT 线按阅读顺序重排：I1=GRU/CfC、I2=Step1设计、I3=dev分析、I4=Why I Made。
3. MAKING 线去重+重排 M1…M16（消灭 M8×2 / M9×5 / M13×5 的串号）。
4. Step 11–14 补 ID（M13–M16）。
5. 野生型 6 张架构帖补 ID：5 张 INSIGHT(I5–I9) + 1 张 MAKING(M17)；A/B 标签修正。
6. `.pyc`、重复 `life_log.jsonl` 删除；其余文件挂到对应帖。
7. "personal reflection" 移到作品集反思板块。
