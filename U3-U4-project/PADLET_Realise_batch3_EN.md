# Realise Padlet · Batch 3（白话修订 · 可直接粘贴）

> **写作规矩（本批起强制）**  
> - 读者：几乎不懂电子 / 编程的 RCA 老师  
> - 目的：让人看见**开放、会转弯、会承认失败**的思考过程——不是证明你很懂电路  
> - 禁止：堆型号、缩写、协议名；非写不可时，用「人话括号」一次性解释，然后别再炫  
> - 保留：横向对比（选项 A/B/C → 选了谁 → 扔掉谁）——对比才是思维链  

尾部格式照旧。

---

## 0. 进度（同前，不重复长表）

开篇 + 问题链 + 定位 ≈ 完成。  
本批 = **造物怎么选型、基因组怎么比着想**（白话版）。  
接线细节 / 软件 / 演示 = 还没写。

**本批 10 张：** `RE-M1` · `RE-I15` · `RE-I30` · `RE-M2` · `RE-M3` · `RE-M4` · `RE-M8` · `RE-M9` · `RE-I17` · `RE-I18`  

**⚠ 按你后来的三板块分法重新挂栏时：**  
- **蛋外面 APPEARANCE：** `RE-I15` · `RE-M8`（+ 待补 M5–M7）  
- **蛋里面 HARDWARE：** `RE-M1` · `RE-M9` · `RE-I30` · `RE-I17` · `RE-I18`  
- **软件 SOFTWARE：** `RE-M2` · `RE-M3` · `RE-M4`（基因组 = 注意力规则，不是焊出来的）  
详见 `PADLET_Realise_sections_外观硬件软件.md`。

---

## 1 · RE-M1

**Title:** Two Boxes, Not One — How I Split the “Brain” and the “Nerves”

**Body:**

**What I was deciding:**  
Who does the feeling math, and who does the touching of the world?

**Options I put side by side**

- **One computer for everything**  
  Smart enough for the “feeling” part, but clumsy at reading many cheap sensors at once. I would spend the whole month inventing adapters instead of making a thing.

- **One tiny board for everything**  
  Great at sensors. Too small to run the feeling system I already built in Investigate. I would have to throw that work away or hide it in the cloud.

- **A phone-like board that needs the internet**  
  Looks modern. Dies when Wi‑Fi dies. The object stops being a presence in the room and becomes a guest of the router.

- **Two boxes: a small board that only senses + a bigger board that only feels** ← **chosen**

**Why that leap:**  
Investigate already gave me a working “feeling engine.” Realise’s job is not to reinvent it. Realise’s job is to give it hands. Splitting the work lets each half stay honest.

**What this shows about my thinking:**  
I am willing to make the build look less “one elegant chip” if it protects the research story. Elegance that erases Investigate is fake progress.

**TYPE** 🟩 MAKING

**DATE** week 1
**ID** RE-M1
**Status** SUPPORTING

---

## 2 · RE-I15

**Title:** Why an Egg — I Compared Four Bodies and Killed Three

**Body:**

**Question in my head:**  
What shape makes a person understand something without opening an app?

**Four bodies on the table**

| Shape | Easy to read across the room? | Temptation to treat it like a pet? | Easy to open and fix? | Decision |
|---|---|---|---|---|
| Clear plastic box | Looks like lab gear / a screen cousin | Low | Very easy | No |
| Cute face / ears / toy body | People stare | **Dangerously high** | Medium | No — overlaps Unit 2 “care object” |
| Naked circuit board on a stand | Almost none | Low | Very easy | No — not a presence |
| **Closed egg that glows as one soft body, with probes sticking out** | **Yes** | Medium (I must police this) | Harder | **Yes** |

**The leap:**  
I do not need the friendliest shape. I need the shape that refuses to become a dashboard and refuses to become a pet. The egg is a compromise with a spine.

**Honest cost:**  
A closed egg gets warm inside. That is a later problem I am not hiding — it is the price of this choice, not a reason to sneak the cute face back in.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I15
**Status** LOAD-BEARING

---

## 3 · RE-I30

**Title:** The Sensor Wish-List vs What I Actually Plugged In

**Body:**

This card is me refusing to pretend the dream shopping list and the desk are the same thing.

**How I compared**

For each sense the project needs, I asked three columns:

1. **What I wanted on paper**  
2. **What is actually wired now**  
3. **What I cut on purpose**

Plain-language results:

- **Thirst of soil** — wanted a proper soil moisture probe → I have one → kept. (Cheaper rusty-style probes lie when wet; I compared and refused them.)
- **Smell / stale air** — wanted one nice air chip that also “smells” chemicals → on the desk I only have temperature/pressure-ish parts → **no true “stale air” sense yet**. I will not fake that number.
- **Light** — wanted a chip that speaks in real light units → I have a cheap light resistor that only gives a rough dark/bright → **good enough for demos, not a lab claim**.
- **Sound** — wanted a digital microphone → the small board cannot speak that language easily → I use a simple loudness sensor instead → **settled substitute**.
- **Water chemistry (acid / fertilizer)** — acid probe still waiting → fertilizer/salt probe is on but not carefully trained with real test liquids → **paused / half-done, written as such**.
- **“Someone is here” motion sensor** — early idea from the pet direction → **removed**. It answers the wrong question (your arrival, not the environment’s state).

**What this shows about my thinking:**  
A jump is allowed. A cover-up is not. Missing senses stay missing in the story until they are real.

**TYPE** 🟨 INSIGHT

**DATE** week 2
**ID** RE-I30
**Status** LOAD-BEARING

---

## 4 · RE-M2

**Title:** Soil Genome — Comparing Three “Ways of Caring”

**Body:**

**Idea in one sentence:**  
Same body, different “attention diet.” A genome here is not a new machine — it is a list of **what matters more**.

**I put three natures in one grid and asked: if this were soil life, what would it panic about first?**

| What it can feel | Soil life | Water life | Indoor air | Soil’s choice |
|---|---|---|---|---|
| Dry / wet ground | **Cares most** | Does not apply | Does not apply | Panic about thirst |
| Heat | Cares a lot | Cares even more | Medium | Roots cook / freeze |
| Day and night light | Strong | Medium | Medium | Thirst + heat + bright often travel together |
| Water chemistry | Medium | Strong | Off | Food vs salt stress |
| Stale air smell | Medium hint (rot) | Weak | **Cares most** | Only a side clue |
| Noise | Almost ignores | Medium | Strong | Background only |

**Signature story I will demo:**  
Ground dries + gets hotter + stays bright for hours → “drought.” Three clues agree, so one broken sensor is less likely to fool me.

**Rejected leap:**  
Make the soil genome secretly about “does the user love me.” That is the pet brief crawling back into the numbers.

**TYPE** 🟩 MAKING

**DATE** week 1–2
**ID** RE-M2
**Status** LOAD-BEARING

---

## 5 · RE-M3

**Title:** Water Genome — How I Infer Danger Without the Perfect Sensor

**Body:**

**The awkward fact:**  
I do not own a sensor that directly says “how much oxygen is in the water.”

**So I compared three attitudes**

| Attitude | What it would look like | Why I kept / killed it |
|---|---|---|
| Pretend I measure oxygen anyway | Fake number in the demo | Lie — killed |
| Buy the perfect probe in week one | Cleaner science | Money / time / calibration — delayed, not forgotten |
| **Admit the gap; watch several cheap clues move together** | Heat up + chemistry drift in a known pattern | **Chosen** — honest inference |

**Compared with soil and air**

- Soil can ask the ground “are you dry?” directly.  
- Air can ask “are you stale?” when that chip exists.  
- Water must say: “I cannot taste oxygen; I can only notice a suspicious combination.”

**What this shows:**  
A leap is: *change how you reason when a sense is missing.*  
A fake leap is: *invent the missing sense in software and smile.*

**TYPE** 🟩 MAKING

**DATE** week 1–2
**ID** RE-M3
**Status** LOAD-BEARING

---

## 6 · RE-M4

**Title:** Indoor Air Genome — The Room’s Breath, Not Your Mood

**Body:**

**Comparison question:**  
When something “notices a person,” whose story are we telling?

| If the object reacts to… | Soil story | Water story | Air story | Allowed? |
|---|---|---|---|---|
| Dry ground / hot days | Main story | — | — | Yes |
| Suspicious water pattern | — | Main story | — | Yes |
| Stale, damp, noisy air | Side | Side | **Main story** | Yes |
| You walking closer (motion pet sensor) | — | — | Feels like a pet saying hi | **No — removed** |

**The leap from Investigate:**  
Field work taught me people can read a creature without words. Realise must not cheat by making the object chase human attention. Indoor air genome cares about **the shared air**, even when that makes the object feel less “loving.”

**TYPE** 🟩 MAKING

**DATE** week 1–2
**ID** RE-M4
**Status** LOAD-BEARING

---

## 7 · RE-M8

**Title:** Six Shells for One Plug — Failure as Thinking

**Body:**

**What happened:**  
I printed five little cases for the sensor board’s cable end. None fitted. The sixth did.

**Options I almost took instead of reprinting**

| Escape | Why it whispered “do this” | Why I said no |
|---|---|---|
| Leave the board hanging outside the egg | Instant success photo | Then it is not the object I claimed |
| Only use a power cable forever | Avoids the awkward plug | The two boxes must **talk**, not only eat electricity |
| Glue it and hope | Fast | Later the light will flicker and I will blame the code like a coward |
| **Print again until the shape tells the truth** | Slow, ugly pile of plastic | **Chosen** |

**What this shows about my thinking:**  
I would rather show five dead shells than one perfect picture of a part that never worked. The jump is emotional as much as practical: stay with the friction.

**TYPE** 🟩 MAKING

**DATE** week 1
**ID** RE-M8
**Status** DONE

---

## 8 · RE-M9

**Title:** Power — Wall Brick vs Pocket Bank vs Battery Tower

**Body:**

**Question:**  
Can this thing sit beside soil or water like a presence, or only beside my laptop?

| Power style | Feels like a finished object? | Strong enough? | Mess of cables? | Decision |
|---|---|---|---|---|
| Wall charger tangle | No — still a desk toy | Yes | High | No for the claim |
| Phone power bank | Sort of | Often sulks / drops out | Medium | Weak |
| **Small battery tower feeding the main board** | **Yes, if the egg can own it** | **Matched to what I need** | **Fewer cables** | **Yes** |

**Honest limit:**  
Batteries empty. Demos must say how long. “Cordless” means *allowed to live in the room*, not *immortal*.

**TYPE** 🟩 MAKING

**DATE** week 1
**ID** RE-M9
**Status** SUPPORTING

---

## 9 · RE-I17

**Title:** The Flash Failed — I Blamed the Cable, the Truth Was a Menu

**Body:**

**Scene:**  
I try to put a tiny program onto the sensor board. The computer builds it fine, then fails while writing. It looks cursed.

**Suspects I lined up like a detective board**

| Suspect | What I tried | What happened |
|---|---|---|
| Bad cable | Swapped cables | Still fails |
| Wrong socket | Unplugged / replugged | Still fails |
| Weak power | Other ports | Still fails |
| “Maybe speed settings” | Twiddled alone | Still mostly fails |
| **Wrong clock setting in the software menu** (board wants one beat; menu offered another) | **Changed one dropdown** | **Suddenly works** |

**The leap:**  
I wasted time on glamorous hardware myths. The real error was ordinary and embarrassing — and that is the useful story. Teachers do not need the menu name; they need to see I can kill my favourite wrong theory.

**TYPE** 🟨 INSIGHT

**DATE** week 2
**ID** RE-I17
**Status** LOAD-BEARING

---

## 10 · RE-I18

**Title:** The Board Lied About Its Name

**Body:**

**What I thought I bought:**  
A common beginner board everyone teaches with.

**What it actually was:**  
A look‑alike chip that behaves *almost* the same — until you try to program it from the wrong computer the wrong way.

**Three ways I could have responded**

| Path | Upside | Downside | Choice |
|---|---|---|---|
| Keep pretending it is the famous board | Simple story | Keeps breaking in confusing ways | No |
| Throw it away and buy a “real” one tomorrow | Cleaner | Spends time I do not have; erases what I already learned | Later if needed |
| **Admit the look‑alike; program it on the laptop; let the other box only listen** | Matches reality; project moves | Slightly awkward two-step habit | **Yes** |

**What this shows:**  
Shopping labels are not evidence. I would rather write an ugly true sentence than a pretty false one.

**TYPE** 🟨 INSIGHT

**DATE** week 2
**ID** RE-I18
**Status** LOAD-BEARING

---

## 粘贴顺序

`RE-M1` → `RE-I15` → `RE-I30` → `RE-M2` → `RE-M3` → `RE-M4` → `RE-M8` → `RE-M9` → `RE-I17` → `RE-I18`

---

## 也请你知道（Batch 1 / 2）

Batch 2 里 `RE-I9`–`I14`（架构、通道、光、液态网络等）**仍偏技术腔**。  
若要同一套白话标准，回 **「白话改 Batch2」**，我按同样规矩重写那几张——重点改成思维跳跃，不改成芯片说明书。

下一批接线也可以继续白话 + 对比。回 **「继续 4」** 或 **「白话改 Batch2」**。
