# Plan A 培育型 · 补漏帖 + 收尾 + 方法论反思（可直接粘贴 Padlet）

> 这些是 **Step 14「备份重启并验证」之后**才补上、但之前忘了写进博客的工作。
> 阅读顺序：**接在 Step 14（AL-M16）之后、Plan B 野生型之前**。
> 每帖含：标签行（TYPE / ID / STATUS）+ 中文 + English。文件附件按标注挂。
>
> ⚠ 插入这几张会把野生型的号往后推（见文件末尾「ID 重排说明」）。

---

## Step 15 · 把「感知→情绪」补成完整闭环：反馈/表达子系统
### Step 15 · Closing the perception→emotion loop: the feedback / expression subsystem

**TYPE:** 🟩 MAKING ｜ **ID:** `AL-M17` ｜ **STATUS:** LOAD-BEARING ｜ **FILE:** `feedback_v2.py`

**中文**
之前的系统只做到「感知→情绪」半闭环：它能*感觉*，但对外什么都不*表达*，也不会*长成一个人*。Step 14 重启验证跑通后，我补了 `feedback_v2.py`，把回路补成「感知→情绪→反馈→（影响世界）」，拆成四个部件：
1. **阶段性性格**（依恋 5 维）——在先天气质底子上被经历慢慢塑造；
2. **语言习得**——从世界叙事里接触词汇、随发育阶段推进；
3. **心理反馈**——每一帧都产出一条「内心状态」实时输出；
4. **行为反馈**——只有指标越阈值才触发一个具身行为。
关键取舍：这四样都是**慢变量 + 阈值触发**，不是「每帧都表演」。我要的是「它大部分时候只是安静地活着，偶尔才说/做点什么」，而不是一个话痨。

**English**
The old system only closed half the loop — *perception→emotion*. It could *feel* but never *express*, and never *grew into someone*. After Step 14's clean restart verified, I added `feedback_v2.py` to complete *perception→emotion→feedback→(acts on world)*, in four parts: (1) a **staged personality** (5 attachment dimensions) slowly shaped by experience on top of innate temperament; (2) **language acquisition** picking up words from the world's narrative as development advances; (3) a **psyche readout** emitting one line of inner state every frame; (4) **behavior feedback** that fires an embodied action only when metrics cross a threshold. Key trade-off: all four are **slow variables + threshold-triggered**, not "perform every frame" — I wanted something that mostly just *lives quietly* and only occasionally says or does something.

---

## Step 16 · 5 维依恋性格：先天气质 vs 后天性格
### Step 16 · Five-dimensional attachment personality: innate temperament vs. grown character

**TYPE:** 🟩 MAKING ｜ **ID:** `AL-M18` ｜ **STATUS:** LOAD-BEARING

**中文**
性格不是一开始就设死的。我区分了**气质**（GENOME 里的生物基线，不变）和**性格**（气质 + 经历，会长）——依据 Thomas & Chess 的气质理论。性格是 5 个 0~1 的维度：**安全依恋 / 探索勇气 / 情绪调节 / 社会信任 / 挫折耐受**（Bowlby、Ainsworth 依恋理论）。
机制：从气质映射出**起点**（如受惊恢复慢→情绪调节起点低），然后每帧以极小步长（LR=0.0006）被经历塑造——安全+连接高→安全依恋涨，长期分离→安全依恋降……每个发育阶段结算一次「性格快照」。步长故意设得很小：性格是慢变量，要长期一致的经历才改得动，不能一惊一乍。
性格还**反过来调制**表达：安全依恋 <0.4 时，它说话会更退缩试探。

**English**
Personality isn't hard-set from birth. I separated **temperament** (the biological baseline in the GENOME — fixed) from **character** (temperament + experience — it grows), following Thomas & Chess. Character is five 0–1 dimensions: **secure attachment / exploration courage / emotion regulation / social trust / frustration tolerance** (Bowlby, Ainsworth). Temperament sets the *starting point* (e.g. slow fright-recovery → low initial emotion regulation), then each frame nudges it by a tiny step (LR=0.0006): safety+connection high → secure attachment rises; prolonged separation → it falls; a "character snapshot" is settled at each developmental stage. The step is deliberately tiny — character is a slow variable that only shifts under consistent long-term experience. Character also *feeds back* onto expression: below 0.4 secure attachment, it speaks more hesitantly.

---

## Step 17 · 语言习得：从「听到」到「会用」
### Step 17 · Language acquisition: from "hearing" to "using"

**TYPE:** 🟩 MAKING ｜ **ID:** `AL-M19` ｜ **STATUS:** LOAD-BEARING

**中文**
语言不是开关，是**曲线**。我建了一个分 8 档的词库（约 250+ 词），对应儿童语言发展的典型顺序：称呼/需求叠字 → 感官状态 → 家人物体 → 食物动物 → 动词 → 形容/情绪 → 时间地点 → 抽象心理。
习得机制两条：**日常耳濡目染**（环境暴露的微小基础增量）+ **叙事 grounding**（在世界叙事里「亲耳听到」某词时额外加速，符号落地学得更快）。情境越有意义（连接高/情绪强），词记得越牢。每档按发育进度解锁，续跑时会按当前年龄**预置**一批「本该已习得」的早期词，不必从零重学。
表达阶段随发育推进：前语言（纯感受基调+拟声）→ 咿呀单词 → 电报句 → 简单句 → 复杂句（Brown 1973）。
> 说明：这是「随年龄增长的**代表性**可用词曲线」，不是真实 6 岁几千词的全量计量——早期档已含全部内心独白所需词，保证任何阶段表达都可用。

**English**
Language isn't a switch, it's a **curve**. I built an 8-tier lexicon (~250+ words) following the typical order of child language development: address/need reduplications → sensory states → family & objects → food & animals → verbs → adjectives/emotions → time & place → abstract/psychological. Two acquisition channels: **ambient exposure** (a tiny baseline gain) + **narrative grounding** (an extra boost when a word is actually "heard" in the world's narrative — grounded words are learned faster). The more meaningful the context (high connection / strong emotion), the better a word sticks. Tiers unlock by developmental progress; on resume it *pre-seeds* early words that "should already be known" for its current age. Expression advances through stages: prelinguistic (pure bodily tone + vocalizations) → babbling → telegraphic → simple → complex sentences (Brown 1973).
> Note: this is a *representative* usable-vocabulary curve that grows with age, not a full count of the thousands of words a real 6-year-old has — early tiers already contain every word the inner monologue needs, so expression is usable at any stage.

---

## Step 18 · 心理独白 + 具身行为：让内在被看见
### Step 18 · Psyche readout + embodied behavior: making the inner life legible

**TYPE:** 🟩 MAKING ｜ **ID:** `AL-M20` ｜ **STATUS:** LOAD-BEARING

**中文**
两件事让「它在想什么」变得可读：
- **心理反馈（PsycheReadout）**：每一帧把（情绪+身体+性格+语言水平）渲染成一句内心状态。措辞受语言阶段控制——前语言期是「〔哇——〕一阵尖锐的紧」这种身体感受基调，到复杂句期才会是「身体里有个地方一直在疼，我需要有人来帮我。」先有 7 种「感受意图」（求安慰/好奇探索/警觉/被淹没/连接喜悦…），再按语言水平语言化。
- **行为反馈（BehaviorSelector）**：12 种具身行为（哭闹/吮手自我安抚/伸手去够/转头寻声/僵住…），**不是每帧都动**，只有情绪+身体预算越阈值才触发，且带 6 帧不应期防止连帧重复。行为也受性格调制：情绪调节高才会自我安抚，探索勇气高才会伸手去够。

**English**
Two things make "what it's thinking" legible:
- **PsycheReadout**: each frame renders (emotion + body + personality + language level) into one line of inner state. Wording is gated by language stage — prelinguistic is a bodily tone like "〔waah—〕a sharp clench," and only at the complex-sentence stage does it become "There's a place inside my body that keeps hurting; I need someone to help me." Seven "feeling intents" (seek-comfort / curious-explore / wary / overwhelmed / joy-connect…) come first, then get verbalized to the current language level.
- **BehaviorSelector**: 12 embodied behaviors (crying, fist-sucking self-soothe, reaching, turning to sound, freezing…) that *don't* fire every frame — only when emotion + body budget cross a threshold, with a 6-frame refractory period to avoid repeats. Behavior is personality-modulated too: it self-soothes only with high emotion regulation, and reaches out only with high exploration courage.

---

## Step 19 · 多主体「活世界」：照顾者从提线木偶升级为有内部状态的主体
### Step 19 · A multi-agent living world: caregivers become subjects with internal state, not puppets

**TYPE:** 🟩 MAKING ｜ **ID:** `AL-M21` ｜ **STATUS:** LOAD-BEARING ｜ **FILE:** `npc_agents.py`

**中文**
最大的一次补充。之前 NPC 是「LLM 编剧凭空即兴决定母亲这一刻理不理婴儿」——不可控、不一致。我把每个照顾者建成**有内部状态、随时间/事件演化的主体**：
- **母亲 陈若筠**（主照顾者，完整建模）：疲惫/耐心/焦虑/情绪/摩擦余波/脆弱时刻，还带睡眠债（含「越累越强制微睡眠」的现实上限）、生理期周期、婆媳摩擦衰减。每帧基于人设 + 状态 + 感知到的婴儿行为，产出：**是否意识到**婴儿需求（响亮哭闹高觉察、隐性情感需求低觉察=劣势 Fe）、**是否会回应**（焦虑-回避型：先观察）、**回应质量**、以及**内心活动**。
- 父亲（工作日晚上在场）、外婆（仅周六，「一哭就抱」的旧观念，和母亲育儿观冲突）。
关键设计：这个 appraisal 作为**强约束注入编剧 LLM**——「若某照顾者没意识到/不会回应，就不要让 TA 恰好安抚到婴儿」。状态演化全用规则（零额外 LLM 调用）。
**最重要的原则：不根据结果反向调控成长。** 婴儿连接上不去若是母亲人设的必然后果，那就让它上不去，判断标准是「反应符不符合人设」，而非「结果好不好」。
> ⚠ 这条原则挡住了「事后按结果调参」的作弊，但**没**挡住「先验偏置」——见 `AL-I6` 反思。

**English**
The biggest addition. NPCs used to be "an LLM playwright improvising, out of nowhere, whether the mother attends to the baby this moment" — uncontrollable and inconsistent. I rebuilt each caregiver as a **subject with internal state that evolves over time/events**:
- **Mother 陈若筠** (primary caregiver, fully modeled): fatigue / patience / anxiety / mood / friction / vulnerable moments, plus sleep debt (with a realistic ceiling where "the more exhausted, the more forced micro-sleep"), a menstrual cycle, and decaying in-law friction. Each frame, from persona + state + perceived infant behavior, she outputs: **whether she notices** the need (high awareness of loud crying, low awareness of implicit emotional needs = inferior Fe), **whether she'll respond** (anxious-avoidant: observe first), **response quality**, and **inner monologue**.
- Father (present weekday evenings), Grandmother (Saturdays only, old "pick him up the moment he cries" view that clashes with the mother's).
Key design: this appraisal is injected as a **hard constraint into the playwright LLM** — "if a caregiver didn't notice / won't respond, don't let them happen to soothe the baby." State evolution is all rule-based (zero extra LLM calls).
**The most important principle: never reverse-engineer growth from outcomes.** If the infant's connection can't rise because that's the necessary consequence of the mother's persona, then let it stay low. The criterion is "does the reaction fit the persona," not "is the outcome good."
> ⚠ This principle blocks *post-hoc outcome tuning* cheating — but it does **not** block *prior bias*. See reflection `AL-I6`.

---

## 收尾 · 培育型跑到 2 岁的终态读数（带保留意见）
### Closing · Final-state readout of the nurtured run at age 2 (with caveats)

**TYPE:** 🟨 INSIGHT ｜ **ID:** `AL-I5` ｜ **STATUS:** RUNNING ｜ **FILE:** `growth_status.json`

**中文**
干净重跑到虚拟 **2 岁 0 月龄（dev_progress 100%，成熟期）** 时的最终状态：
- **语言**：复杂句阶段，可用词汇 **282**。最后一句内心独白：「身体里有个地方一直在疼，我需要有人来帮我。」
- **性格 5 维**：探索勇气 0.611、情绪调节 0.545、**安全依恋 0.0、社会信任 0.0、挫折耐受 0.0**。
- **情绪终态**：效价 −35、唤醒 73、安全 59、连接 **26.9**、分离阶段 **3（最大）**。
- **母亲终态**：耐心 0.07、焦虑 0.72、情绪 −0.97、摩擦 0.99；本回合**未觉察**婴儿需求、不会回应。

**我不打算把这个当成一个「发现」，理由写在下一张卡（`AL-I6`）。** 这里只做两点技术备注：
1. 三个维度**精确归零**（撞 `_clip01` 地板），而不依赖连接的两维存活——这更像**度量退化/地板伪影**，不是「养出了一个具体的人」。
2. 状态标 RUNNING 而非结束：仍有未解 bug + 归零可能是测量假象，不构成定论。

**English**
Final state of the clean rerun at virtual **age 2y0m (dev_progress 100%, maturity)**:
- **Language**: complex-sentence stage, usable vocab **282**. Last inner monologue: "There's a place inside my body that keeps hurting; I need someone to help me."
- **Personality (5 dims)**: exploration courage 0.611, emotion regulation 0.545, **secure attachment 0.0, social trust 0.0, frustration tolerance 0.0**.
- **Emotion**: valence −35, arousal 73, safety 59, connection **26.9**, separation phase **3 (max)**.
- **Mother**: patience 0.07, anxiety 0.72, mood −0.97, friction 0.99; this turn she **did not notice** the need and won't respond.

**I'm deliberately not treating this as a "finding" — the reason is in the next card (`AL-I6`).** Two technical notes only: (1) three dimensions hit **exactly zero** (clipped to the floor) while the two that don't depend on connection survived — that looks more like **metric degeneration / a floor artifact** than "a specific person grew." (2) Marked RUNNING, not finished: unresolved bugs remain and the zeros may be a measurement artifact, so this is not a verdict.

---

## 反思 · 「这个结论是被设定的」：论引导性养育者与如何规避
### Reflection · "The conclusion was baked in": on a leading caregiver prompt, and how to avoid it

**TYPE:** 🟨 INSIGHT ｜ **ID:** `AL-I6` ｜ **STATUS:** LOAD-BEARING

**中文**
上一张卡里「学会了语言、却没养出安全感」——**这句话是废话**，因为结论是我亲手设定的，不是涌现的。三条证据：
1. **母亲人设本身就是不安全依恋的教科书成因**：焦虑-回避型、延迟响应、劣势 Fe（觉察不到情感需求）。依恋理论里这几条正是制造回避型依恋的「因」。
2. **性格更新规则又把「果」写死**：安全依恋只在「安全+连接高」时涨、分离时降。母亲极少响应情感需求→连接常年 <45→加分支几乎不触发；分离阶段=3→天天扣分。结论是从（人设）+（规则）里**演绎**出来的，而两者都出自同一套理论。这是套套逻辑，不是检验。
3. **冒烟枪**：三维精确归零、不挂靠连接的两维存活——「性格」退化成了确定性函数。

**我做对的一半**：代码里明写「不根据结果反向调控成长」，这防住了事后调参作弊。**但它防不住先验偏置**——我挑了一个注定产出不安全感的母亲，配一套把她的行为直接翻译成「不安全」分数的尺子。

**如何规避（下一版要这么做）：**
1. **别让同一套理论既写世界又写尺子**：照顾者只给底层机械参数（响应延迟/频率/质量），依恋分从交互历史用独立度量反推。
2. **照顾者当成实验条件的光谱**：≥3–4 种原型（安全-响应/焦虑-回避/忽冷忽热/一哭就抱），结论从「一个点」变成「安全度随响应性的梯度」——梯度才是结果。
3. **每条件多种子（N>1）**，报分布而非一条轨迹。
4. **预注册 + 盲化/随机气质**，在看结果前定好参数。
5. **测你没写进规则的东西**：用分离后是否主动寻求靠近（类 Strange Situation 探针）这类**行为**标记，而不是直接读你一帧帧加出来的标量。
6. **改口径**：这不是「AI 能否产生依恋」的实证，而是**设计虚构/一致性模拟**——「把理论 T 编译进规则+人设后，装置复现了 T 的预测轨迹」。价值在装置与问题本身。

**English**
On the previous card, "it learned language but never grew secure" — **that sentence is trivial**, because I authored the conclusion; it did not emerge. Three pieces of evidence: (1) The mother's persona is itself a textbook *cause* of insecure attachment (anxious-avoidant, delayed response, inferior Fe / blind to emotional needs). (2) The personality update rule then hard-codes the *effect*: secure attachment rises only when safety+connection are high and falls under separation; the mother rarely meets emotional needs → connection stays <45 → the "+" branch almost never fires; separation phase = 3 → it's debited every frame. The conclusion is *deduced* from (persona)+(rule), both written from the same theory — a tautology, not a test. (3) Smoking gun: three dimensions hit exactly zero while the two not tied to connection survived — "personality" degenerated into a deterministic function.

**The half I got right**: the code explicitly forbids "reverse-engineering growth from outcomes," which blocks post-hoc tuning. **But it can't block prior bias** — I hand-picked a mother destined to produce insecurity, paired with a ruler that translates her behavior directly into an "insecurity" score.

**How to avoid it (next version):** (1) Don't let one theory write both the world and the ruler — give caregivers only low-level mechanical params (response delay/frequency/quality) and derive attachment from interaction history via an independent measure. (2) Treat caregivers as a *spectrum of conditions* (≥3–4 archetypes: responsive-secure / anxious-avoidant / inconsistent / over-responsive) so the result becomes a *gradient* of security vs. responsiveness, not a single foregone point. (3) Multiple seeds per condition (N>1); report distributions. (4) Pre-register + blind/randomize temperament before seeing outcomes. (5) Measure what you *didn't* write into the rules — behavioral markers like proximity-seeking after separation (a Strange-Situation-style probe), not the scalar you incremented yourself. (6) Reframe the claim: this is not evidence about "can AI attach," it's **design fiction / a consistency simulation** — "compile theory T into rules+persona and the apparatus reproduces T's predicted trajectory." The value is the apparatus and the questions.

---

## ID 重排说明（插入这几张之后）

**新增 7 张**，插在 Step 14（`AL-M16`）之后、Plan B 野生型之前：

| 顺序 | 帖子 | TYPE | ID |
|---|---|---|---|
| … | Step 14: Back Up and Restart（已存在） | 🟩 MAKING | `AL-M16` |
| 新 | Step 15: 反馈子系统 | 🟩 MAKING | `AL-M17` |
| 新 | Step 16: 5 维依恋性格 | 🟩 MAKING | `AL-M18` |
| 新 | Step 17: 语言习得 | 🟩 MAKING | `AL-M19` |
| 新 | Step 18: 心理独白+具身行为 | 🟩 MAKING | `AL-M20` |
| 新 | Step 19: 多主体活世界 | 🟩 MAKING | `AL-M21` |
| 新 | 收尾终态读数 | 🟨 INSIGHT | `AL-I5` |
| 新 | 方法论反思 | 🟨 INSIGHT | `AL-I6` |

**因此野生型（Plan B）整体往后推：**
- 原 `AL-I5`→`AL-I7`、`AL-I6`→`AL-I8`、`AL-I7`→`AL-I9`、`AL-I8`→`AL-I10`、`AL-I9`→`AL-I11`
- 原 `AL-M17`（野生型 Step3 新模块）→ `AL-M22`；若 `symbol_tracker` 单列则 `AL-M18`→`AL-M23`

> 我可以把这套新编号 + 野生型顺延**一起并进 `_rebuild_tags.py`**，等你关掉 `padlet_card_tags.xlsx` 后一次性写入。需要的话说一声。
