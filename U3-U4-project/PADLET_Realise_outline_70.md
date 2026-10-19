# Realise Padlet · 帖子构思大纲（约 70 篇）

> 参照更新后的 Investigate Blog 体例。  
> Realise = **Movement 4：from experiment to object**（Investigate 阅读指南里已写明的 `RE-` 前缀）。  
> 目标：**约 70 篇**，覆盖「实验结束 → 产品定位 → 硬件/软件实现 → 诱导演示 → 作品集产出 → 诚实边界」。  
> 语言：Padlet 正文建议**全英文**（与 Investigate 一致）；本大纲中文方便你对照。

---

## 0. 沿用 Investigate 的四字段（不要改规则）

| FIELD | 含义 | Realise 怎么用 |
|---|---|---|
| **TYPE** | 色块类别 | ⬜ CONTEXT / 🟧 PRIMARY / 🟨 INSIGHT / 🟩 MAKING / 🟦 QUESTION / 🟪 PRECEDENT |
| **DATE** | 思考/动手发生的时间 | 真实轨迹；不知道就写大概周次，别伪造精确到分的假日期 |
| **ID** | 链上位置 + 可交叉引用 | 见下方 `RE-` 编号规则 |
| **STATUS** | 这张卡在研究里站哪 | LOAD-BEARING / SUPPORTING / RUNNING / DONE / SEED / DEAD END |

### ID 编号规则（镜像 AL-）

| 前缀 | 用途 | 大约数量 |
|---|---|---|
| `RE-S` | 总览 / 怎么读 / 桥接文档 | 4 |
| `RE-Q` | 驱动 Realise 的问题链（读完应能跟住论证） | 6 |
| `RE-I` | 推理 / 改主意 / 诚实边界（最强卡，别埋进 MAKING） | 14 |
| `RE-M` | 动手：硬件、固件、软件、打印、接线、演示 | 36 |
| `RE-C` | 产品/生态相关先例或引用（少量即可） | 4 |
| `RE-P` | 一手：诱导演示记录 / 短测反馈（若有） | 4 |
| **合计** | | **≈ 68–72** |

### MAKING 卡固定四行（与野生型流水账一致）

```
File:
What was done:
Why:
What it means:
```

底部：`DATE | ID | Status`  
INSIGHT 卡：写清「我改了什么想法 / 为什么这张是 load-bearing」，不要写成日志摘要。  
QUESTION 卡：标题尽量是**问句**（像 AL-Q1→Q7）。

### 与 Investigate 的接缝（开篇就要说清）

- Investigate 已经写了：双轨实验、田野、`AL-I19`（拒掉电子宠物）、野生型仿真局限、`AL-Q7`（无语言可读的状态）。
- Realise **不是**再做一遍实验，而是：**把已验证的 CfC 核 + 基因组概念，转成「生态环境情感化转译」物体**。
- Investigate 里提到的 `RE-01`（无语言可读性）= Realise 问题链的起点，不要另起炉灶。

---

## 1. 你 Realise 里已经写了的内容 → 建议 ID 映射

| 现有帖（PDF 里） | 建议 TYPE | 建议 ID | STATUS | 备注 |
|---|---|---|---|---|
| AI Life Project Overview: From Investigate to Realise | ⬜ CONTEXT | `RE-S2` | LOAD-BEARING | 保留，略收紧与 S1/S3 的分工 |
| The Pivot: Companionship → Ecological Translation | 🟨 INSIGHT | `RE-I1` | LOAD-BEARING | 核心转向；可交叉引用 `AL-I19` |
| How Device Grows Out of Investigate Tech | 🟨 INSIGHT | `RE-I2` | LOAD-BEARING | 继承清单（CfC / genome / sensors） |
| Honest Boundaries of Scope | 🟨 INSIGHT | `RE-I3` | LOAD-BEARING | 三界限：短时诱导 / 设计权重≠涌现 / 单点传感 |
| Positioning Statement | 🟨 INSIGHT | `RE-I4` | LOAD-BEARING | 长期愿景一句话 |
| project start：hardware preparation | 🟩 MAKING | `RE-M1` | SUPPORTING | 补齐 File/What/Why/Means |
| design, modeling and print：appearance & case | 🟩 MAKING | `RE-M5` | SUPPORTING | 拆成多张原子卡更像 Investigate |
| Arduino USB-C case（5 fail → 6 succeed） | 🟩 MAKING | `RE-M8` | DONE | **好卡**：失败可见；保留「xd」语气即可 |
| sensor connection test | 🟩 MAKING | `RE-M12` | SUPPORTING | 拆成「每通道一张」更好 |
| set up RPi4B and connect Arduino | 🟩 MAKING | `RE-M18` | SUPPORTING | 把 USB 坑单独成 INSIGHT |
| ChatGPT wiring diagram | 🟩 MAKING | `RE-M11` | SUPPORTING | 标注 AI 协助（与田野仪器披露一致） |
| Genome Presets & Sensor Inference Design | ⬜ CONTEXT | `RE-S3` | SUPPORTING | 文档挂载；论证写在 I/Q 卡 |
| Sensory Weighting System Technical Design | ⬜ CONTEXT | `RE-S4` | SUPPORTING | 同上 |

> 结论：你不是从零写 70 篇——大约 **12 篇已有骨架**，需要：**补 HOW TO READ、补问题链、把粗 MAKING 拆细、补软件/演示/作品集/收尾**。

---

## 2. 建议阅读动线（评委怎么扫）

1. `RE-S1` 怎么读  
2. `RE-Q1 → Q6` 问题脊骨（5 分钟读完应懂 Realise 在争什么）  
3. `RE-I1 → I4` 转向与边界  
4. `RE-M*` 造物过程（可扫标题）  
5. `RE-P*` 诱导演示证据  
6. `RE-I*` 收尾反思 + 作品集产出卡  

---

## 3. 完整帖表（约 70）

### A · 开篇桥接（4）

| # | 标题（英文，可直接用） | TYPE | ID | STATUS | 写什么（一句话） |
|---|---|---|---|---|---|
| 1 | HOW TO READ THIS PADLET — Realise | ⬜ CONTEXT | `RE-S1` | SUPPORTING | 镜像 Investigate 蛋壳指南：四字段、`RE-` 前缀、与 AL-/PR- 关系 |
| 2 | From Investigate to Realise — Project Overview | ⬜ CONTEXT | `RE-S2` | LOAD-BEARING | **已有**：起源 / 双轨 / 田野 / Realise 任务 |
| 3 | What This Phase Is Not | 🟨 INSIGHT | `RE-I0` | LOAD-BEARING | 不是第二轮实验；不是电子宠物；不声称学会了生态行为 |
| 4 | Inheritance Map — What Travels From AL- to RE- | ⬜ CONTEXT | `RE-S3` | SUPPORTING | 一张表：CfC、5D 情绪、genome、传感器合同、田野问题 → 分别落到哪张 RE 卡 |

---

### B · 问题脊骨 RE-Q（6）— 像 AL-Q1→Q7

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 5 | What must stay legible without a dashboard? | 🟦 QUESTION | `RE-Q1` | LOAD-BEARING | = Investigate 里点名的 RE-01；接 `AL-Q7` + 田野 |
| 6 | If the entity inhabits an ecosystem, whose feelings are being shown? | 🟦 QUESTION | `RE-Q2` | LOAD-BEARING | 环境压力 vs 用户情绪；翻译媒介 vs 被爱对象 |
| 7 | Can one body wear many natures? | 🟦 QUESTION | `RE-Q3` | LOAD-BEARING | 变色龙：同一硬件 + 基因组权重表 |
| 8 | Where do the thresholds come from — literature, or lived observation? | 🟦 QUESTION | `RE-Q4` | LOAD-BEARING | 舒适区间自动标定 vs 硬编码；接「新生儿先熟悉环境」叙事 |
| 9 | What can five weeks honestly demonstrate? | 🟦 QUESTION | `RE-Q5` | LOAD-BEARING | 短时诱导事件 vs 慢生态趋势（为 I3 铺垫） |
| 10 | When light breathes, is that emergence or design? | 🟦 QUESTION | `RE-Q6` | LOAD-BEARING | 强制区分：加权规则（设计）≠ CfC 时序动态（可涌现） |

---

### C · 定位与转向 INSIGHT（已有 + 补强，共 8）

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 11 | The Pivot — From Emotional Companionship to Ecological Translation | 🟨 INSIGHT | `RE-I1` | LOAD-BEARING | **已有**；加一句交叉引用 `AL-I19` |
| 12 | Companionship Is a By-product, Not a Goal | 🟨 INSIGHT | `RE-I5` | LOAD-BEARING | 表达层硬线：输出「环境在经历什么」，不是讨好 |
| 13 | How the Device Grows Directly Out of Investigate | 🟨 INSIGHT | `RE-I2` | LOAD-BEARING | **已有** |
| 14 | Honest Boundaries of Scope | 🟨 INSIGHT | `RE-I3` | LOAD-BEARING | **已有** |
| 15 | Positioning Statement | 🟨 INSIGHT | `RE-I4` | LOAD-BEARING | **已有** |
| 16 | Field Research Forced the Product Question | 🟨 INSIGHT | `RE-I6` | LOAD-BEARING | 田野不是「好不好摸」，是「无仪表盘如何读生命系统」→ 产品命题 |
| 17 | Why Not a Dashboard App Alone | 🟨 INSIGHT | `RE-I7` | LOAD-BEARING | 拒绝纯数据 UI；物理表达才是 Realise 的答辩点 |
| 18 | Naming the Object — ANIMA / A Living Presence | 🟨 INSIGHT | `RE-I8` | SUPPORTING | 命名如何承担「翻译媒介」而非宠物 |

---

### D · 产品架构决策（设计论证，偏 I + 少量 C）（10）

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 19 | System Architecture — Environment → Arduino → USB/JSON → Pi → 5D → Light | 🟨 INSIGHT | `RE-I9` | LOAD-BEARING | 信号链总图（对应 product design 第 2 屏） |
| 20 | Seven Universal Sensory Channels | 🟨 INSIGHT | `RE-I10` | LOAD-BEARING | T/M/G/L/S/pH/EC；「权重为零仍记录」原则 |
| 21 | A Genome Is a Sensory Weighting Table, Not Different Hardware | 🟨 INSIGHT | `RE-I11` | LOAD-BEARING | 工程化 Investigate 的「气质基因组」 |
| 22 | Genome: Soil / Root | 🟩 MAKING | `RE-M2` | LOAD-BEARING | JSON 权重 + 干旱特征应激；挂基因组文档 |
| 23 | Genome: Freshwater | 🟩 MAKING | `RE-M3` | LOAD-BEARING | moisture=0；低氧风险组合 |
| 24 | Genome: Indoor Air | 🟩 MAKING | `RE-M4` | LOAD-BEARING | VOC/湿度；通风不良 |
| 25 | Two-Layer Sensory Weighting — Comfort Curve × Genome Weight | 🟨 INSIGHT | `RE-I12` | LOAD-BEARING | 挂 `感官加权系统技术设计文档.md` |
| 26 | From Feeling to Light — 5D → Hue / Breath / Stability / Ring / Pulse | 🟨 INSIGHT | `RE-I13` | LOAD-BEARING | 表达映射；强调非言语 |
| 27 | Why a Liquid Neural Network Here | 🟨 INSIGHT | `RE-I14` | LOAD-BEARING | 变化率 / 多通道一致 / 零权重≠盲 |
| 28 | Precedent: Ambient / Ecological Sensing Interfaces | 🟪 PRECEDENT | `RE-C1` | SUPPORTING | 1–2 个相关先例，说明你不 overlapping Unit 2 |

---

### E · 外壳与物理造物 MAKING（12）

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 29 | Hardware Preparation — Parts Land on the Desk | 🟩 MAKING | `RE-M1` | SUPPORTING | **已有骨架**；列 BOM：Pi / Uno / 电池塔 / LED / 探头 |
| 30 | Why an Egg — Closed Diffuser Body | 🟨 INSIGHT | `RE-I15` | LOAD-BEARING | 形态理由：全身漫射光 = 皮肤；探针伸出介质 |
| 31 | Modeling the Shell — First Printable Body | 🟩 MAKING | `RE-M5` | SUPPORTING | **已有**；CAD → 切片 → 打印 |
| 32 | Shell Iteration — Fit, Access, Probe Exits | 🟩 MAKING | `RE-M6` | SUPPORTING | 开孔、分模、装配公差 |
| 33 | Diffuser + LED Core Placement | 🟩 MAKING | `RE-M7` | SUPPORTING | WS2812 环；光核位置 |
| 34 | Arduino USB-C Case — Five Failures, Sixth Fits | 🟩 MAKING | `RE-M8` | DONE | **已有**；保留失败叙事 |
| 35 | Battery Tower 5V/4A — Untethered Power | 🟩 MAKING | `RE-M9` | SUPPORTING | 21700 + pogo；自包含 |
| 36 | Passive Decision — Closed Egg Needs a Heatsink Later | 🟨 INSIGHT | `RE-I16` | SUPPORTING | Pi 温升；诚实待办 |
| 37 | Anatomy A–F — What Lives Inside the Object | ⬜ CONTEXT | `RE-S4` | SUPPORTING | 外壳/光核/认知核/传感板/电源/探针（作品集页同步） |
| 38 | Probe Design — Reaching Into Soil / Water / Air | 🟩 MAKING | `RE-M10` | SUPPORTING | 防水探头如何出壳 |
| 39 | AI-Assisted Wiring Diagram (and What I Still Had to Verify) | 🟩 MAKING | `RE-M11` | SUPPORTING | **已有**；披露 ChatGPT；哪些脚位后来改了 |
| 40 | Precedent: Biomimetic Enclosure / Soft Glow Objects | 🟪 PRECEDENT | `RE-C2` | SUPPORTING | 可选；别堆 |

---

### F · 传感接线与标定（14）— 把「connection test」拆成原子卡

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 41 | The Contract — Serial Protocol Before Anything Else | 🟩 MAKING | `RE-M12` | LOAD-BEARING | 挂 `SERIAL_PROTOCOL.md`；115200；JSON 一行/~2s |
| 42 | Clock Source Must Be 16MHz — The Flash Failure That Wasn't the Cable | 🟨 INSIGHT | `RE-I17` | LOAD-BEARING | LGT8F328 坑；**强卡** |
| 43 | This Board Is LGT8F328P, Not ATmega328P | 🟨 INSIGHT | `RE-I18` | LOAD-BEARING | 为何 Pi 上 avrdude 写失败；烧录只走 Windows |
| 44 | USB Pitfall — Data Port vs POWER Port | 🟨 INSIGHT | `RE-I19` | LOAD-BEARING | 接错过一次；写进卡 |
| 45 | Wire Light (A0) | 🟩 MAKING | `RE-M13` | SUPPORTING | 光敏电阻；后续换 BH1750 的诚实说明 |
| 46 | Wire Moisture (A1) — First Sensor Was Dead | 🟩 MAKING | `RE-M14` | DONE | 换新探头；空气 0–4 / 泡水 350–370 标定 |
| 47 | Wire Sound (A2) — Peak-to-Peak, Not One analogRead | 🟩 MAKING | `RE-M15` | SUPPORTING | MAX4466；采样策略 |
| 48 | Wire BMP280 / DHT — Overlap and What Stays | 🟩 MAKING | `RE-M16` | RUNNING | 与 BME680 方案差异；去留决策 |
| 49 | Wire EC (A7) — Default Formula, Not Calibrated Yet | 🟩 MAKING | `RE-M17` | RUNNING | 诚实：未用标准液标定 |
| 50 | Pause pH (A6) — Planned, Not Wired | 🟩 MAKING | `RE-M18` | RUNNING | 范围诚实；别假装接了 |
| 51 | Remove PIR — Wrong Product Question | 🟨 INSIGHT | `RE-I20` | LOAD-BEARING | 陪伴型残留传感器被拿掉；接 I1 |
| 52 | Sensor Connection Test — First Live Packet | 🟩 MAKING | `RE-M19` | SUPPORTING | **已有**总测；指回 M13–M18 |
| 53 | Firmware on Uno — Sample, Pack, Send, Sleep | 🟩 MAKING | `RE-M20` | LOAD-BEARING | `.ino`；与野生型「当下长度」呼应但周期可不同 |
| 54 | Pin Map Card — Occupied Pins at a Glance | ⬜ CONTEXT | `RE-S5` | SUPPORTING | 挂硬件接线现状报告表格 |

---

### G · 树莓派、软件与表达（12）

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 55 | Flash & Boot Raspberry Pi 4B | 🟩 MAKING | `RE-M21` | SUPPORTING | **已有**；SSH / hostname；改弱密码待办 |
| 56 | Pi ← USB → Arduino — First End-to-End Read | 🟩 MAKING | `RE-M22` | LOAD-BEARING | 读到 JSON；mode=live |
| 57 | Port CfC + AutoNCP Onto the Device | 🟩 MAKING | `RE-M23` | LOAD-BEARING | Investigate 核原样复用；不重训装懂 |
| 58 | Implement Sensory Weighting Transform | 🟩 MAKING | `RE-M24` | LOAD-BEARING | comfort × genome → CfC 输入 |
| 59 | Genome Switch = Load a JSON File | 🟩 MAKING | `RE-M25` | LOAD-BEARING | 变色龙工程实现 |
| 60 | Auto-Calibration Window — Newborn Learns Comfort | 🟩 MAKING | `RE-M26` | LOAD-BEARING | 接 Q4；部署初期观察 |
| 61 | LED Expression Driver — Breath at ~4.5s | 🟩 MAKING | `RE-M27` | LOAD-BEARING | 5D→光；非言语硬线 |
| 62 | Optional Tone Only at Extremes — Never Speech | 🟨 INSIGHT | `RE-I21` | LOAD-BEARING | 为什么不用说话；田野无语言前提 |
| 63 | Local PWA / Journal on Wi-Fi | 🟩 MAKING | `RE-M28` | SUPPORTING | 作品集 demo；本地服务 |
| 64 | Designed Weights vs Emergent Dynamics — Architectural Separation | 🟨 INSIGHT | `RE-I22` | LOAD-BEARING | 回答 Q6；防答辩误读 |
| 65 | Smoke Test — All Channels + One Genome + Light | 🟩 MAKING | `RE-M29` | SUPPORTING | 集成冒烟 |
| 66 | Precedent: Interoceptive / Predictive Emotion Models | 🟪 PRECEDENT | `RE-C3` | SUPPORTING | 轻量引用，服务 I14 |

---

### H · 诱导演示与一手证据（6）

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 67 | Induced Event Protocol — What Counts as a Demo | 🟨 INSIGHT | `RE-I23` | LOAD-BEARING | 五周内可证伪的演示规则 |
| 68 | Demo: Artificial Drought (Soil Genome) | 🟧 PRIMARY | `RE-P1` | LOAD-BEARING | 过程+光反应+日志片段 |
| 69 | Demo: Sudden Temperature Shift | 🟧 PRIMARY | `RE-P2` | LOAD-BEARING | 同上 |
| 70 | Demo: Genome Switch Mid-Session | 🟧 PRIMARY | `RE-P3` | LOAD-BEARING | 同硬件换 JSON，反应重定向 |
| 71 | What the Demo Does Not Prove | 🟨 INSIGHT | `RE-I24` | LOAD-BEARING | 慢趋势、全域环境、真涌现学习 |
| 72 | If Someone Stands Next to It — Informal Reading | 🟧 PRIMARY | `RE-P4` | SUPPORTING | 可选：无仪表盘时别人怎么读光 |

---

### I · 作品集产出与收尾（约 6–8，把总数压在 ~70）

| # | 标题 | TYPE | ID | STATUS | 写什么 |
|---|---|---|---|---|---|
| 73 | Portfolio: Product Design Deck (1920×1078) | 🟩 MAKING | `RE-M30` | DONE | 7 页 HTML/SVG；挂文件 |
| 74 | Portfolio: App Showcase / PWA Screens | 🟩 MAKING | `RE-M31` | DONE | demo.html / showcase |
| 75 | Portfolio: Field Personas → Product Implications | 🟨 INSIGHT | `RE-I25` | LOAD-BEARING | 田野人物如何约束表达层 |
| 76 | One Continuous Question Across Investigate and Realise | 🟨 INSIGHT | `RE-I26` | LOAD-BEARING | 收束到 Positioning；接 AL-Q 链 |
| 77 | What I Would Do With More Time | 🟨 INSIGHT | `RE-I27` | SUPPORTING | 长时部署、pH、真标定、BH1750 |
| 78 | Closing — Translation Medium, Not Companion Pet | 🟨 INSIGHT | `RE-I28` | LOAD-BEARING | 最后一张；一句话站位 |

> 若必须严格 **70**：合并 37+40，或砍 C2/C3/P4；若到 **72** 也可（Investigate 本身也不卡死整数）。

---

## 4. 写法抽样（照抄结构，换内容）

### 例 A · MAKING（成功失败都要）

**Title:** Arduino USB-C Case — Five Failures, Sixth Fits  
**TYPE:** 🟩 MAKING｜**ID:** `RE-M8`｜**STATUS:** DONE  

**File:** `uno_case_v6.stl`  
**What was done:** Printed five enclosure versions for the Uno R3 USB-C board; none seated. Sixth version cleared the connector and screw bosses.  
**Why:** The board must live inside the egg without stressing the only data+power USB-C port.  
**What it means:** Fit is not a cosmetic problem — a bad case is a future intermittent disconnect that will look like a software bug. Recording five failures keeps the build from looking cleaner than it was.

### 例 B · INSIGHT（改主意）

**Title:** Clock Source Must Be 16MHz — The Flash Failure That Wasn't the Cable  
**TYPE:** 🟨 INSIGHT｜**ID:** `RE-I17`｜**STATUS:** LOAD-BEARING  

正文结构：症状 → 排除了什么（线/口/供电）→ 真正原因（外部 16M 晶振 / 默认 32M）→ **意味着什么**（文档里伪装成硬件玄学的问题，其实是一个设置）。

### 例 C · QUESTION（脊骨）

**Title:** When light breathes, is that emergence or design?  
**TYPE:** 🟦 QUESTION｜**ID:** `RE-Q6`｜**STATUS:** LOAD-BEARING  

正文：为什么答辩官会误读 → 你怎么在架构上切开两层 → 指向 `RE-I22` / `RE-I3`。

---

## 5. 两周冲刺建议（按优先级写）

**Week A — 论证先立住（评委先读这些）**  
`RE-S1` → `RE-Q1…Q6` → `RE-I0,I1,I5,I3,I22,I26` → 把已有 Overview/Pivot/Boundaries 补上 ID 色块  

**Week B — 造物可见**  
`RE-M8,I17,I18,I19,M14,M20,M22–M27` → `RE-P1–P3` → 作品集挂载 `M30/M31`  

**可后补 SUPPORTING**  
单传感器接线细卡、先例卡、Anatomy、heatsink 待办  

---

## 6. 和 Investigate 对齐的检查清单

- [ ] 每张卡都有 TYPE 色 + DATE + ID + STATUS  
- [ ] MAKING 用四行结构；INSIGHT 不写成「今天接了线」日志  
- [ ] 失败 / 暂停 / 未标定写进卡（pH 未接、EC 未标定、光敏待换 BH1750）  
- [ ] 交叉引用 Investigate：`AL-Q7`, `AL-I19`, `AL-P*`, CfC/`AL-I1`  
- [ ] AI 协助披露（接线示意图、设计文档）——与田野仪器披露同标准  
- [ ] 不把「设计的加权规则」写成「网络自己学会的生态行为」  

---

## 7. 下一步我可以继续帮你做的

1. **按本表直接写英文正文**（一次 10 张，可粘贴 Padlet）  
2. **只写 Week A 的 Q+I 脊骨**（最影响评分）  
3. **把你已有 12 张粗卡改成 Investigate 体例终稿**  

你回我选 1 / 2 / 3，或指定从哪一段 ID 开始写。
