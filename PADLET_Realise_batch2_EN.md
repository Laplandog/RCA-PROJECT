# Realise Padlet · Batch 2（可直接粘贴）

> **本批 10 张**：`RE-I6` · `RE-I7` · `RE-I8` · `RE-I9` · `RE-I10` · `RE-I11` · `RE-I12` · `RE-I13` · `RE-I14` · `RE-I29`  
> 尾部格式按你指定的四行块（TYPE 后空一行）。  
> DATE 用 Realise 周次占位；你贴 Padlet 时可改成精确日期。  
> **已校对**：表格改散文（Padlet 友好）；Connection 映射去掉「对人打招呼」歧义；原 `RE-C1` 因无具名引用改挂 `RE-I29`。

---

## 1 · RE-I6

**Title:** Field Research Forced the Product Question

**Body:**

The field instrument was never a popularity test for a device I had already decided to build.

`AL-P0`–`P4` asked keepers of small living creatures how they first notice a state change without language — seen, heard, smelled, touched, or “just felt” — and what it costs to learn that reading. The speculative probe (a blank digital being that senses through physical sensors and grows) was there to watch the *human* reaction, not to validate a Tamagotchi brief.

What came back forced the product question sideways. The useful material was not “I would love this.” It was material about **reading**: mistranslation loops, delayed recognition, the fear of damaging something once it has become singular, the difference between relating to one individual and to a group. That is a problem of legibility under uncertainty — the same problem `AL-Q7` named for the entity’s inner states.

So Realise does not ask: how do I make people attach to an object?  
It asks: how does a person understand what a living system is experiencing **without a data dashboard**?

The companionship product failed that question. Ecological translation is the form that can still answer it (`RE-Q1`, `RE-I1`).

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I6
**Status** LOAD-BEARING

---

## 2 · RE-I7

**Title:** Why Not a Dashboard App Alone

**Body:**

A clean dashboard would be easier to finish in five weeks. Charts for moisture, VOC, pH; thresholds in red. It would also abandon the only constraint that makes Realise continuous with Investigate.

If understanding requires opening a phone and reading numbers, the project has accepted that ecological state is for people who already think in dashboards. The field work pointed the other way: keepers often catch the first signal in the body — a sound, a stillness, a smell, a “just felt” — before they can name a metric.

So the phone may exist as a **secondary** journal and debug surface (portfolio PWA, logs, genome switch UI). It is not the primary interface. The primary interface is the object in the room: light, breath, optional extreme tone — never speech (`RE-Q1`, `RE-I21`).

This is also how Realise stays distinct from a generic IoT plant monitor. The claim is not denser data. The claim is a different channel of understanding.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I7
**Status** LOAD-BEARING

---

## 3 · RE-I8

**Title:** Naming the Object — ANIMA / A Living Presence

**Body:**

The name has to carry the corrected brief, not the abandoned one.

**ANIMA** points at an animating principle — something that makes a body feel inhabited — without promising a pet, a friend, or a therapist. **A Living Presence** describes what you encounter in the room: a continuous presence whose state can be sensed peripherally, not a character waiting to be entertained.

What the name must not do: invite “my baby,” “feed me,” or “I missed you” as the default story. Those stories pull the expression layer back toward companionship (`RE-I5`).

Naming is a design control. Every caption, portfolio slide, and LED behaviour has to remain compatible with: *translation medium for an environment you cannot feel directly* (`RE-I4`).

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I8
**Status** SUPPORTING

---

## 4 · RE-I9

**Title:** System Architecture — From Environment to Light

**Body:**

The signal chain Realise actually builds:

**Environment** (soil / water / air)  
→ **Sensory organs** (Arduino Uno, seven channels sampled and packed)  
→ **Nerve** (USB serial JSON, ~every 2s at 115200 baud)  
→ **Cognitive core** (Raspberry Pi 4B running CfC + AutoNCP)  
→ **Inner state** (5-D emotion: valence · arousal · safety · connection · seeking)  
→ **Expression** (addressable LED core — colour, breath, stability, flow; non-verbal)

This is Investigate’s emotional stack moved into a physical loop. Nothing in this diagram requires a caregiver LLM. Nothing in this diagram centres the user’s mood as input.

If a stage is missing, the translation breaks. If a stage is faked (simulated packets labelled as live without saying so), the demo is a different claim and must be labelled as such — a lesson already paid for in the wild-type run.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I9
**Status** LOAD-BEARING

---

## 5 · RE-I10

**Title:** Seven Universal Sensory Channels

**Body:**

One shared body of senses. Genomes differ in *care*, not in whether the channel exists.

Seven channels: **T** temperature (medium) · **M** moisture (substrate water; weight forced to zero when physically N/A) · **G** air & VOC (breath, staleness, ventilation) · **L** light (day/night rhythm) · **S** sound (disturbance, flow, noise) · **pH** acidity (wet media) · **EC** conductivity / nutrients (starvation vs salt stress).

**Principle:** a channel weighted to zero is still recorded. The body senses fully; the genome only decides what it feels. That leaves room later for “this looks more like water — switch genome?” without having been blind (`RE-Q3`, `RE-I11`).

Hardware on the bench may lag the ideal list (e.g. photoresistors before BH1750, BMP280 before BME680, pH paused). Those gaps belong on MAKING cards as RUNNING — they do not rewrite this principle.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I10
**Status** LOAD-BEARING

---

## 6 · RE-I11

**Title:** A Genome Is a Sensory Weighting Table, Not Different Hardware

**Body:**

In Investigate, genome meant temperament — innate bias for an individual entity. In Realise, the same word is overloaded on purpose, then redefined tightly:

A genome is a **JSON weighting table**: per channel, a weight (0–1), a comfort range, and a sensitivity curve. Switching file is how one body wears soil/root, freshwater, or indoor air (`RE-Q3`).

What this is not:
- not a different PCB per niche
- not a personality for the user to bond with
- not proof that the CfC “knows” tomato biology

What this preserves from Investigate: the idea that the *same core* can be biased into different dispositions by a compact parameter set. What changes: the disposition is ecological, not social.

Engineering test: if I cannot change niche without resoldering, the chameleon claim is false.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I11
**Status** LOAD-BEARING

---

## 7 · RE-I12

**Title:** Two-Layer Sensory Weighting — Comfort Curve × Genome Weight

**Body:**

Raw sensor numbers are not feelings. Realise inserts two authored layers before the CfC sees the world:

1. **Comfort curve** — how far a reading sits from a local comfort band (preferably calibrated from early deployment observation, not only from a paper — `RE-Q4`).
2. **Genome weight** — how much this nature cares about that channel right now.

The product fed to the network is the combination: a weighted stress / relief signal per channel (and jointly across channels for signature events).

Why two layers rather than one magic threshold: it keeps “what is unusual for this place” separable from “what this niche prioritises.” Drought for soil is not the same signature as poor ventilation for indoor air, even if temperature appears in both stories.

These layers are **design**. They must stay architecturally distinct from the CfC’s continuous-time dynamics (`RE-Q6`, `RE-I22`). Full technical write-up hangs as supporting document (`RE-S4` / sensory weighting PDF).

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I12
**Status** LOAD-BEARING

---

## 8 · RE-I13

**Title:** From Feeling to Light

**Body:**

The five-dimensional state becomes non-verbal physical expression. It reports what the environment is going through — never what the device “wants” (`RE-I5`).

- **Valence** (distress ↔ pleasure) → LED hue: negative toward orange/red; positive toward green/cyan; neutral toward warm white.
- **Arousal** (calm ↔ aroused) → breathing speed.
- **Safety** (alert ↔ secure) → stability versus tremor / waver.
- **Connection** (isolated ↔ answered) → a flowing ring when the *sensed world* shifts in a way the genome treats as response — e.g. sound / vibration change in the medium — **not** a greeting ritual for whoever walks by. (PIR-style “someone is here → be happy” was rejected with the companionship brief.)
- **Seeking** (content ↔ needful) → pulse rate; optional tone only at extremes — never speech.

Calm secure growing ≈ a slow breath near 4.5s. That number is chosen for human peripheral reading, not discovered by the network.

If a mapping makes the object look needy in order to summon the user, it fails `RE-Q2`. Cut it.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I13
**Status** LOAD-BEARING

---

## 9 · RE-I14

**Title:** Why a Liquid Neural Network Here

**Body:**

A threshold alarm (“moisture < X”) is not the same project. Realise keeps CfC + AutoNCP for three architectural reasons already rehearsed in the product thinking:

1. **Rate of change over absolute value** — flag departure from the environment’s own recent rhythm. The same drop can be danger in one context and night-normal in another.
2. **Multi-channel consistency** — one drifting sensor is often noise; an event earns trust when independent channels trend together.
3. **Zero weight ≠ blind** — muted channels still log. Attention shifts; the sense body stays whole.

This is why the Investigate core is reused rather than replaced with if-statements (`RE-I2`, `RE-S3`). Reuse is not nostalgia. It is the claim that temporal dynamics still matter once the sensing target changes from “creature in a room” to “medium in a niche.”

Limit, restated: weighting rules that *aim* those dynamics at drought or hypoxia are still authored (`RE-Q6`). The LNN does not get to launder design into emergence.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I14
**Status** LOAD-BEARING

---

## 10 · RE-C1 → 改挂为 RE-I29（见下）／或补先例后再用 C

> ⚠ 检查结论：这张**几乎没有具名作品/文献**，按 Investigate 规则不够格当 🟪 PRECEDENT（AL-C / AL-R 都是具体引用）。先改成 🟨 INSIGHT，ID 用 `RE-I29`，避免假先例。你之后若补上 1–2 个真引用，再拆回 `RE-C1`。

**Title:** Why This Is Not Another Wellbeing Toy

**Body:**

Unit 2 already occupied “emotional wellbeing object” territory. A companionship egg would have been a thematic remake with better lights.

Realise has to sit in a different neighbourhood: ambient / environmental sensing that tries to make invisible conditions graspable without forcing the user through a spreadsheet — more “legibility of a world that is not you” than “an object that soothes you.” I am not loading a fake bibliography onto this card. When a specific exhibition, device, or paper becomes load-bearing for the argument, it gets its own 🟪 PRECEDENT card with a real citation — the Investigate standard.

What I refuse from the pet neighbourhood: bonding loops as success metrics.

If a reader can swap ANIMA for a generic ADHD soothe-toy and the story still works, the positioning failed — go back to `RE-I1` and `RE-I6`.

**TYPE** 🟨 INSIGHT

**DATE** week 1
**ID** RE-I29
**Status** SUPPORTING

---

## 粘贴顺序

1. `RE-I6` → `RE-I7` → `RE-I8`  
2. `RE-I9` → `RE-I10` → `RE-I11` → `RE-I12` → `RE-I13` → `RE-I14`  
3. `RE-I29`

建议紧接 Batch 1 的 `RE-I5` 之后、进入硬件 MAKING 之前。

---

## 下一批判预告（Batch 3）

硬件与接线脊骨：`RE-M1` 零件就位、`RE-I15` 为什么是蛋、`RE-M5`–`M8` 外壳/六版失败、`RE-I17`–`I19`（16MHz / LGT8 / USB 坑）、`RE-M12` 串口合同。

回 **「继续 3」** 即写。
