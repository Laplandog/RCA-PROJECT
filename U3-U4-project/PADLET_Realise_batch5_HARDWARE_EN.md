# Realise Padlet · Batch 5 — HARDWARE 板块补全（流水账体）

> 接 batch3 重写版。本板块最终顺序：
> **RE-M1 → RE-M9 → RE-I30 → RE-I18 → RE-I17 →（本批 I19 → M12 → M11 → M13 → M14 → M15 → M16 → M17 → M18 → I20 → M20 → M19 → M21 → M22 → S5）**
>
> 体例同上。本批全部内容都能在 `硬件接线现状报告.md` / `SERIAL_PROTOCOL.md` / `sensor_node.ino` / `serial_sensor.py` 里查到出处，**没有一句是我编的**。

---

## H6 · RE-I19

**Title:** Two Identical Sockets, One of Them Cannot Talk

**Body:**

This is the most ordinary mistake in the whole build and probably the easiest one for anyone to understand, which is why I want it written down properly rather than buried.

The Raspberry Pi has USB-C sockets. They look the same. One of them has the word POWER printed next to it in small letters. That one is wired only for electricity — it can feed the board, and it physically cannot carry data. The others carry both.

I plugged the Arduino into the POWER one.

The result is the cruellest possible failure mode: everything looks alive. The Arduino's light comes on. The board is clearly getting power. Nothing is broken, nothing smells hot, no error appears. There is simply no data, ever, and the software just sits there waiting for a line that will never arrive. If you do not already know this distinction exists, there is nothing on the screen or on the desk to tell you.

I lost time to it, then found the printed word, then moved one cable.

What I took from it is not "read the labels." It is that a lot of debugging time goes into problems that are invisible by construction — where the system's outward appearance is identical in the working and the broken case. That is exactly the situation this whole product is trying to fix for a different subject. A pot of soil that is drying out looks identical to a pot of soil that is fine, right up until it does not. ANIMA exists because some states have no surface. It is a decent joke on me that I spent an afternoon inside one.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.2
**ID** RE-I19
**Status** LOAD-BEARING

**ATTACH：** 挂 `硬件接线现状报告.md`（第 1 节表里那一行就是这件事）。如果能拍一张两个口并排、其中一个印着 POWER 的**特写**，这张卡的说服力直接翻倍——老师看照片就懂了。

---

## H7 · RE-M12

**Title:** Writing the Contract Before Touching a Wire

**Body:**

Before any sensor went onto a pin, I wrote a document called SERIAL_PROTOCOL.md and made it the only thing the hardware side and the software side had to agree on.

The contract is short. Every two seconds, the Arduino prints one line of JSON — JSON is just text formatted so a program can read it, and one line looks like this: temperature 22.3, moisture 55.0, light 15200, and so on. It goes over the USB cable at 115200 baud, which is simply the agreed speed both ends run at. Field names are fixed. Order does not matter.

Two clauses in that document are doing real work.

First: the Arduino must send physical units, not raw numbers. A sensor natively produces a number between 0 and 1023 which means nothing on its own. The conversion into actual degrees or actual percent happens on the Arduino, before it is sent. So the software side never has to know what kind of sensor is on the other end — it receives meaning, not voltage.

Second, and this is the one I care about: **if a sensor is not connected, the Arduino does not send that field at all.** It does not send zero. It does not send null. The field is simply absent.

That clause exists because of pH. On the pH scale, 7 is neutral and 0 is battery acid. If an unconnected pH sensor reported 0, the software would faithfully translate that into "this water is catastrophically acidic" and the light would go red, and it would be right to, given what it was told. A missing sensor pretending to be a reading is not a small bug — it is the machine confidently describing an emergency that does not exist.

So the rule is: absence stays absence. The software treats a missing field as "cannot see this right now" and feeds a neutral value, and it writes a warning to the log rather than silently smoothing over it. That single decision is the reason RE-I30 can honestly say there is no smell sense on this device instead of quietly outputting a plausible number.

Writing the contract first also meant that when the wiring took three weeks longer than planned, the software half was never blocked — it ran against simulated data in exactly the format the real thing would eventually send.

**TYPE** 🟩 MAKING

**DATE** 2026.7.1
**ID** RE-M12
**Status** LOAD-BEARING

**ATTACH：** ⭐ 直接挂 `SERIAL_PROTOCOL.md` 全文。这份文件本身就是证据——它证明你是先立规矩再动手的。

---

## H7b · RE-M11

**Title:** The Wiring Diagram Was AI-Assisted, and Here Is What I Still Had to Check

**Body:**

I used ChatGPT to generate a wiring diagram for the sensor board. I am disclosing that the same way AL-P0 discloses how the field interview instrument was built, because a tool that shapes the work should be visible in the account of the work.

What it was good for: laying out which sensor goes to which pin in a readable picture, faster than I would have drawn it, and catching that two of my sensors both wanted the same pair of pins.

What it got wrong, and what I therefore had to verify myself:

It assumed the sensors I named in the ideal specification, not the ones physically on my desk. The diagram happily drew a BME680 and a BH1750. I have a BMP280 and a photoresistor. Every pin it assigned to those two had to be redone by hand against the actual modules.

It did not know the board was an LGT8F328P clone rather than a genuine Arduino Uno, because I did not know that yet either — see RE-I18. Nothing in the diagram was wrong because of it, but it meant the diagram carried a confidence about the board that turned out to be unearned.

And it could not tell me which of the Pi's USB-C sockets carries data. That is not a diagram problem, it is a physical fact about one specific board, and it cost me an afternoon — RE-I19.

What I take from this is roughly what the field work taught me about instruments in general: the tool is fine, the disclosure is mandatory, and the verification is mine. Every pin in the final build was confirmed against the physical module and written into the pin map in RE-S5, not trusted from the picture.

**TYPE** 🟩 MAKING

**DATE** 2026.7.2
**ID** RE-M11
**Status** SUPPORTING

**ATTACH：** 那张 ChatGPT 生成的接线图（你 Padlet 上已经有一张标了 "generated by chatgpt5.5" 的）。**旁边并排放你手改后的版本**，对照最有力。

---

## H8 · RE-M13

**Title:** Wiring Light (A0) — A Sensor That Only Knows Brighter and Darker

**Body:**

The light sensor is a photoresistor on pin A0 — a small component whose electrical resistance falls as more light hits it. Wire it in a divider circuit and you get a number that goes up when the room gets brighter.

That is genuinely all it knows. It does not report lux, the actual unit of illumination. It reports a raw number that I have to convert with an approximate formula I wrote myself, and that formula is not calibrated against anything.

What I wanted was a BH1750, a digital light sensor that outputs real lux values directly, no conversion needed, no guessing. It is on the list and not bought.

Which leaves an honest split I want stated rather than fudged. Relative change over time — it is getting darker, it has been bright for six hours — is something this component reports reliably, and that is what the soil genome actually uses light for. Look at RE-M2: light is weighted 0.7 not because light is a threat to a root, but because a long bright stretch is what precedes the ground drying. For that job, a rough rising and falling curve is enough.

What I cannot do is put a lux figure in a table and call it a measurement. So the light channel gets used for rhythm and never for absolute claims, and this card is where that limit is written down so that no later demonstration card can quietly forget it.

**TYPE** 🟩 MAKING

**DATE** 2026.7.4
**ID** RE-M13
**Status** RUNNING

---

## H9 · RE-M14

**Title:** Wiring Moisture (A1) — The One Sensor That Is Actually Calibrated, and the One That Was Dead

**Body:**

This is the sensor the whole soil demonstration rests on, and it is the only channel in the project that has been calibrated against physical reality rather than estimated from literature.

It is a capacitive soil moisture probe on pin A1 — capacitive meaning it senses water through a sealed surface rather than by passing current between two exposed metal prongs. The cheap pronged kind corrodes within weeks and then reports drift as if it were data, so I ruled those out before buying anything.

One detail that cost me time and is worth knowing: this probe runs on 3.3 volts, not 5. It has a Grove connector with four wires, one of which is unused, and connecting it to 5V the way most sensors on this board are connected will damage it.

Then the actual story of this card. I wired it, and the readings were nonsense — not noisy, not drifting, just meaningless. I assumed it was me. I checked the wiring. I checked the pin assignment. I rewrote the conversion in the firmware. I checked the voltage. I spent a day working through my own possible mistakes, in order, from most likely to least.

The sensor was simply faulty. A new one, wired identically, worked immediately.

I have kept that day in the account because of what it changed rather than what it cost. I now test a component in isolation before I debug the system it sits in, and that habit is exactly the reverse of what feels natural — it feels arrogant to suspect the part before suspecting yourself. It is also what a field participant described about noticing their animal: the skill is knowing which of the possible explanations to check first, and that ordering is learned expensively.

Calibration, done 5 July: in open air the probe reads a raw value of 0 to 4. Fully submerged in water, 350 to 370. Those two numbers went into the firmware as SOIL_DRY_RAW and SOIL_WET_RAW, and everything between them is interpolated. Worth noting this particular unit reads higher when wetter, which is the opposite direction from some other models — the conversion formula is written so the direction does not matter as long as the two endpoints are correct.

**TYPE** 🟩 MAKING

**DATE** 2026.7.5
**ID** RE-M14
**Status** DONE

**ATTACH：** ⭐ 如果那颗坏的传感器还在，**拍一张两颗并排的照片**。挂 `sensor_node.ino`（里面 `SOIL_DRY_RAW` / `SOIL_WET_RAW` 两行连注释一起，是直接证据）。

---

## H10 · RE-M15

**Title:** Wiring Sound (A2) — Why One Reading of a Microphone Is Meaningless

**Body:**

The sound sensor is a MAX4466 on pin A2 — an electret microphone with an amplifier, which outputs a varying voltage rather than digital audio.

I had wanted an INMP441, a digital microphone. The Arduino Uno has no hardware support for the kind of digital audio connection that part needs, so I switched. I want to be clear that this is a settled substitution and not a compromise I regret: both parts answer the same question the project actually asks, which is roughly how much is going on around here.

The interesting part is what I got wrong about how to read it.

A microphone output is a wave. It swings above and below a middle resting value, thousands of times a second, and the loudness is how far it swings — not where it happens to be. So a single instantaneous reading of a microphone tells you nothing at all. It might catch the top of a wave during silence, or the exact midpoint during a shout. Reading it once and calling that "the sound level" is like judging how rough the sea is by measuring the water height at one random instant.

The correct approach, which is written into my firmware to-do list and not yet implemented: sample continuously for a few tens of milliseconds, keep the highest and lowest values seen in that window, and report the difference between them. That difference is the amplitude, and amplitude is loudness.

Marked RUNNING because it is a known task, not a finished one. It also matters less than it sounds for the demonstration I am actually planning, since sound is weighted 0.15 in the soil genome — a root is not troubled by a noisy room, and RE-M2 explains why I deliberately kept it low rather than letting the object start reacting to me walking past.

**TYPE** 🟩 MAKING

**DATE** 2026.7.4
**ID** RE-M15
**Status** RUNNING

---

## H11 · RE-M16

**Title:** BMP280 and DHT11 — Two Sensors Doing Half of One Sensor's Job

**Body:**

The specification asks for a BME680. That is a single chip that reports temperature, humidity, air pressure, and VOC — volatile organic compounds, which in plain terms is the chemical staleness of air, the thing you notice when you walk into a room that has been shut all day.

What is actually on the board is a BMP280 on the I2C connection (pins A4 and A5 — I2C is a two-wire arrangement that lets several chips share the same pair of wires) plus a DHT11 on pin D2.

Between them these two cover temperature and humidity, with overlap, and they cover VOC not at all. The BMP280 has no chemical sense of any kind.

Two consequences I have to live with and state.

The VOC channel does not exist. Under the contract in RE-M12, the Arduino simply omits that field, so the software knows it is blind there rather than being fed a comfortable zero. This is not cosmetic: VOC is weighted 0.9 in the indoor air genome, the single highest weight of any channel in any of my three genomes. It is written up properly in RE-M4, and it is the reason the indoor air genome cannot currently be demonstrated at all.

The DHT11 is coarse. It reports whole degrees with roughly two degrees of error. For a project whose entire premise, per RE-Q4, is noticing when an environment departs from its own recent rhythm, a sensor that cannot resolve anything finer than a degree is a real limitation. The freshwater genome weights temperature at 0.9 and treats warming as its main proxy for oxygen risk — resting that on a DHT11 is not something I would defend in a laboratory.

Both are marked as open decisions in the hardware report rather than quietly accepted, because buying a BME680 would fix both problems at once and the only reason it has not happened is money and time.

**TYPE** 🟩 MAKING

**DATE** 2026.7.4
**ID** RE-M16
**Status** RUNNING

---

## H12 · RE-M17

**Title:** Wiring Conductivity (A7) — Running on the Manufacturer's Guess

**Body:**

The conductivity probe is a TDS module on pin A7, wired on 5 July, with a waterproof probe on a two-pin lead. Conductivity means how easily electricity passes through the water, which rises with dissolved minerals — so it stands in for how much fertiliser or salt is in there. In the soil genome it separates two opposite problems that look similar from the outside: starvation, where there is nothing dissolved, and salt stress, where there is far too much.

It is wired, the firmware flag is switched on, and it produces numbers.

Those numbers are converted using the formula the manufacturer supplied in the product listing. I have not calibrated it. Proper calibration means buying standard reference solutions of known concentration — 342 and 707 parts per million are the usual pair — putting the probe in each, and adjusting the formula until the reading matches the known value. I have not bought them.

So this channel currently produces numbers that are probably in the right neighbourhood and are definitely not measurements. Marked RUNNING for that reason, and it is on the to-do list in the hardware report with the specific solutions named, so it is a defined task rather than a vague intention.

Why I wired it anyway rather than waiting: relative movement is still informative even when the absolute value is not trustworthy. If the reading climbs steadily over an hour, something is dissolving into that water, and that is true regardless of whether my conversion formula is off by fifteen percent. This is the same distinction I drew for light in RE-M13 — change is usable, absolutes are not — and it is worth noticing that I have now made that same call twice on two different channels, which suggests it is a principle rather than an excuse.

**TYPE** 🟩 MAKING

**DATE** 2026.7.5
**ID** RE-M17
**Status** RUNNING

---

## H13 · RE-M18

**Title:** pH Is Bought, Reserved, and Deliberately Not Connected

**Body:**

The pH probe — a PH-4502C board with a glass electrode on a screw-lock BNC connector — is sitting on my desk, not wired.

Pin A6 is reserved for it. The firmware has a switch called ENABLE_PH and it is set to false. Under the contract in RE-M12 that means the pH field is never sent, so the software knows it cannot see pH rather than being handed a number.

I want to be precise about why this is a card rather than an omission, because "I ran out of time" is true and is not the interesting part.

pH matters most to the freshwater genome, where it is weighted 0.8 — second only to temperature. So the genome that most needs this sensor is the one I am least able to demonstrate, which is stated plainly in RE-M3. That is not a coincidence. Water is the niche where the important variables are chemical, and chemical sensing is the expensive, fragile, calibration-hungry end of this whole project.

And there is a specific danger this card exists to prevent. On the pH scale, 7 is neutral and 0 is extreme acid. An unwired sensor that reported 0 would be read by the software as a catastrophe, the light would go red, and the demonstration would look dramatic and be entirely fictional. The contract rule about omitting absent fields was written with exactly this sensor in mind.

So: bought, reserved, switched off, and written down. The gap is visible in the account rather than papered over in the demonstration.

**TYPE** 🟩 MAKING

**DATE** 2026.7.5
**ID** RE-M18
**Status** RUNNING

---

## H14 · RE-I20

**Title:** Removing the Motion Sensor — Taking the Last Piece of the Pet Off the Board

**Body:**

There was a PIR motion sensor in the early parts list. PIR means passive infrared: it detects a warm body moving nearby. It is the component in every automatic light and every burglar alarm, and it costs almost nothing.

It was there from when this was still a companion object. The behaviour it enables is obvious and immediately appealing — you walk into the room, the egg notices you, it brightens. Everybody who has seen a prototype do that has smiled at it.

RE-I1 changed the brief and RE-Q2 sharpened the test: does the output report the environment, or audition for affection? A motion sensor cannot pass that test, because the only question it can answer is a question about you. Whether a person has come near is not a fact about the soil, the water, or the air. It is a fact about the person.

Two things make this worth its own card rather than a line in RE-I30.

The first is that it was the last piece of the abandoned brief still physically present. The pivot had been written up, argued, and cross-referenced back to AL-I19 — and this component was still sitting in the parts pile the whole time, waiting to be wired. A design decision is not finished when you have written the paragraph. It is finished when the hardware agrees with the paragraph.

The second is that it was the cheapest possible decision to reverse and I did not reverse it. It costs almost nothing, the wiring is trivial, and it would have made every demonstration more charming. It is exactly the kind of small compromise that does not look like a compromise at the time. Every subsequent mapping decision in the software section gets tested against this one: if I would not accept a motion sensor, I cannot accept a rule that does the same thing in code.

Worth noting that this pressure did not go away when the component did. RE-I13 had to explicitly define the Connection dimension so that it responds to changes in the sensed medium and not to a person arriving — and my own portfolio deck still has the old wording in it, which is a live inconsistency I need to fix rather than a solved problem.

**TYPE** 🟨 INSIGHT

**DATE** 2026.7.4
**ID** RE-I20
**Status** LOAD-BEARING

---

## H15 · RE-M20

**Title:** The Firmware — Sample, Convert, Pack, Send, Wait

**Body:**

The program running on the Arduino is deliberately the least clever thing in this project. It has one job and no opinions.

Every two seconds it does five things. Read each connected sensor. Convert each raw number into a physical unit using that channel's calibration. Assemble the results into a single line of JSON. Print that line to the USB connection. Wait.

It does not decide anything. It does not know what a genome is, or what stress means, or that a neural network exists on the other end of the cable. It does not filter, average, or smooth. That is a design decision rather than laziness: every place where meaning gets added to a number is a place where I have made a judgement, and I want all of those judgements in one part of the system where they can be read, argued with, and changed by editing a text file. Splitting the interpretation across two boards means half of the reasoning is buried in firmware that has to be reflashed from a Windows laptop to change — see RE-I17 and RE-I18 for how enjoyable that is.

The parts of it that carry actual decisions, all of them recorded elsewhere: the moisture conversion uses the two calibration endpoints from RE-M14. Channels that are not wired are controlled by simple on-off switches — ENABLE_PH is false, ENABLE_EC is true — and switched-off channels are omitted from the JSON entirely rather than sent as zero, per RE-M12. The two-second interval matches what the software expects, and the speed is fixed at 115200.

One thing that is genuinely confusing and worth naming: this program communicates at 115200, but the process of loading the program onto the board happens at 57600. Two different speeds for two different purposes on the same cable. I mixed these up more than once early on, and the failure looks identical to a hardware fault, which is a theme by now.

**TYPE** 🟩 MAKING

**DATE** 2026.7.5
**ID** RE-M20
**Status** LOAD-BEARING

**ATTACH：** ⭐ 挂 `arduino/sensor_node/sensor_node.ino`。文件顶部那段中文注释（"烧录前必读"四条）本身就是最好的过程证据——**建议你把那段翻成英文再挂**，不然老师打开是一堆看不懂的字。

---

## H16 · RE-M19

**Title:** The First Real Packet

**Body:**

After the contract, the six printed shells, the clock source, the fake Arduino, the POWER socket, the dead moisture probe, and the calibration in a glass of water — the Raspberry Pi printed a line of JSON that had come from actual sensors reading an actual room.

That is the whole card, and I want it short on purpose, because the moment itself was short and slightly anticlimactic.

What it proves is narrow and I will not inflate it. It proves the chain is continuous: physical world, sensor, Arduino, cable, Raspberry Pi. It does not prove any reading is accurate. Most of them are not — the light value is an approximation, the conductivity uses a manufacturer's formula, the temperature is coarse, and the pH and VOC fields are absent.

What it changes is the status of everything downstream. Until this moment, every piece of software in the project had only ever been tested against simulated data — and I know exactly how much that matters, because the wild-type experiment in Investigate ran on a simulated world and had to be labelled as such in every card that touched it. The seam between "this works against numbers I generated" and "this works against a room" is the seam the whole Realise phase exists to cross.

The reading code has one feature worth mentioning: if the USB connection drops mid-run, it reconnects and carries on instead of crashing. That is there because the shell is closed and the cable is not strain-relieved yet, and an object that dies when it is nudged is not a presence in a room.

**TYPE** 🟩 MAKING

**DATE** 2026.7.2
**ID** RE-M19
**Status** SUPPORTING

**ATTACH：** ⭐ 你 Padlet 上已经有的 `video_2026_07_02_00_54_13.mp4`（sensor connection test）就挂这里。再加一张**串口里滚动的 JSON 截图**——老师不用懂 JSON 也能看出"数字在动"。

---

## H17 · RE-M21

**Title:** Setting Up the Raspberry Pi, and the Password I Have Not Changed

**Body:**

The Raspberry Pi 4B is the half of the object that does the feeling. Setting it up was the least eventful part of this build: write the operating system to a memory card, boot it, connect it to the network, and from then on work on it remotely from my laptop rather than plugging a monitor into a thing that is supposed to live inside a sealed egg.

Two things are worth recording.

The first is that remote access is not a convenience here, it is a requirement of the form. RE-I15 chose a closed body. A closed body means there is no screen, no keyboard, and no way in — so every future change to the software has to arrive over the network. The shape decision quietly determined the working method.

The second is a genuine fault that I am writing down rather than fixing silently. The Pi's password is currently 12345. That is on my home network, on a device that at the moment holds nothing but sensor logs, so the actual risk today is close to nothing. But this object is described throughout this Padlet as something that lives in a room, continuously, for a long time, listening through a microphone. A permanently networked microphone in a room with a five-digit password is not a small oversight in that framing — it is a contradiction between what I say the object is and how I have actually configured it.

It is on the to-do list in the hardware report. Writing it here rather than only there is deliberate: RE-I0 refuses to let the project look stronger than it is, and this is one of the places where the gap between the described object and the built object is embarrassing rather than technical.

**TYPE** 🟩 MAKING

**DATE** 2026.7.4
**ID** RE-M21
**Status** RUNNING

---

## H18 · RE-M22

**Title:** Pi Reads Arduino — and Why the Pi Is Only Allowed to Listen

**Body:**

The connection between the two boards is deliberately one-directional. The Arduino talks. The Raspberry Pi listens. The Pi never sends anything back.

Partly this is forced. RE-I18 established that loading programs onto this particular board from the Pi does not work, so firmware changes go through a Windows laptop regardless.

But it turned out to be the right architecture rather than a workaround, and the reason is worth stating. If the Pi could talk back — could tell the Arduino to sample faster, or to ignore a channel, or to recalibrate — then the reasoning about the environment would be spread across two devices, and I would no longer be able to point at one place and say this is where the interpretation happens. RE-M20 makes the same argument from the other end. Keeping the sensing side deaf keeps it honest: it reports what is there, at a fixed rhythm, with no idea what anyone downstream wants to hear.

The listening code is defensive in three specific ways, all of which exist because of things that actually went wrong. It discards corrupted lines instead of crashing, because a half-received line at startup used to bring the whole thing down. It reconnects automatically if the USB connection drops, because the cable is not strain-relieved. And it blocks and waits rather than polling, so the rhythm of the whole system is set by the Arduino's two-second heartbeat rather than by a timer on the Pi — which matters more than it sounds, because the emotion network in the software section is a continuous-time model and is told how much real time has passed between readings.

**TYPE** 🟩 MAKING

**DATE** 2026.7.2
**ID** RE-M22
**Status** LOAD-BEARING

**ATTACH：** 挂 `serial_sensor.py`。

---

## H19 · RE-S5

**Title:** Pin Map — What Is Occupied and What Is Waiting

**Body:**

A reference card rather than an argument. This is the state of the sensor board as of 5 July.

A0 is the photoresistor, giving light as a rough relative value. A1 is the capacitive soil moisture probe, the only calibrated channel in the project. A2 is the MAX4466 microphone. A4 and A5 are the BMP280, sharing the two-wire I2C connection. D2 is the DHT11 temperature and humidity module. A7 is the conductivity probe, wired and uncalibrated. A6 is reserved for pH and is not connected.

Not present: any VOC sensor, so the air has no chemical sense. Removed on purpose: the PIR motion sensor, per RE-I20.

Reading this list against the seven-channel principle in RE-I10 gives an honest summary of where the build actually stands. Two channels are fully real — moisture and temperature. Three are real but rough — light, sound, conductivity. One is absent — VOC. One is unwired — pH.

That is what the object can currently feel. Everything the software section claims has to be read against this card.

**TYPE** ⬜ CONTEXT

**DATE** 2026.7.5
**ID** RE-S5
**Status** SUPPORTING

**ATTACH：** ⭐ 挂 `硬件接线现状报告.md` 第 2 节整张表。**强烈建议出一张图**：一张 Arduino 的俯视图，每个用到的脚标上传感器名 + 绿/黄/灰三色（绿=已标定，黄=已接未标定，灰=没接）。这张图老师十秒读完，比任何文字都强，也直接兑现你 RE-S1 里 STATUS 的承诺。我可以帮你出这张 SVG。

---

# 本批 ATTACH 汇总

| ID | 附什么 | 状态 |
|---|---|---|
| RE-I19 | ⭐ POWER 口特写照 | 需补拍 |
| RE-M12 | ⭐ `SERIAL_PROTOCOL.md` 全文 | ✅ 有 |
| RE-M11 | ChatGPT 接线图 + 你手改版并排 | Padlet 上有前者 |
| RE-M14 | ⭐ 坏/好两颗湿度传感器并排照 + `sensor_node.ino` | 照片需补 |
| RE-M20 | ⭐ `sensor_node.ino`（**顶部注释建议翻成英文**） | ✅ 有，需翻译 |
| RE-M19 | ⭐ 已有的 sensor connection 视频 + 串口 JSON 滚动截图 | 视频✅ 截图需补 |
| RE-M22 | `serial_sensor.py` | ✅ 有 |
| RE-S5 | ⭐ `硬件接线现状报告.md` + **引脚状态彩色图** | 图我可以帮你做 |
