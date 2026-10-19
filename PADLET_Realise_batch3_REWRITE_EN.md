# Realise Padlet · Batch 3 重写版（流水账体 · 按外观/硬件/软件三板块归位）

> **改了什么**
> 1. 全部去掉对比表格 —— 表格把"我先想到 A、撞墙、才想到 B"压成"所有选项同时摆在桌上"，正好杀掉你要展示的跳跃感。改成时间顺序的第一人称。
> 2. **正文零 Markdown 符号**（无 `**` 无反引号）—— Padlet 不渲染，你现有卡里星号是原样显示的。可以直接整段复制粘贴。
> 3. 技术词照常出现，**每个术语后面紧跟一句人话翻译**（按你选的路线）。
> 4. 按你的三板块归位：APPEARANCE（蛋外面）/ HARDWARE（蛋里面）/ SOFTWARE（软件）。M2–M4 已从硬件挪到软件。
> 5. 修了审稿里 A1–A7 的事实问题（尤其：淡水和空气基因组最在乎的传感器现在是瞎的；土壤那颗第一次是坏的）。
>
> 尾部四字段格式照你 Batch 2 起指定的样式。
>
> **DATE 的来源（请你核一遍，我没有编，但有两条是推断的）**
>
> | ID | 我填的日期 | 依据 | 可信度 |
> |---|---|---|---|
> | RE-M2 M3 M4 | 2026.7.1 | `基因组预设与传感器推理设计.md` 与三个 JSON 的文件时间 | 高 |
> | RE-M1 | 2026.7.2 | Padlet 上的 sensor connection test 视频 `video_2026_07_02_00_54_13.mp4` | 高 |
> | RE-M9 / RE-I18 | 2026.7.4 | `硬件接线现状报告.md` 首版落款「最后更新 2026-07-04」，两件事都写在里面 | 高 |
> | RE-I17 / RE-I30 | 2026.7.5 | 报告里明写「2026-07-05 实测确认」（Clock Source）与「2026-07-05」（土壤标定、EC 接线） | 高 |
> | RE-M8 | 2026.7.2 | 外壳视频 `mmexport1782951176363.mp4` 时间戳换算约为 7 月 2 日 | 中 · **待你确认** |
> | RE-I15 | 2026.6.26 | `实物图/` 里最早一批照片是「2026年6月26日」 | 中 · **待你确认**（这是外壳照片的日期，不一定是你想清楚"为什么是蛋"的日期） |

---

# 板块 2 · APPEARANCE — Outside the Egg

---

## A1 · RE-I15

**Title:** Why an Egg — and the Two Shapes I Had to Kill First

**Body:**

I did not start with an egg. I started with a clear plastic box, because that is what you build when you are still thinking like an engineer. I put the boards in it, looked at it on my desk, and the honest reaction was: this is lab equipment. Nobody walks past lab equipment and wonders how it is doing. It reads as a machine that has readings inside it, which means the first thing anyone would ask is "so where do I see the numbers" — the exact question RE-Q1 says the project has to survive without.

So I went the other way and sketched a face. Eyes, a soft body, something with ears. It was immediately better to look at. It was also immediately Unit 2 again — my ADHD therapeutic toy — and worse, it answered the wrong question. A face invites you to ask how the object feels about you. The whole pivot in RE-I1 was away from that. I had drawn the thing I had just spent two months arguing against.

That is when the egg arrived, and it arrived as a negative decision rather than a positive one. I was not looking for the friendliest shape. I was looking for a shape that could not become a dashboard and could not become a pet. An egg has no front. It has no face to read, so you cannot make eye contact with it, so you have to read the whole body — which is exactly how the field participants described noticing their animals: not from a signal in one place, but from the overall state of the thing.

Two more shapes died on the way. A bare board on a stand, which is honest but has no presence in a room. And a screen embedded in the surface, which is a dashboard wearing a costume.

The cost I am not hiding: a sealed egg gets hot inside. The Raspberry Pi runs the emotion network continuously, and I have already measured that it stays within safe range under load — but the enclosure is closed, and I knew while I was modelling it that long sessions would need a heatsink (a metal fin that pulls heat off the chip without a fan). I printed it without one anyway, for a reason and against a deadline. That is the bill for choosing this shape, and RE-I16 is where I record that I chose not to pay it yet.

**TYPE** 🟨 INSIGHT

**DATE** 2026.6.26
**ID** RE-I15
**Status** LOAD-BEARING

---

## A5 · RE-M8

**Title:** Five Failed Shells for One Plug, and Why I Kept Printing

**Body:**

The Arduino Uno board has one USB-C socket on it, and that socket has to poke out of the egg — it is both how the board gets power and how it talks to the Raspberry Pi inside. So I needed a small printed collar around that socket: strong enough to hold the plug straight, thin enough to fit the curve of the shell.

I printed it. It did not fit. I adjusted and printed again. Did not fit. Third, fourth, fifth. Each one took most of an hour on the printer, and each one was wrong in a different way — too tight to seat the plug, too loose to hold it, wall too thick to sit flush against the curve, opening in slightly the wrong place. The sixth one fitted.

Three shortcuts were available the whole time and I want them on the record, because refusing them is the actual decision here.

I could have left the sensor board hanging outside the shell entirely. Instant success photograph, and the object in that photograph would not be the object I have been describing for eight cards.

I could have run only a power cable in and left the data out of it. That would have quietly broken the architecture in RE-I9: the two boards do not just need electricity, they need to talk. A power-only connection turns the egg into a thing that glows, not a thing that translates.

I could have glued the fifth one in place. It would have held for the presentation and then, six weeks later, the light would start flickering and I would spend three days blaming my code for a mechanical fault.

I kept the five dead shells. They are in the documentation photographs on purpose. A pile of failed plastic is more informative about how I work than one clean render, and this project has been arguing since Investigate that the seams should stay visible.

**TYPE** 🟩 MAKING

**DATE** 2026.7.2
**ID** RE-M8
**Status** DONE

---

# 板块 3 · HARDWARE — Inside the Egg

---

## H1 · RE-M1

**Title:** Two Boards, Not One — Splitting the Nerves From the Brain

**Body:**

The first hardware question was embarrassingly basic: what actually goes inside.

My instinct was one board doing everything, because one board is elegant and elegant is easier to photograph. I looked at three versions of that and none of them survived.

One Raspberry Pi doing everything. The Pi (a small full computer, about the size of a credit card) is strong enough to run the CfC emotion network I built in Investigate. But it is bad at reading a lot of cheap analogue sensors — it has no analogue inputs at all, so every single sensor would need its own converter chip. I would have spent the whole Realise window building adapters instead of building a thing.

One Arduino doing everything. The Arduino (a much simpler board, roughly a very small brain that does one job forever) is excellent at sensors — that is what it exists for. It is nowhere near powerful enough to run a neural network. Choosing it means throwing away Investigate's core, or hiding it on a server somewhere, which is the same as throwing it away.

A board that streams everything to the cloud. Modern-looking, and dead the moment the Wi-Fi drops. The object stops being a presence in the room and becomes a guest of the router. I had already watched the wild-type experiment lose continuity to a crash-and-restart seam; I was not going to design a new dependency that breaks the same way.

So: two boards. The Arduino Uno is the nervous system — it touches the world, reads the sensors, and does nothing else. The Raspberry Pi 4B is the brain — it does the feeling and the light, and never touches a sensor directly. Between them, one USB cable carrying one line of text every two seconds.

The leap here is not technical, it is about what I was willing to protect. Investigate already produced a working feeling engine. Realise's job is not to reinvent it — Realise's job is to give it hands. The moment I framed it that way, the "one elegant chip" version stopped being attractive, because elegance that erases Investigate is not progress, it is amnesia.

**TYPE** 🟩 MAKING

**DATE** 2026.7.2
**ID** RE-M1
**Status** SUPPORTING

---

## H2 · RE-M9

**Title:** Power — Can This Thing Sit Next to Soil, or Only Next to My Laptop?

**Body:**

This looked like a boring question until I noticed it decides whether the object is finished or not.

A wall charger works perfectly and ruins the claim. If the egg has a cable running to the nearest socket, it is a desk prototype, and a desk prototype cannot be placed next to a plant, a tank, or in the middle of a room, which is where the whole argument about ambient reading lives.

I tried a phone power bank next. It failed in a specific and annoying way: power banks are designed to cut out when the device stops drawing much current, so it kept switching itself off during quiet moments — exactly the moments the object is supposed to be sitting there doing very little. A power source that punishes stillness is the wrong power source for a thing whose main behaviour is stillness.

What I am using now is a 21700 battery tower module (a stack of large rechargeable cells with a board on top that outputs a steady 5V at up to 4A), connected to the Pi through pogo pins — spring-loaded contacts that press against a pad rather than plugging in, so there is no connector to snap off inside the shell. It has been powered up and verified. It matches what the Pi actually draws, and it is one object rather than a knot of cables, which matters when the whole thing has to fit inside a sealed egg.

The honest limit: batteries run out. When I write up a demonstration I have to state how long it ran on its own. "Cordless" in this project means allowed to live in the room, not immortal — and if I ever show a photograph of it sitting in soil with no cable, the caption has to say for how long.

**TYPE** 🟩 MAKING

**DATE** 2026.7.4
**ID** RE-M9
**Status** SUPPORTING

---

## H3 · RE-I30

**Title:** The Sensor Wish-List Versus What Is Actually Plugged In

**Body:**

This card exists so the shopping list and the desk never get confused with each other. For each sense the project claims, here is what I wanted, what is physically wired right now, and what I cut.

Temperature. Wanted a DS18B20 probe (a sealed metal temperature probe you can push into soil or water). What is wired is a DHT11 (a cheap combined temperature-and-humidity module) plus a BMP280 (a pressure-and-temperature chip). They work, but the DHT11 reads in whole degrees with about two degrees of error — coarse for a project whose whole idea is noticing small departures from an environment's own rhythm. Written down as a known weakness, not smoothed over.

Soil moisture. Wanted a capacitive probe — one that senses water through an insulated surface rather than by passing current between two exposed metal prongs. The cheap pronged kind corrodes and then reports nonsense, so I refused those early. I have the capacitive one, it is wired to pin A1, and it is the one sensor in this project that is genuinely calibrated: on 5 July I measured it in open air (raw value 0–4) and submerged in water (350–370) and put those two numbers into the firmware. Worth saying that the first one I bought was simply faulty. I spent a day suspecting my wiring and then my code before testing the part itself and finding it dead. Replacing it fixed everything. That day is the reason I now test the component before I debug the system.

Air and smell. Wanted a BME680 — one chip that reports temperature, humidity, pressure and VOC (volatile organic compounds, roughly "the chemical staleness of air"). What I have is the BMP280, which does not sense VOC at all. So there is currently no smell sense on this device. The field is simply absent from the data stream rather than filled with a plausible-looking zero.

Light. Wanted a BH1750 (a digital light sensor that outputs real lux values straight away). What is wired is a photoresistor — a component whose resistance changes with brightness, giving a raw number I have to convert myself with an approximate formula. Fine for showing a day-night rhythm. Not something I would put in a table of measurements.

Sound. Wanted an INMP441 (a digital microphone). The Arduino Uno cannot receive that kind of digital audio, so I switched to a MAX4466 — still a real microphone, just one that outputs a varying voltage instead of digital audio. This one is settled, not a compromise I regret. There is a task left on it: a single instantaneous reading of a microphone is meaningless, so the firmware has to sample continuously for a few tens of milliseconds and take the difference between the loudest and quietest point. That is written in my to-do list, not done.

Water chemistry. The pH probe (PH-4502C) is bought and still not wired — the pin is reserved and the firmware flag is switched off, so the field is omitted entirely rather than sent as zero. Sending zero would be read as extreme acid, which is worse than saying nothing. The TDS/EC probe (conductivity, which stands in for how much dissolved salt or fertiliser is in water) is wired and running on the manufacturer's default formula, with no calibration against known reference solutions. Marked RUNNING, not DONE.

Human presence. There was a PIR motion sensor in the early sketches, from when this was still a companion object. Removed. It answers "has someone come near" — a question about you, not about the environment. It was the last piece of the pet brief still physically attached to the board, and taking it off was the cheapest and most decisive thing I did all week.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.5
**ID** RE-I30
**Status** LOAD-BEARING

---

## H4 · RE-I18

**Title:** The Board Was Not What the Label Said

**Body:**

I bought what was sold as an Arduino Uno R3 — the standard beginner board, the one every tutorial on the internet is written for. I wired the sensors onto it, wrote the firmware, and tried to load the program onto it from the Raspberry Pi, so that the whole egg could be self-contained.

The first handshake worked. The board answered. Then the actual writing of the program failed, every single time, at exactly the same stage. I did the obvious things — different cable, different port, different speed setting — and it failed identically each time, which is the specific kind of failure that means you are wrong about something more basic than what you are testing.

When I gave up and plugged it into a Windows laptop instead, the Arduino software identified the chip as an LGT8F328, not the ATmega328P that a real Uno carries. It is a compatible replacement chip made by a different manufacturer: same pin layout, mostly the same behaviour, different silicon underneath, and — importantly — a slightly different protocol for accepting a new program. Combined with the USB-to-serial chip on this particular clone (a CH340, whose Linux driver is known to be awkward with large data transfers), that explained the failure completely.

Three ways I could have gone.

Keep insisting it is a real Uno and keep debugging against a false model. That is how you lose a week.

Throw it away and buy a genuine board. Cleaner, and it spends money and days I do not have, and it discards everything I just learned about how this specific board behaves.

Accept what it actually is, load programs onto it from the Windows laptop, and let the Raspberry Pi only read from it. That last part is what I did, and it is not a defeat — the Pi never needed to write to the Arduino in normal operation anyway. It only needed to listen. So the workflow is slightly more awkward at build time and identical at run time.

What this changed in how I work: a label on a product page is a claim, not evidence. I now check what the hardware says about itself before I trust what the seller says about it. I would rather write an ugly true sentence than a tidy false one.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.4
**ID** RE-I18
**Status** LOAD-BEARING

---

## H5 · RE-I17

**Title:** It Still Failed on the Laptop — I Blamed the Cable, the Answer Was a Dropdown

**Body:**

Read this one directly after RE-I18, because the whole point is that I thought I had already solved it.

I had just worked out that the board is an LGT8F328 clone and that I should load programs onto it from the Windows laptop rather than the Raspberry Pi. So I plugged it into the laptop expecting relief. It compiled fine and then failed while writing to the chip, throwing an error that reads "not in sync" and spitting back meaningless bytes.

Here is my detective board, in the order I actually worked through it.

The cable. Obvious first suspect, cheap to test, and cables really do fail this way. Swapped it. Same failure.

The port. Unplugged, replugged, tried every socket. Same failure.

Power. Wondered whether the board was browning out mid-write. Tried a powered connection. Same failure.

Speed. Lowered the transfer speed, because "it works until it has to move a lot of data" smells like a timing problem. This felt like the sophisticated answer. It mostly still failed.

Then the actual cause, which was in a menu. Arduino's software has a setting called Clock Source — which crystal the chip should assume it is running from, effectively how fast the board's internal heartbeat is. The software's default for this chip family is Internal 32MHz. This particular board runs from an external 16MHz crystal — the product listing said so, in a line I had read and not understood. So the software was talking to the board at one tempo while the board was keeping time at another. Every message arrived slightly out of step, which is exactly why the handshake succeeded (short, forgiving) and the bulk write failed (long, unforgiving).

I changed one dropdown from 32MHz to 16MHz. It worked immediately, and has worked every time since. Confirmed 5 July.

What I want visible here is not the fix, it is the shape of the mistake. I spent my time on the glamorous physical suspects — bad cable, bad power, bad port — because those are the failures that feel like real engineering. The actual fault was ordinary, invisible, and sitting in a menu I had never opened. The useful skill was not knowing about clock sources. It was noticing that the failure was too identical to be a physical fault, and being willing to kill my favourite theory.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.5
**ID** RE-I17
**Status** LOAD-BEARING

---

# 板块 4 · SOFTWARE — The Rules You Cannot See

> ⚠️ 这三张原本在 Batch3 的硬件批里，按你的分法**必须挂到软件板块**。基因组不是焊出来的，是一个 JSON 文件。老师如果在硬件区看到它们，会以为你为土壤和水各做了一块电路板——那正好推翻 RE-Q3 的变色龙主张。

---

## S2 · RE-M2

**Title:** The Soil Genome — Deciding What This Nature Panics About First

**Body:**

A genome in Realise is not a different machine. It is a text file — a JSON, meaning a plain list of settings a human can open and read — that says, for each of the senses the body has, how much this particular nature cares about it. Same egg, same probes, same emotion network. Different priorities.

Writing the soil one meant asking a question I could not answer from a datasheet: if this were a tomato root, what would it notice first?

Moisture came out top, and not by a small margin. I gave it the highest weight in the file, 0.9 out of 1. A root's emergency is thirst; everything else is context. Temperature next at 0.8, because roots cook and roots freeze and both are fast. Light at 0.7, which surprised me until I thought about it properly: light is not directly a root's problem, but a long bright hot stretch is what makes the ground dry out, so light is early warning rather than a threat in itself.

Then the ones I deliberately turned down. Sound sits at 0.15 — a root is not indifferent to vibration, but a noisy room is not a soil emergency, and if I had weighted it higher the object would have started reacting to me walking past, which is the pet brief crawling back in through the numbers. Air staleness at 0.6, kept in as a hint about rot rather than a main signal.

The event I want to be able to demonstrate is a combination rather than a single reading: the ground dries, the temperature climbs, and it stays bright for hours. Three independent senses agreeing. I built it that way because a single sensor drifting is usually just a sensor drifting — one reading can lie, three readings agreeing rarely do. That is also the reason the CfC network is still in this project instead of a simple threshold alarm, and it is argued properly in RE-I14.

What I have to say plainly: the actual numbers in this file are still estimated from literature, not measured in a real pot of soil. The file says so itself — there is a field near the top called _calibration_status and it currently reads "using literature-estimated defaults, not yet field-calibrated". I left that line in rather than deleting it, because RE-Q4 promises that where the thresholds come from is inspectable, and a promise you delete from the file is not a promise.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M2
**Status** RUNNING

---

## S3 · RE-M3

**Title:** The Water Genome — Reasoning Around a Sense I Do Not Have

**Body:**

The freshwater genome ran into a wall the soil one did not, and the wall turned out to be the interesting part.

The thing that actually kills a pond or a tank is oxygen dropping. I do not own a dissolved oxygen probe, and they are expensive. So the first version of this file was a lie waiting to happen: I could easily have written a number called "oxygen" and computed it from other readings, and nobody looking at a demonstration would have known.

I considered three responses honestly. Fake it in software and never mention it — no. Buy the proper probe in week one — deferred rather than abandoned, because the money and the calibration time were not there. Or admit the gap and change what kind of claim the device is making about water.

I took the third, and it changed the design rather than just the caption. Instead of asserting a state, the water genome watches for a combination that is suspicious: water temperature climbing, at high weight, 0.9 — warm water holds less oxygen, so temperature is the closest honest proxy I have — alongside pH drifting at 0.8 and conductivity moving at 0.7. Any one of those alone means very little. Together, in that pattern, they mean something is going wrong in a way that is consistent with oxygen falling.

Which gives the three natures three genuinely different relationships to their own certainty. Soil can ask the ground a direct question and get a direct answer: are you dry. Air, if the right chip is fitted, can ask directly whether it is stale. Water cannot ask its most important question at all, and has to reason sideways from things it can measure.

And I have to go further, because there is a second gap and it is worse. The two channels this genome leans on after temperature are pH and conductivity — and the pH probe is bought but still not wired (see RE-I30), while the conductivity probe is running on the manufacturer's default formula with no calibration. So the freshwater genome as written cannot be honestly demonstrated yet. It is the design, not the evidence. It is marked RUNNING for that reason and it will stay RUNNING until those two probes are real.

That distinction — I designed this versus I demonstrated this — is the same line RE-Q6 draws between designed rules and network dynamics. It is the line this whole project is trying not to blur.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M3
**Status** RUNNING

---

## S4 · RE-M4

**Title:** The Indoor Air Genome — The Room's Breath, Not Your Arrival

**Body:**

The third genome is the one where the old companion brief tried hardest to come back, and it is also the one with the biggest hole in it.

Indoor air is the niche closest to a person. The soil version sits in a pot; the water version sits in a tank; this one sits in a room with you in it. So every design instinct pulled toward making it react to you — brighten when you come home, settle when you sit down. I want that instinct on the record because it was strong and it was wrong. RE-Q2 asks whose feelings are being shown, and the answer for this genome has to be the room's, not yours. The air in a badly ventilated room is getting worse whether or not you have just walked in, and the entire point is to make that visible.

So the weights follow the room. VOC — chemical staleness in the air — is the highest at 0.9. Humidity and sound both at 0.6, because a room that is damp and echoing tells you something about ventilation. Temperature at 0.6. Moisture, pH and conductivity are all switched off entirely, weight zero, marked inactive — there is no soil and no water here for them to read.

That last bit matters more than it sounds. A channel at zero is still recorded. The sensor keeps sensing; the genome only decides that this nature does not care. That is what makes it possible later for the system to notice "these readings look like water, not air — perhaps the wrong genome is loaded" rather than being blind to it. RE-Q3 and RE-I11 argue that properly.

Now the hole, which I would rather write myself than have someone find. VOC is the channel this genome cares about most, at 0.9 — and there is no VOC sensor on the device. I have a BMP280, which reports pressure and temperature and cannot smell anything. The BME680 that would do it has not been bought. So the indoor air genome is currently a nature whose most important sense does not exist.

Which leaves the five-week window with an honest and slightly uncomfortable summary: I designed three natures and only one of them — soil — can actually be demonstrated right now, because it is the only one whose top-weighted channel is both wired and calibrated. Rather than quietly demonstrating all three on simulated data, the plan is to demonstrate soil properly and present the other two as designs with their missing organs named. RE-Q5 already committed me to that: five weeks can show translation under induced stress, not mastery of ecology. This is what that commitment costs when it is actually enforced.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M4
**Status** RUNNING

---

# 粘贴顺序

**APPEARANCE 板块：** RE-I15 → （M5 M6 M7 待写）→ RE-M8 → （I16 待写）

**HARDWARE 板块：** RE-M1 → RE-M9 → RE-I30 → RE-I18 → RE-I17 → （I19 M12 M13–M20 待写）

**SOFTWARE 板块：** （S4 开场待写）→ RE-I11 → **RE-M2 → RE-M3 → RE-M4** → I12 I13 I14 I9（待白话）

⚠️ RE-I18 必须排在 RE-I17 前面。原 Batch3 是反的，导致"我以为已经解决了、换台电脑又炸"这条时间线读不出来。

---

# STATUS 改动说明

RE-M2 / M3 / M4 我从 LOAD-BEARING 改成了 **RUNNING**。

理由：按 RE-S1 自己给的定义，RUNNING = unfinished / uncalibrated / paused on purpose。三个 JSON 文件里都写着 not yet field-calibrated，水和空气那两套最关键的探头还没接。标成 LOAD-BEARING 等于说"整个论证靠这三张卡撑着"，而它们现在撑不住。标 RUNNING 反而更强——它证明你的 STATUS 字段不是装饰，是真的在用。

---

# 下一步建议（按收益排）

1. **RE-I31 —— 那张缺失的跳跃卡。** 野生型跑在仿真世界里、日志写着 "mode": "sim" 的那一刻，你怎么从"这东西需要真的能碰到世界"跳到"那它得有个身体"。这是老师真正在找的东西，现在整份 Realise 里没有。
2. **RE-I19** —— 树莓派上印着 POWER 的那个口只能供电不能传数据。对完全不懂技术的老师是最好读的一张。
3. **RE-M12** —— 两块板之间的说话约定（一行 JSON、每两秒一次、缺的传感器直接不写这个字段而不是发 0）。「缺席就是缺席，不许拿零冒充」这条规矩本身就是论点。
4. **APPEARANCE 补 M5 M6 M7 I16** —— 外壳建模、探针口、光的漫射皮肤、封闭蛋会热。
