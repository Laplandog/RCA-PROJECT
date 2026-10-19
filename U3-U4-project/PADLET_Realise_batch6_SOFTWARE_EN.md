# Realise Padlet · Batch 6 — SOFTWARE 板块（流水账体）

> 这是你三板块里最后一块，也是**目前论证最强、但 Padlet 上最空**的一块。
>
> ⚠️ **本批含三张会改写你已贴内容的卡**，请优先看：
> - `RE-I22` —— 你 `narrative.py` 的注释里自己写着"**CfC核心尚未训练，情感值近似随机**"。这是全项目最强的诚实点，Padlet 上一个字都没有。
> - `RE-I14 修订版` —— 现版本把"变化率优先于绝对值"列为用液态网络的第一条理由，但 `感官加权系统技术设计文档.md` 第 7 节明写这条**不在五周实现范围内**。现在这句话是过度宣称，**必须改**。
> - `RE-I13 修订版` —— Connection 维在代码里**根本没接到灯上**（`expression_mapper.py` 只用了 valence/arousal/safety/seeking），而你作品集第 5 页还写着 "a person nearing"，正是 `RE-Q2` 和 `RE-I20` 明令删掉的东西。
>
> 体例同前：零表格、零 Markdown 符号、术语后跟人话。

---

## S0 · RE-S4

**Title:** How to Read the Software Section

**Body:**

Three sentences, so this section is not read as a list of features.

Everything here is a rule I wrote. The hardware section was about what the object can physically feel. This section is about what it does with that — which senses matter, what counts as unusual, and how a feeling becomes light. None of it was discovered by the machine. All of it is authored, and the point of writing it out is that authored rules can be argued with.

The order matters. Read it as: the world arrives as numbers, the numbers become a departure from normal, the departure gets weighted by a nature, the weighted signal goes into a network, the network's state becomes light. Each of those arrows is a card, and each arrow is a place where I made a decision.

The most important card in this section is RE-I22, and it is the one that says what the network is not doing. If you only read one card here, read that one.

**TYPE** ⬜ CONTEXT

**DATE** 2026.7.1
**ID** RE-S4
**Status** SUPPORTING

---

## S1 · RE-I11 修订版（建议替换你 Padlet 上的旧版）

**Title:** A Genome Is a Menu of What to Care About

**Body:**

In Investigate, genome meant temperament — eight numbers describing an individual's innate leanings. In Realise I kept the word and gave it a different job, which is confusing on purpose and worth defining tightly.

Here a genome is a text file. For each of the senses the body has, it says three things: how much this nature cares about that sense, what range counts as comfortable, and how far outside that range counts as real distress. That is all. You can open it in any text editor and read it, and if you disagree with a number you can change it and run the thing again.

What this is not. It is not a different circuit board for each niche. It is not a personality for you to get attached to. And it is emphatically not evidence that the network understands tomato biology — it is evidence that I read about tomatoes and wrote some numbers down.

What it preserves from Investigate is the structural idea that one core can be biased into different dispositions by a small set of parameters. What changed is the direction of the bias: in Investigate the disposition was social, and here it is ecological.

The engineering test is blunt. If switching from soil to water requires me to unsolder anything, then the chameleon claim in RE-Q3 is false and I have quietly built a product line instead of one body. It does not, and the code that does the switching is in RE-M25 — although whether the object is *allowed* to switch turns out to be a separate question, and I answered it differently. See RE-I32.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.1
**ID** RE-I11
**Status** LOAD-BEARING

---

## S5 · RE-I12 修订版

**Title:** Two Layers Before the Network Sees Anything

**Body:**

A sensor reading is not a feeling, and the gap between them is where most of my design decisions live. There are exactly two layers in that gap, and keeping them separate is deliberate.

**Layer one turns a number into a departure.** Each sense has a comfortable band and, further out, a distress threshold. Inside the band, the output is zero — nothing to report. Outside it, the output rises smoothly toward one as the reading approaches distress, and stops at one so that an absurd reading cannot overwhelm everything else. Crucially the output is signed: too little is negative, too much is positive. Soil that is bone dry and soil that is waterlogged are both far from comfortable, and they are opposite emergencies, so collapsing them into a single "badness" score would throw away the only thing that tells them apart.

**Layer two multiplies that departure by how much this nature cares.** A departure of 0.8 on a channel weighted 0.9 arrives as 0.72. The same departure on a channel weighted 0.15 arrives as 0.12. Nothing is hidden; things are simply prioritised.

Why two layers rather than one threshold. Because they answer different questions and I want to be able to change one without the other. Layer one asks what is unusual *for this particular place* — and the numbers in it can eventually come from observing the actual environment rather than from my reading, which is RE-M26. Layer two asks what this *kind of life* prioritises, and that is a design claim about ecology that stays fixed. Drought in soil and poor ventilation in a room are different signatures even though temperature appears in both stories, and the two-layer split is what lets that be true.

One detail with a principle inside it: a sense that is switched off for a niche — moisture in an air genome, since there is no substrate — is skipped entirely rather than being given a weight of zero. Those are different statements. Zero means this nature does not care. Switched off means this question has no meaning here. The code distinguishes them because the difference is real, and the raw reading is written to the log either way.

Both layers are design. Neither is learned. That distinction is the whole subject of RE-I22.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.1
**ID** RE-I12
**Status** LOAD-BEARING

**ATTACH：** 挂 `感官加权系统技术设计文档.md`（Padlet 上已有 PDF 版），以及 `sensory_mapper.py`。

---

## S6 · RE-M24

**Title:** Building the Weighting Layer — And What It Does When a Sensor Lies

**Body:**

Writing RE-I12 as running code took one file, and most of the work in it is not the arithmetic. The arithmetic is four lines. The rest is deciding what to do when the world does not cooperate.

Four situations, each with a decision behind it.

A sense is switched off for this niche. Skip it entirely, output zero, but still write the raw reading to the log. Logging a channel nobody is listening to sounds pointless until you consider the case where the wrong genome is loaded — a soil genome in a fish tank. If the muted channels were never recorded, there would be no way to ever notice. The body senses fully; the genome only decides what it feels.

A reading is missing because the sensor is not connected. Output zero, meaning neutral, and write a warning into the log. Neutral rather than distressed, because an absent sensor is not evidence of a problem — the whole argument in RE-M12 and RE-M18 is that absence must stay absence.

A reading arrives that is physically impossible, like a pH of fifteen on a scale that ends at fourteen. Treat it as a broken sensor rather than an emergency. Neutral, warning, move on. This one is the least intuitive and the most important: the naive behaviour is to feed it through the curve, get maximum distress, and turn the light red. A device that panics loudest when its sensors are broken is worse than useless, because it is most dramatic exactly when it is least informed.

A reading is not a number at all, because the line arrived garbled. Same treatment.

What these four have in common is that the system's response to not knowing is to say nothing rather than to guess. That is the same commitment as RE-M12 at the software end, and it is the reason I can claim in RE-I30 that missing senses stay missing in the story.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M24
**Status** LOAD-BEARING

**ATTACH：** `sensory_mapper.py`。

---

## S7 · RE-M26

**Title:** The Calibration Window — Letting It Watch Before It Judges

**Body:**

RE-Q4 asks where the comfortable ranges come from. Right now the honest answer is: I estimated them from reading, and every genome file admits this in a field near the top that says so in plain text. I have left that field in rather than deleting it.

This card is the mechanism that replaces the estimate, and it is written and tested but not yet run on real long-term data.

How it works. When the device is placed somewhere new, it spends the first several days making no judgements at all. It only records. Then it takes each sense's recorded history, finds the average and the spread, and defines comfortable as within one spread of the average and distressed as beyond three spreads. It writes those numbers back into the genome file and changes the status field from "estimated" to "calibrated from real observation."

Three details with reasoning attached.

It refuses to calibrate on too little data, and says so rather than producing a confident band from six readings.

It does not calibrate senses that are switched off for this niche, since there is nothing meaningful to observe.

And during the observation period the light holds a soft neutral white — not because that is pretty, but because it is the honest expression of the state the device is actually in. It is not calm. It is not distressed. It has no basis yet for either, and the light should say that rather than defaulting to a comfortable green.

Why this is worth the complexity. It moves the answer to "where did these thresholds come from" from *I read some papers* to *the device measured this specific place for a week*. Those are very different claims to defend. It does not make the thresholds objective — a week of observation in an already-struggling environment would calibrate distress as normal, which is a real weakness and the reason the estimated values remain as a fallback. What it does is make the origin of every number local and inspectable: you can always ask which days, under what conditions, with which genome.

And it happens to be the same shape as something already in the project's narrative from Investigate — a new thing spends its earliest period simply taking in its surroundings before it has any basis for judgement. I did not design the mechanism to fit the metaphor. I noticed afterwards that the honest engineering solution and the developmental story were the same shape, which is the kind of coincidence worth pointing at rather than pretending was planned.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M26
**Status** RUNNING

**ATTACH：** `calibration.py`。

---

## S8 · RE-M23

**Title:** Moving the Emotion Core Into the Object

**Body:**

The network doing the feeling is the same one built in Investigate, moved across without retraining. That is the point rather than a shortcut, and RE-S3 lists it as the main thing that travels from AL- to RE-.

What it actually is: a CfC network wired by AutoNCP. Both of those names describe a neural network that runs in continuous time — meaning it is told how much real time has passed between one reading and the next, and its internal state evolves accordingly. A conventional network sees a sequence of steps and has no idea whether they were two seconds or two hours apart. This one is told, every time.

That is the whole reason it is here rather than a simpler thing. This object's subject matter is a slow environment. A drop in soil moisture over four hours and the same drop over four minutes are different events, and only a model that knows about elapsed time can treat them differently.

The specific shape: eight weighted senses go in, twenty-eight neurons in the middle, five values come out — the same five-dimensional emotion space from Investigate. Valence, arousal, safety, connection, seeking.

Two implementation details that carry meaning.

The internal state persists between readings. Each tick does not start from blank; it continues from where the last one left off. That continuity is the closest thing in this system to the object being continuously alive rather than repeatedly consulted, and it is the same property that made the wild-type experiment's crash-and-restart seams matter so much in Investigate.

And each genome nudges the starting state slightly, using one of the temperament parameters carried over from the eight-parameter system. Deliberately gently — the offset is scaled right down, because a large one would mean the genome was dictating the output rather than tilting it.

What did not travel: the caregiver language model, the simulated apartment, and any suggestion that five weeks of this equals long ecological learning.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M23
**Status** LOAD-BEARING

**ATTACH：** `life_core.py`。

---

## S9 · RE-I22 ⭐ 本板块最重要的一张

**Title:** The Network Is Not Trained — Saying So Before Anyone Asks

**Body:**

This is the card I would most like to be judged on, and it is the one that makes the project smaller.

The emotion network in this device has never been trained. Its internal weights are random. It runs in inference mode and no learning happens while it is running.

This is not an accident and it is not a bug. It is the same condition as the wild-type entity in Investigate — a randomly initialised core with no pre-training — and it is deliberate. But it has a consequence I have to state plainly rather than let a viewer infer wrongly: **the five emotion values coming out of this network are not meaningful in themselves.** They are a fixed but arbitrary function of the input. Valence is not a judgement about whether things are good. It is a number produced by untrained weights.

I did not decide this by reasoning about it in the abstract. I found it while writing the narrative engine — the part that turns readings into a written diary — and discovering that if I drove the diary from the emotion values, the entries were nonsense. So I wrote in the comments at the top of that file that the emotion values are approximately random and that the diary would instead be driven by the comfort-zone departures, which have unambiguous physical meaning. That comment is the most useful sentence in my codebase.

So here is the honest account of what makes the light change colour.

The chain that carries meaning is: sensor reading, comfort curve, genome weight, and then straight into either the diary or the light. Every step in that chain is a rule I wrote, and every step is defensible, because a departure from a comfortable moisture band genuinely does mean the soil is drying.

The network's contribution is different in kind. Because it runs in continuous time and carries its state forward, it contributes *how the response moves* — how quickly the state shifts when several senses change together, how it lags, how it settles afterwards. That is a real temporal texture and it is why the light does not snap between states like a threshold alarm. It is not knowledge about ecology.

Which gives the answer to RE-Q6. When the light breathes and someone says it feels alive, the correct response is: the colour is designed, the timing is dynamics, and neither is understanding. If a drought demonstration looks convincing because I wrote a moisture weight of 0.9 and mapped negative valence to red, that is successful design and I should call it design.

The uncomfortable version, stated once so it cannot be said I avoided it: with the network untrained, a large part of what this device does could be achieved without it. The network earns its place through temporal behaviour and through architectural continuity with Investigate — not because it knows anything. Training it on real long-term deployment data is the obvious next step and it is outside five weeks.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.20
**ID** RE-I22
**Status** LOAD-BEARING

**ATTACH：** ⭐ **截一张 `narrative.py` 开头那段注释的图**（"情感只作调味：CfC核心尚未训练…"那三行），配一句英文翻译。这是你自己在写代码时写下的诚实，比任何事后声明都有力。建议这张卡置顶到 SOFTWARE 板块最前面。

---

## S10 · RE-I14 修订版（⚠️ 必须替换你 Padlet 上的旧版）

**Title:** Why a Continuous-Time Network Rather Than an Alarm

**Body:**

> ⚠️ 旧版第一条理由是 "Rate of change over absolute value"。你的加权设计文档第 7 节明写：变化率**不在五周实现范围内**，当前只用瞬时读数，这条原则只体现在校准逻辑里。旧版是过度宣称，以下为诚实版。

An alarm that fires when moisture drops below a fixed number is a much smaller project than this one, and it would work. So the network has to justify itself.

The first justification is time, and it is the real one. This model is told how much actual time passed between readings, and its state evolves accordingly. A slow slide and a sudden drop produce different internal trajectories even when they end at the same value. That is a property a threshold cannot have, and it matters because the subject is an environment, where almost everything that matters is a shape over hours rather than a value at an instant.

The second is that several senses arrive together and interact. Drought in the soil genome is not moisture alone — it is moisture falling while temperature rises while light has been high for hours, three departures reinforcing each other. A network integrating all of them at once handles that without me writing a rule for every combination, and a single drifting sensor carries less weight when nothing else agrees with it.

The third is continuity. The state carries forward, so the object has a recent past. It does not evaluate each reading from a blank start.

Now the correction, which is why this card was rewritten. An earlier version of this card claimed that the system prioritises rate of change over absolute value. That is the design intention and it is **not currently implemented.** My own technical document is explicit: within five weeks, only instantaneous readings are used, and the rate-of-change principle appears only in the calibration logic, not in live inference. The interface for adding it exists and it is a named future step. Until it is built, the honest statement is that the network handles time *internally* through its own dynamics, not that the system explicitly reasons about rates.

Restating the limit from RE-I22: the weighting rules that aim any of this at drought are authored by me, and the network is untrained. Continuous-time dynamics are a real reason to use this architecture. They are not a licence to describe designed behaviour as emergent.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.20
**ID** RE-I14
**Status** LOAD-BEARING

---

## S11 · RE-I13 修订版（⚠️ 必须替换，并且**作品集第 5 页要一起改**）

**Title:** From Feeling to Light — What Is Mapped and What Is Not

**Body:**

> ⚠️ 你作品集 `pd_page5_expression` 里 Connection 那行写的是 "When it senses a response — **a person nearing**, sound shifting"。这正是 `RE-Q2` 和 `RE-I20` 明令拒绝的行为。**Padlet 和作品集必须同时改**，否则老师会发现你的原则和你的产品页在打架。

Five dimensions come out of the network. Not all five reach the light, and I would rather say which than imply a completeness the code does not have.

Valence becomes colour. Distress runs toward amber and red; ease runs toward green and cyan. In the driver this is not a continuous rainbow but five named states — settled, calm, alert, uncomfortable, threatened — with the colour sliding smoothly between them rather than snapping, because a hard jump reads as a notification and a slide reads as a body changing.

Arousal becomes breathing speed. The rhythm rises and falls continuously; higher arousal breathes faster. In practice the driver deliberately compresses this into a narrow, slow range — the fastest it will go is still slower than a person's resting breath. A fast blinking object is an appliance demanding attention. This one is not allowed to demand.

Safety becomes steadiness. Below a threshold, a small random unevenness is added to the brightness. Not a flicker, not an alarm — the difference between a steady hand and a slightly unsteady one.

Seeking raises the pulse rate at extremes, and a tone is reserved for extremes only. Never speech. That is argued separately in RE-I21.

**Connection is currently not mapped to anything.** The expression code uses valence, arousal, safety and seeking; connection is computed and unused. I am stating that rather than describing an intended flowing-ring behaviour as if it existed.

And there is a specific reason connection is the hard one, which is worth more than the missing feature. In an earlier version, connection was going to respond when a person came near. That is the motion sensor from RE-I20 reappearing in software after I had physically removed it from the board — the same wrong idea, wearing code instead of a component. The test in RE-Q2 rules it out: does the output report the environment, or audition for affection. So connection has to mean the *sensed medium* answering back, and I have not yet found a version of that which is honest rather than decorative. It stays unmapped until I do.

One number I should not overstate: a specific breathing period appears in my portfolio deck as a calm resting rhythm. That figure was chosen for comfortable human peripheral reading and then adjusted again in the driver. It was not discovered by the network, and the deck and the code should be reconciled rather than quoted at different values.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.20
**ID** RE-I13
**Status** LOAD-BEARING

**ATTACH：** `expression_mapper.py` + `led_driver.py`。

---

## S12 · RE-M27

**Title:** Driving Thirty LEDs Without the Convenient Library

**Body:**

The light ring is thirty individually addressable LEDs. Each one wants its colour delivered as a precisely timed sequence of electrical pulses, at a rate where being slightly late corrupts the message — and a Raspberry Pi runs a normal operating system that can interrupt whatever it is doing at any moment. The usual answer is a well-known library that handles this. Installing it dragged in a stack of dependencies I did not want on a device meant to boot reliably inside a sealed shell.

So the driver instead borrows a different piece of hardware. The Pi has an interface built for talking to chips at a fixed clock rate, and the driver uses it to fake the LED protocol: every single bit of colour data is expressed as three bits on that interface, one pattern meaning one and another meaning zero. The timing then comes from dedicated hardware rather than from software hoping to be scheduled on time. The whole driver is about forty lines and has no dependencies beyond one standard module.

Above it sits the expression loop, running fifty times a second in its own thread. It reads the current state, decides which of the five moods applies, slides the colour gradually toward that mood's colour, and modulates brightness as a slow sine wave whose frequency comes from arousal. Threatened states get a raised minimum brightness so distress is visible across a room rather than only when you are standing over it. Low safety adds the small unevenness described in RE-I13.

Two decisions I want on the record.

Every drawing operation is wrapped so that a failure cannot take down the main program. If the light dies, the sensing and the reasoning continue and the logs keep being written. The expression layer is allowed to fail alone.

And when nothing is alive — before a life has been started — the ring holds a very dim, very slow blue. Not off. Off would be indistinguishable from unplugged, and the object's entire claim is that its state is readable from across the room. Dormant has to look like dormant.

**TYPE** 🟩 MAKING

**DATE** 2026.7.20
**ID** RE-M27
**Status** LOAD-BEARING

**ATTACH：** ⭐ **五种心情各拍一张灯亮着的照片**，横排贴出来。这是整个 SOFTWARE 板块唯一一张不懂技术的老师能直接"读懂"的东西。挂 `led_ws2812.py` 和 `led_driver.py`。

---

## S13 · RE-I21

**Title:** No Speech — Even Though It Would Be Easy

**Body:**

The object has a diary. It writes sentences like "the soil is drying out; I begin to feel thirsty." Those sentences are in the phone journal, and they are never spoken and never displayed on the object itself.

This is a restriction I imposed while holding the means to break it. The whole Investigate project used a language model. Making this thing talk would take an afternoon and it would be the single most impressive-seeming addition available to me.

The reason not to is in the field work. AL-P0 through P4 asked people who care for small animals how they first notice a state change *without language*. Every participant answered from before language: a sound, a stillness, a smell, a posture, or something they could only call a feeling. That pre-verbal reading is the thing this project is trying to make possible for environments — and if the object says "I am thirsty," the reading is over before it starts. You have not learned to read anything. You have been told.

There is a second reason that is about the machine rather than the person. A spoken sentence claims understanding. When something says "I feel unsafe," it is asserting an inner life. Given RE-I22 — an untrained network producing approximately arbitrary emotion values — that claim would be false in a way that light simply cannot be. Light is honest by being ambiguous. It shows a state and leaves the interpreting to you, which is exactly the division of labour the field participants described doing with their animals every day.

So: a tone is permitted at extremes, where it functions as an alarm rather than a statement. Text lives in the journal, where it is a record you choose to open, not a voice in the room. The object itself stays wordless.

The written phrases exist in both English and Chinese, and they are fixed sentences I wrote, chosen by which sense departed and in which direction. No language model runs on this device. That is worth stating precisely, because "it writes a diary" would otherwise imply something much more impressive and much less honest than what is happening.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.20
**ID** RE-I21
**Status** LOAD-BEARING

**ATTACH：** `narrative.py`。

---

## S14 · RE-I32 ⭐ 新卡

**Title:** The Engine Can Change Its Nature. The Object Is Not Allowed To.

**Body:**

This is a decision where the code and the product deliberately disagree, and I want the disagreement visible rather than tidied away.

The engine supports switching genome at runtime. One function call swaps the weighting table and the object is now reading its world as a different kind of life. It works, and RE-M25 describes it.

The product refuses to use it. In the application, a genome is chosen once, when a life begins, and never changes for as long as that life exists.

I went back and forth on this and the argument that settled it was about what the word nature is doing. If you can change what something fundamentally cares about with a dropdown menu, then it was never a nature — it was a costume, and the object is a demonstration rig wearing themes. RE-Q3 asks whether one body can wear many natures. The answer I have landed on is: one body, yes, across many *lives* — but not one life trying on several. A tomato does not become a fish in the afternoon.

There is also a technical fact that supports it and that I did not design for. Switching genome resets the network's internal state, because the state was accumulated under a different set of priorities and carrying it across would be meaningless. So a switch is not seamless — it is a discontinuity, a small death and rebirth. Once I noticed that, pretending it was a settings change felt dishonest.

This has a cost I am accepting knowingly. It makes the most impressive possible demonstration unavailable: same hardware, same room, flip the file, watch the light reinterpret the identical world. That demonstration would be a genuinely good argument for RE-Q3 and I have given it up.

What replaces it is in RE-P3: run the same recorded conditions through two separately born lives with different natures, and compare. Less theatrical. It shows the same thing without requiring the object to contradict what it says it is.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.20
**ID** RE-I32
**Status** LOAD-BEARING

---

## S15 · RE-M25

**Title:** Switching Genome Is Loading a File

**Body:**

The engineering claim behind RE-Q3 comes down to one thing: is changing niche a matter of changing a file, or a matter of changing the machine.

It is a file. The function that does it loads a different text file into the weighting layer and deliberately keeps the same network weights. Nothing is recompiled, no hardware is touched, no soldering iron is involved. The same body, the same probes, the same core — a different set of priorities.

Keeping the network weights identical across the switch is the part that matters. If a genome swap also swapped the network, then soil and water would be two different brains and the chameleon idea would be marketing. Because the core is the same, what changes is genuinely only what this life attends to, not what it is capable of.

The one thing that does reset is the accumulated internal state, for the reason given in RE-I32: a state built up under one set of priorities does not mean anything under another.

So the mechanism exists, works, and is verified. And the product then declines to expose it as a live switch, which is RE-I32. Both of those are true at once, and I would rather this Padlet show a capability that was built and then deliberately restrained than imply the restraint was a limitation.

**TYPE** 🟩 MAKING

**DATE** 2026.7.20
**ID** RE-M25
**Status** DONE

**ATTACH：** `life_core.py` 里 `switch_genome()` 那段（含注释）。

---

## S16 · RE-M32 ⭐ 新卡

**Title:** Birth, Freezing, Rebirth, Death — Building a Life You Can Lose

**Body:**

The application around all of this is not a settings panel. It is organised around one active life at a time, and around a small set of actions that are deliberately weighty.

A life is born: you choose its nature, and from that moment it accumulates a history. It can be frozen, which suspends it without deleting anything — every diary entry and every scrap of accumulated state is preserved, and it goes into storage while another life becomes active. It can be woken again later and carries on. It can be reborn, which erases this particular life and starts a new one. Or there is death, which clears everything, including storage, and returns to an empty first screen.

Age counts only time spent actively alive. Frozen time does not count. Time while the device is switched off does not count. That was the first decision in this design and everything else followed from it, because it meant age had to mean accumulated experience rather than elapsed calendar time — which is the only definition consistent with what Investigate was arguing about persistence and continuity.

The state persists across a power cut and comes back as the same life. That matters more than it sounds: in Investigate, the wild-type run had crash-and-restart seams that had to be disclosed in every card that touched them, because a discontinuity in the entity's history is a discontinuity in the claim. Building the persistence properly here is that lesson paid forward.

Two things I want to say honestly about it.

This is the part of the project that most risks pulling back toward the companion object I rejected in RE-I1. Freezing and death are emotionally loaded actions. A person who freezes a life rather than deleting it is treating it as something that can be harmed, and my field participants used exactly that vocabulary — care, responsibility, the fear of damaging something once it has become singular.

But I do not think this is the pet brief returning, and the test in RE-Q2 is why. None of these actions makes the object respond to *you*. They govern whether it is reading its environment at all. The weight is not affection, it is the difference between an instrument you can reset without consequence and a record that means something because it could be lost. RE-Q4's calibration argument depends on exactly that: a device whose history can be casually wiped has no basis for knowing what normal looks like here.

**TYPE** 🟩 MAKING

**DATE** 2026.7.20
**ID** RE-M32
**Status** LOAD-BEARING

**ATTACH：** `dashboard.py` 顶部那段说明（出生/冷冻/唤醒/重生/死亡 + 年龄定义）——**建议翻成英文再挂**。

---

## S17 · RE-M28

**Title:** The Phone Page Is a Journal, Not a Cockpit

**Body:**

There is a phone interface. It is a small web page served by the device itself over the local network, installable to a home screen and able to open without a connection. RE-I7 already committed to it being secondary, and this card is where that commitment had to survive contact with actually building it.

It shows the current readings, the current state, the diary, and the life-management actions from RE-M32.

The temptation was immediate and strong. Once the data is on a screen, charts are easy, and charts are satisfying, and a well-made dashboard would be the fastest way to make this project look finished. I have watched myself want to add a graph of moisture over time roughly once a week.

The rule that keeps it in its place: **nothing may appear on the phone that is required to understand the object.** The phone can tell you more, and more precisely, and further back in time. It cannot be the only place a state is legible. If I ever find myself needing to open it to know how things are going, RE-Q1 has failed and the failure is in the light, not in the phone.

There is a structural reason it stays honest, too. The reasoning process writes its current state to a small file, and the web page reads that file. The page cannot ask the network anything, cannot influence it, and does not contain any of the interpretation. It is a window onto a process that would run identically with nobody watching — which is the correct relationship for a device whose subject is an environment that does not care whether you are looking.

Where it genuinely earns its place is the diary. RE-I21 keeps language off the object; this is where language is allowed to live, as a record you choose to open. Reading back through three days of entries is a different act from glancing at a light, and it is the one thing here a chart could not do better.

**TYPE** 🟩 MAKING

**DATE** 2026.7.20
**ID** RE-M28
**Status** SUPPORTING

**ATTACH：** `portfolio/demo.html`、`portfolio/app_showcase.svg`（你已经做好了），手机上打开的实拍照片。

---

## S18 · RE-M29

**Title:** Everything at Once — The First Full Loop

**Body:**

The smoke test is the moment where the two halves of this Padlet meet: real sensors on one side, all the authored rules on the other.

One command, one genome, and the whole chain runs continuously. Real readings arrive from the Arduino every two seconds. Each one passes through the comfort curves and the genome weights. The weighted vector goes into the network, which is told how much real time has passed. Five values come out. Those become a colour and a rhythm on thirty LEDs, and any transition between comfort and stress becomes a diary entry.

What it verifies is only that the chain is unbroken and does not fall over. That is not nothing — it is the first time the sequence exists as one continuous thing rather than as parts I have tested separately — but it is much less than it looks. Read it against RE-S5 for what the object can actually feel: two channels are properly real, three are rough, one is absent, one is unwired. Read it against RE-I22 for what the network is actually contributing.

The things that made it not work the first time were, without exception, boring. A speed mismatch. A field name typed differently at each end. The absent pH field arriving as nothing where the code expected something. None of them were interesting and all of them were mine.

And one thing I should say about what this is not. Everything up to here proves the machine works. Nothing up to here shows that a person can read it. That is a different question, it is the question RE-Q1 actually asks, and it belongs to the demonstration cards.

**TYPE** 🟩 MAKING

**DATE** 2026.7.20
**ID** RE-M29
**Status** RUNNING

**ATTACH：** ⭐ **一段一镜到底的视频**：手上浇水/吹热风 → 镜头摇到灯 → 灯变色。不切、不加字幕。这一段能顶十张卡。

---

## S19 · RE-I9 修订版（白话）

**Title:** The Whole Chain in One Breath

**Body:**

Six steps, and every arrow between them is a card in this Padlet.

An environment — soil, water, or a room — that is doing something a person cannot see.

Sensors touching it, on a small board whose only job is to read and report. Roughly two seconds, one line of text, physical units, and anything it cannot sense is simply absent from that line.

A cable. One direction only. The reading board never hears back.

A small computer that turns each reading into how far things sit from comfortable, weights that by what this particular nature cares about, and feeds it to a continuous-time network that has been carrying its own state forward since the life began.

Five numbers describing an internal state.

Thirty lights behaving as one glowing body: colour, breathing rhythm, steadiness. No words.

This is Investigate's emotional stack moved into a physical loop. Nothing in it requires a caregiver language model. Nothing in it takes the user's mood as an input.

Two rules govern the whole chain. If a stage is faked — simulated readings presented as live — it is a different claim and must be labelled as one, a lesson already paid for in the wild-type run. And if a stage does not know something, it says nothing rather than guessing, which is why the light stays honest when a sensor is missing instead of confidently reporting an emergency that is not happening.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.1
**ID** RE-I9
**Status** LOAD-BEARING

**ATTACH：** ⭐ 你作品集 `pd_page2_architecture.svg`（第 02/07 页）就是这张卡的图，直接挂。

---

# SOFTWARE 板块最终顺序

```
RE-S4  → RE-I22 ⭐（建议提前，先说清楚不是什么）
       → RE-I9 → RE-I11 → RE-I12 → RE-M24 → RE-M26
       → RE-M23 → RE-I14 → RE-I13 → RE-M27 → RE-I21
       → RE-I32 → RE-M25 → RE-M32 → RE-M28 → RE-M29
       → RE-M2 → RE-M3 → RE-M4（batch3 重写版里的三张基因组卡）
```

---

# 本批 ATTACH 汇总

| ID | 附什么 | 优先级 |
|---|---|---|
| RE-I22 | ⭐ `narrative.py` 开头注释截图 + 英译 | 最高 |
| RE-M27 | ⭐ 五种心情的灯光照片横排 | 最高 |
| RE-M29 | ⭐ 一镜到底视频：浇水/吹热风 → 灯变 | 最高 |
| RE-I9 | `pd_page2_architecture.svg` | ✅ 现成 |
| RE-I12 | `感官加权系统技术设计文档.md` + `sensory_mapper.py` | ✅ 现成 |
| RE-M23 | `life_core.py` | ✅ 现成 |
| RE-M26 | `calibration.py` | ✅ 现成 |
| RE-I13 | `expression_mapper.py` + `led_driver.py` | ✅ 现成 |
| RE-I21 | `narrative.py` | ✅ 现成 |
| RE-M25 | `life_core.py` 的 `switch_genome()` 片段 | ✅ 现成 |
| RE-M32 | `dashboard.py` 顶部说明（**需翻英**） | 需翻译 |
| RE-M28 | `demo.html` / `app_showcase.svg` + 手机实拍 | 半有 |
