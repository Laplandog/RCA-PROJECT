# AI 交接文档 · A/B 实验 → Realise 产品 → Padlet

> **用途**：把 Zixun（RCA Graduate Diploma · 目标申请 IDE）从双轨实验到 Realise 造物、再到 Padlet 写作协作的全程交给下一任 AI。  
> **仓库根目录**：`C:\Users\ZQQ\OneDrive\Desktop\IDE\RCA-graduate-diploma U3-U4 project`  
> **用户语言**：默认用**简体中文**回复；Padlet / 作品集交付物正文多为**英文**。  
> **用户身份与总目标**：见根目录 `AGENTS.md` —— 辅助完成 U3/U4，并支撑申请 IDE。

---

## 0. 30 秒读懂项目

| 阶段 | 名字 | 在争什么 |
|---|---|---|
| Investigate | AI Life 双轨实验 + 田野 + 理论 | 持续传感 / 记忆 / 时间下，系统能否长出**未经设计的行为与可读状态**（ALife 内部状态定义，不碰意识玄学） |
| 转向 | 陪伴玩具 → 生态转译 | 田野问的不是「好不好摸」，而是**没有仪表盘如何读懂生命系统**；拒电子宠物（与 Unit 2 ADHD 玩具撞题） |
| Realise | 物理对象 **ANIMA** | 同一套硬件 +「物种基因组」权重表，把土壤/水/气压力转成光/呼吸等非言语表达；**陪伴是副产品不是目标** |

技术栈一句话：Arduino 采多路环境传感器 → USB 串口 JSON → Raspberry Pi 4B 上 **CfC + AutoNCP** → 5 维情绪 → LED 表达；基因组 = JSON 通道权重表（非换板）。

---

## 1. 关键命名与易混点（交接必读）

### 1.1 Plan A / Plan B 曾对调 —— 以 Investigate 定稿为准

项目里出现过两套叫法，**下一任 AI 写文前先核对 Investigate Padlet 定稿**：

| 来源 | 说法 |
|---|---|
| 早期 Realise Overview PDF | Plan A = Wild Type；Plan B = Nurtured |
| Investigate 标签整理 `PADLET_U3_AILIFE_tags_ordered.md` | **培育型 = Nurtured（原常称 Plan B）**；**野生型 = Wild Type（原常称 Plan A）**；并注明要把错标的 Experiment B 改成 A |

**稳妥写法**：正文尽量用 **Nurtured / Wild Type**，少写裸「Plan A/B」；若必须写字母，跟用户确认当前 Padlet 上的最终标签。

### 1.2 野生型实验 ≠ Realise 蛋

- 野生型：实验阶段；传感板曾用**仿真数据**（日志 `"mode": "sim"`），不是最终蛋形产品。  
- Realise 蛋：产品线；七通道生态传感 + Pi/Uno + 外壳 + 基因组切换。  
- 野生型传感器选型逻辑（便宜/入门）与产品七通道清单**不要混为一谈**。

### 1.3 诚实边界（写 Realise 时禁止夸大）

1. 五周内只诚实演示**短时诱导事件**（人工干旱、突变温），不声称证明慢生态趋势。  
2. **感官加权规则 = 设计**；不可把设计说成 CfC「学会了生态」。架构上要分开加权层与 CfC 时序动态。  
3. 单点探头 ≠ 整片环境状态。  
4. 硬件欠债要写进卡：pH 曾暂停未接、EC 未精确标定、光敏电阻待换 BH1750、BMP280 vs BME680 去留等（见 `硬件接线现状报告.md`）。

---

## 2. Investigate：A/B（双轨）实验做了什么

### 2.1 结构（Padlet 阅读指南已定）

完整 Investigate：`Padlet - ZIXUN - Investigate BloG.pdf`（约 71 页，会更新）。

四个字段：**TYPE / DATE / ID / STATUS**。

运动线：

1. **BAZI-** — 放弃方向（DEAD END，刻意保留）  
2. **RP-** — Tavern 迂回，交出方法  
3. **AL-** — AI Life 主线  
   - `AL-Q1→Q7` 问题脊骨  
   - `AL-R` Nisioti 精读；`AL-C` 引用  
   - `AL-I` 洞察；`AL-P` 田野；`AL-M` 造物；`AL-S` 总览  
   - MAKING：`M1–M24` 培育型；`M25–M36` 野生型（以用户 Padlet 实际编号为准）  
4. **PR-** 作品集反思；**RE-** 预告 Realise（Movement 4）

标签清理备忘：`PADLET_U3_AILIFE_tags_ordered.md`  
培育型补漏：`PADLET_U3_nurtured_supplement_and_reflection.md`  
野生型流水账（File / What / Why / What it means）：`PADLET_U3_wildtype_real_process.md`  
野生型附件：`padlet_wildtype_attachments/`

### 2.2 双轨对比意图

| | Nurtured（培育型） | Wild Type（野生型） |
|---|---|---|
| 社会输入 | LLM 作世界/照顾者 | 无 LLM；传感（或仿真）驱动 |
| 问题 | 社会经验塑造什么 | 无语言社会化时内部结构能否自组织 |
| 共享核 | 同系 CfC + AutoNCP、5D 情绪等（控制变量叙事） | 同左 |

野生型关键诚实点：仿真世界、崩溃重启接缝、时长对齐偏差、符号分数曾奖励「冻结系统」——详见野生型 Padlet 文与 `AL-I1x` 系列。

### 2.3 田野

- 仪器与披露：`AL-P0`；参与者记录 `AL-P1`–`P4`（约 5 人，含 Z）。  
- 原始材料夹（用户机）：`C:\Users\ZQQ\OneDrive\Desktop\IDE\u3田野调研`  
- 英文整理：`U3_FIELD_RESEARCH_5_PARTICIPANTS_EN.md`  
- 人物画像 HTML（中/英 1080p）：在 `u3田野调研` 与作品集流程中生成过 `user_personas.html` / `user_personas_1080p_en.html`

田野逼出的产品命题：无仪表盘的**可读性**，不是宠物依恋（Realise `RE-Q1` / `RE-I6`）。

### 2.4 拒陪伴路线

`AL-I19` Hardware Decision Log：拒 Tamagotchi 式陪伴（撞 Unit 2 + 答错田野问题）→ Realise「生态环境情感化转译」。

---

## 3. Realise：从实验到物体

### 3.1 产品定位（定稿语言）

- 名：**ANIMA / A Living Presence**  
- 角色：翻译媒介，不是被爱对象  
- 机制：七通道传感 × 物种基因组权重 × CfC → 光/呼吸等  
- 变色龙：换 JSON 基因组，不换主板（土壤/淡水/室内空气）

### 3.2 关键技术文档（先读这些再改代码）

| 文件 | 内容 |
|---|---|
| `SERIAL_PROTOCOL.md` | Arduino→Pi：一行 JSON、`115200`、缺传感器则省略 key |
| `硬件接线现状报告.md` | 引脚、LGT8F328P、**Clock Source 必须 16MHz**、Pi 只读串口、标定状态 |
| `基因组预设与传感器推理设计.md` | 三基因组 + 推理逻辑 |
| `感官加权系统技术设计文档.md` | comfort × genome 两层加权 |
| `arduino/sensor_node/sensor_node.ino` | 传感固件 |
| `genomes/tomato_soil.json` · `freshwater.json` · `indoor_air.json` | 基因组预设 |

硬件坑（写 Padlet 时是强 INSIGHT）：

- IDE Clock Source **16MHz**（不是默认 32MHz）→ 对应草稿 `RE-I17`  
- 板子是 **LGT8F328P**，不是真 ATmega328P；烧录走 Windows → `RE-I18`  
- USB：**数据口** vs 仅 POWER 口 → 计划 `RE-I19`

### 3.3 作品集 / 演示（portfolio）

目录：`portfolio/`

| 产物 | 说明 |
|---|---|
| `demo.html` | 离线 PWA 演示 |
| `showcase.html` | 展示壳 |
| `app_showcase.svg` | 手机框 App 截图拼贴 |
| `product_design.html` | 产品设计长页 |
| `product_design_1080p.html` | 1920×1078 分页 deck（后来用户要拆文件） |
| `pd_page1_cover.html` … `pd_page7_*.html` | **每屏一个 HTML**（为粘贴体积） |
| `pd_page1_cover.svg` … `pd_page7_*.svg` | **原生矢量 SVG**（用户最终要贴进 Figma 的格式） |
| `RE-S3_inheritance_map.png` | 继承表图（Padlet 不爱 Markdown 表） |

用户约束（Figma）：一口气粘贴代码有上限 → **每页独立文件**；要的是**原生 SVG**，不是整页 HTML。

---

## 4. Padlet 协作：规则、进度、文件地图

### 4.1 两个 Padlet

| Padlet | PDF（根目录，会更新） | 状态 |
|---|---|---|
| Investigate | `Padlet - ZIXUN - Investigate BloG.pdf` | 用户称已写完（以最新 PDF 为准） |
| Realise | `Padlet - ZIXUN - Realise Blog.pdf` | 进行中；早期只有 Overview/Pivot/边界 + 几张粗 MAKING |

Realise = Investigate 指南里的 **Movement 4，前缀 `RE-`**。

### 4.2 Realise 卡体例（必须遵守）

与 Investigate 相同四字段。MAKING：

```
File:
What was done:
Why:
What it means:
```

用户指定的**尾部格式**（Batch 2 起）：

```
**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I6
**Status** LOAD-BEARING
```

- TYPE 后空一行；颜色：⬜ CONTEXT · 🟧 PRIMARY · 🟨 INSIGHT · 🟩 MAKING · 🟦 QUESTION · 🟪 PRECEDENT  
- 无具名文献不要硬挂 🟪（`RE-C1` 已改成 `RE-I29`）  
- Padlet **讨厌宽 Markdown 表** → 改散文或出图  
- 每批可附 **ATTACH** 清单（给作者看，勿粘进正文）

### 4.3 大纲与批次文件

| 文件 | 作用 |
|---|---|
| `PADLET_Realise_outline_70.md` | ~70 篇总纲（块、ID、STATUS、写法） |
| `PADLET_Realise_batch1_EN.md` | 开篇 + Q1–Q6 + I0/I5/S1/S3（尾部格式旧版 DATE 在上，可统一） |
| `PADLET_Realise_batch2_EN.md` | 定位补强 + 架构 I6–I14 + I29（已校对） |
| `PADLET_Realise_batch3_EN.md` | 外壳造物开头 + 16MHz/LGT8/串口合同 + 附图指引 |
| `PADLET_Realise_sections_外观硬件软件.md` | **用户重排结构**：外观（蛋外）→ 硬件（蛋内）→ 软件（后写）。与 `outline_70` 并存；贴 Padlet 时以用户这版分区顺序为准，batch 正文按 ID 归位即可 |

### 4.4 进度快照（交接时点）

| 大纲块 | 状态 |
|---|---|
| 开篇桥接 | ✅ Batch1 + 用户已有 Overview→`RE-S2` |
| 问题脊骨 Q | ✅ `RE-Q1`–`Q6` |
| 定位 I | ✅ 用户 I1–I4 + Batch1 I5 + Batch2 I6–I8/I29 |
| 架构决策 | 🟡 论证 I9–I14 完；**欠**基因组 MAKING `RE-M2`–`M4` |
| 外壳造物 | 🟡 Batch3：`M1 I15 M5–M9` |
| 接线标定 | 🟡 Batch3：`I17 I18 M12`；**下批**应写 I19 + 逐传感器 M13–M20 |
| 软件表达 | ⬜ 未写（Pi、CfC 移植、LED、PWA…） |
| 诱导演示 | ⬜ 未写（P1–P3 + 不证明什么） |
| 作品集收尾 | ⬜ 未写 |

累计助手起草英文正文约 **30 张**（3×10）；用户 Padlet 上还有早期粗卡需**并入对应 RE-ID**，避免无号孤儿。

### 4.5 建议下一任立刻做的事

1. 读最新 `Padlet - ZIXUN - Realise Blog.pdf`，对齐用户已粘贴到哪一 ID。  
2. 写 **Batch 4**：`RE-I19`（USB 坑）+ `RE-M13`–`M20`（逐传感器/标定/固件）+ **`RE-M2`–`M4`（三基因组 JSON）**。  
3. 继续保持：英文正文、中文沟通、诚实边界、交叉引用 `AL-*`。  
4. 要附图时：对照 Batch3 的 ATTACH；协议卡挂 `SERIAL_PROTOCOL.md`；硬件坑挂 `硬件接线现状报告.md`。  
5. 用户说「继续 N」= 按下一批 Padlet 英文稿；说「检查」= 对事实/体例/过度宣称做审稿。

---

## 5. 时间线（协作过程压缩）

```mermaid
flowchart LR
  A[Investigate 双轨+田野] --> B[拒陪伴 / AL-I19]
  B --> C[Realise ANIMA 定位]
  C --> D[硬件接线+基因组文档]
  D --> E[作品集 HTML/SVG/PWA]
  E --> F[Investigate Padlet 定稿]
  F --> G[Realise Padlet 大纲~70]
  G --> H[Batch1 论证脊骨]
  H --> I[Batch2 架构]
  I --> J[Batch3 外壳+坑]
  J --> K[Batch4+ 待写]
```

对话中还做过（与 Padlet 并行）：

- App showcase SVG、人物画像 1080p、产品设计 7 屏 HTML→独立 HTML→原生 SVG  
- 继承表 `RE-S3` 出 PNG（用户要贴图）  
- 审 Batch2：去假 PRECEDENT、表改散文、Connection 映射去掉「对人打招呼」歧义  

---

## 6. 用户偏好（下一任别踩）

- 回复：**简体中文**；交付 Padlet/作品集：**英文**为主。  
- 不要主动 git commit / push（除非明确要求）。  
- 不要把滚动长网页硬塞进「一页粘贴」场景；要分页/拆文件/SVG。  
- 失败、暂停、未标定要写进博客（Investigate 气质）。  
- AI 协助（接线示意图、文档）要像田野仪器一样**披露**。  
- 问「你是啥 AI」时：按 Cursor 当前模型设定回答（本会话为 Cursor Grok 4.5；以实际系统提示为准）。

---

## 7. 快速文件索引

```
项目根/
  AGENTS.md
  SERIAL_PROTOCOL.md
  硬件接线现状报告.md
  基因组预设与传感器推理设计.md
  感官加权系统技术设计文档.md
  arduino/sensor_node/sensor_node.ino
  genomes/*.json
  portfolio/          # demo / showcase / pd_page* html+svg
  padlet_wildtype_attachments/
  PADLET_U3_*.md      # Investigate 侧整理
  PADLET_Realise_*.md # Realise 大纲与 batch 正文
  Padlet - ZIXUN - Investigate BloG.pdf
  Padlet - ZIXUN - Realise Blog.pdf

田野（仓库外）/
  C:\Users\ZQQ\OneDrive\Desktop\IDE\u3田野调研\
```

---

## 8. 给下一任 AI 的开场提示词（可复制）

```
你在交接 RCA GD 学生 Zixun 的 U3/U4 项目。
先读：项目根目录 HANDOFF_AB_experiment_to_Realise_Padlet.md（本文件）。
然后读：PADLET_Realise_outline_70.md + 最新 Realise Blog PDF + 硬件接线现状报告.md + SERIAL_PROTOCOL.md。
任务：按 Batch3 预告继续写 PADLET_Realise_batch4_EN.md（英文正文、指定尾部 TYPE 格式、每张附 ATTACH 指引）。
禁止：把设计加权说成涌现；混淆野生型仿真与 Realise 蛋；无引用却标 PRECEDENT。
沟通：中文；Padlet 正文：英文。
```

---

*文档生成目的：人→AI / AI→AI 交接。事实以用户最新 Padlet PDF 与仓库文件为准；若冲突，问用户一句再写。*
