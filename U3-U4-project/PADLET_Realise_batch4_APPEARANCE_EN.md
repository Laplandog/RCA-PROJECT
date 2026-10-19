# Realise Padlet · Batch 4 — APPEARANCE 板块补全（流水账体）

> 接 `PADLET_Realise_batch3_REWRITE_EN.md`。本板块最终顺序：
> **RE-I15 →（本批 M5 → M6 → M7 → M10）→ RE-M8 →（本批 I16）**
>
> 体例同上：正文零 Markdown 符号、零表格、术语后跟一句人话、可直接粘贴。
>
> ⚠️ **本批有三处需要你填真实内容**，我用【】标出来了。外观这块我手里的实证最少（只有 `实物图/` 的照片和你 Padlet 上那条"5 版失败第 6 版成"的说明），我不替你编建模软件、层高、壁厚这些数字。填进去之前先别贴。

---

## A2 · RE-M5

**Title:** Modelling the Shell — Turning an Argument Into a Printable Body

**Body:**

RE-I15 decided the egg as an argument. This card is where the argument had to become a mesh — a 3D file made of triangles that a printer can actually understand — and where I found out which parts of the argument were expensive.

The brief I gave myself was short. It has to read as one continuous body rather than an assembly of parts, because RE-I15 says the whole point is that you read the entire object rather than a face or a screen. It has to open, because everything inside it is a prototype and prototypes get rewired. It has to let probes out into soil or water without the opening becoming the visual centre of the object. And it has to hold a Raspberry Pi, an Arduino, a battery tower and a ring of thirty LEDs, which between them are much less compact than the drawing suggested.

【请补：你实际用什么建模的（Blender / Fusion / Rhino / Nomad…），以及第一版是怎么长出来的——是从一个球开始拉的，还是从剖面旋转出来的。一两句就够，老师要的是"她真的动手了"这个印象。】

The first real conflict showed up immediately: a continuous surface and a serviceable interior want opposite things. Every seam I add to make it openable is a line across the body that the eye follows, and the eye following a seam is the eye reading the object as a machine again. Every seam I remove makes the inside harder to reach.

What I did not do is resolve that tension in the model. I chose to let the seam exist and to place it where the object is least likely to be looked at, and I am recording that as an unresolved compromise rather than a solved problem. RE-I15 already committed me to naming what this shape costs.

**TYPE** 🟩 MAKING

**DATE** 【请补，建议 2026.6 下旬】
**ID** RE-M5
**Status** SUPPORTING

**ATTACH：** `实物图/` 里的建模截图或早期打印照片 1–2 张。如果有软件界面的截图更好——老师看不懂模型，但看得懂"她在软件里推来推去"。

---

## A3 · RE-M6

**Title:** Shell Iteration — Where It Opens, Where the Probes Leave

**Body:**

The second round was about three holes and one lid, which sounds trivial and turned out to be where the object's honesty lives.

The lid. It has to come off without tools, because during a five-week build I open this thing constantly. It also has to close well enough that the object does not read as "a prop that has been taken apart." 【请补：你实际怎么解决的——卡扣？磁铁？螺丝？摩擦配合？】

The probe exits. The soil moisture probe and, eventually, the pH and conductivity probes have to leave the body and go into the medium. This is the one place where the object visibly admits that it is not self-contained — it has to touch something outside itself to have anything to say. I decided fairly early that I liked that rather than wanting to hide it. An egg with roots coming out of it says the right thing: this presence is reading a specific place, not broadcasting general knowledge. RE-Q1 says a person should be able to form an intuition about what the environment is going through, and a visible probe going into that environment is the cheapest possible way to communicate which environment we are talking about.

The cable exit. The Arduino's single USB-C socket has to reach the outside — that is what RE-M8 is about, and it took six printed attempts.

And the thing I got wrong: I sized these openings from the model rather than from the physical parts. 【请补：具体哪个孔第一次打出来不对，差多少。如果你记不清就删掉这段——但如果记得，这是这张卡最值钱的一句话。】

**TYPE** 🟩 MAKING

**DATE** 【请补】
**ID** RE-M6
**Status** SUPPORTING

**ATTACH：** 开盖状态的照片、探针从壳里伸出来的照片。

---

## A4 · RE-M7

**Title:** The Diffuser — Making Thirty Points of Light Into One Body

**Body:**

Inside the egg there is a ring of thirty individually controllable LEDs — WS2812 pixels, meaning each one can be told its own colour and brightness. Left bare, that is thirty bright dots, and thirty bright dots read as an appliance. A router has lights. A charger has lights. Nothing in a room full of indicator lights invites you to read it as a state.

So the shell has to do the work that the electronics cannot: turn thirty sources into one glow. That is what the diffuser is — a translucent layer that scatters light so you see the shape lit rather than the sources lighting.

Two things had to be true at once, and they pull apart. Enough scattering that you cannot count the individual pixels through the surface. Not so much scattering that the light becomes flat and dead — a completely uniform glow has no body to it, and the breathing rhythm this project depends on is much harder to read on a flat surface than on one with some depth and falloff.

【请补：你实际怎么做的漫射——是靠打印壁厚 + 白色/半透材料本身？还是加了一层内衬？打了几版才不数得出灯珠？这里有一个具体的数字或材料名，这张卡就立住了。】

Why this belongs in APPEARANCE and not in SOFTWARE: the rules deciding what colour and what rhythm are code, and they live in the software section. This card is only about whether a person across the room perceives one living surface or a strip of components. That is a materials and geometry question, and it is answered in plastic.

**TYPE** 🟩 MAKING

**DATE** 【请补】
**ID** RE-M7
**Status** SUPPORTING

**ATTACH：** 开灯的照片，最好有"没装漫射层"和"装了漫射层"的对比两张。**这一对照片是整个 APPEARANCE 板块最有说服力的东西**——不懂技术的老师一眼就懂。

---

## A4b · RE-M10

**Title:** Probe Design — The Part That Has to Leave the Body

**Body:**

Everything else in this object is protected. The probes are not, and that changes how they have to be designed.

What actually goes out. The capacitive soil moisture probe — capacitive meaning it senses water through an insulated surface rather than by passing current between two exposed metal prongs, which is why it does not corrode into nonsense after a few weeks. The conductivity probe, which is waterproof and lives on a two-pin lead. And, when it is finally wired, the pH probe, which is a glass bulb on a BNC connector — a screw-lock plug — and is by some distance the most fragile object in the whole build.

What that forces. The probes cannot be permanent, because a glass pH bulb has a shelf life and a moisture probe can simply die — mine did, on the first one I bought, which is written up in RE-I30. So the exits have to be openings the probe passes through and can be pulled back out of, not holes the probe is glued into.

The thing I have not solved. Where a cable leaves a closed shell and goes into wet soil, water travels back up the cable by capillary action. I have not made a proper seal at that boundary. For a bench demonstration over hours this does not matter. For the long-term deployment that RE-Q4 and RE-Q5 both point toward, it is a genuine failure point, and I would rather write it here than discover it in a viva.

**TYPE** 🟩 MAKING

**DATE** 2026.7.5
**ID** RE-M10
**Status** RUNNING

**ATTACH：** 探针插进土/水里的照片。挂 `硬件接线现状报告.md` 第 2 节（表里有每个探头的型号和状态）。

---

## A6 · RE-I16

**Title:** I Knew It Would Get Hot and I Printed It Anyway — Three Days Before the Deadline

**Body:**

This card is about a decision I made under time pressure and would defend again, and about the specific thing it cost.

RE-I15 chose a closed body over a vented one, and I still think that is right — a vented shell reads as equipment, and equipment is not what this object is trying to be. So this is a sealed form: two halves that meet as one continuous egg, held shut by magnets, no vent, no fan, no opening. Inside it a Raspberry Pi 4B runs the emotion network continuously, fed by a battery module delivering up to 4 amps, and a closed curved shell is close to the ideal shape for keeping heat in. I knew that while I was modelling it.

I did not design anything into the shell to deal with it. No heatsink cavity, no thermal path to the outer surface, no mounting for a metal block, no channel for air to move.

One thing I want to be precise about, because a photograph will raise it. The shell is covered in holes. It would be easy to look at it and assume that is ventilation, and easy for me to let that assumption stand.

It is not. Those holes are where the light comes out. Their positions and sizes were decided by the pattern I wanted visible from across the room, and they sit in the upper dome and around the waist — nowhere near the processor, which is low in the lower half, underneath the battery and the wiring. There is no path from the hot part of this object to any opening in it. Air is not moving through it in any direction I designed or can predict. So the accurate description is a closed body with decorative perforations, and the perforations do not help. If some incidental air exchange happens through them, that is luck, and luck is not a thermal strategy.

The reason I designed nothing is not that I overlooked it. It is that I was three days from the portfolio submission and had not started laying it out. A print of the full body takes hours. A revised body means a revised print, a revised fit check, and a revised assembly, and if it had gone wrong I would have had no object to photograph and no photographs to lay out. So I chose to print the shape I had and spend the remaining time on the submission.

That is a real trade and I want it written as one rather than dressed up. I traded the object's ability to run for long periods against having an object at all on the day it had to exist. Given the same three days I would make the same call, and it is worth noticing that this is precisely the kind of pressure that makes people quietly stop mentioning a known problem — which is exactly why it gets its own card instead of a footnote.

What I have measured: the Pi stays within its safe range under load. That test was on a bench, over hours, with the shell open. "Safe on a bench for hours" and "safe sealed inside a curved shell for a week" are different claims and I have only earned the first. Every demonstration in this Padlet runs for minutes, so nothing I show is affected — but every long-deployment ambition in RE-Q4 and RE-M26 is, and those are the ones that matter for what this object is actually for.

What the next revision does, already worked out and not yet printed. A passive heatsink — a finned metal block sitting on the processor, pulling heat away by conduction — with a mounting boss modelled into the shell so it sits properly rather than being wedged in. Passive specifically, not a fan, and the reason is not thermal. A fan is audible. An object whose entire argument is that its state should be read from the outside cannot have a whirring noise that comes on when it is working hard, because then the noise becomes the primary signal and the light becomes decoration. It would also be genuinely absurd for a device with a microphone in it to be the loudest thing in the room.

So: a known problem, a deliberate deferral for a stated reason, a solution designed and not yet built — and a shell full of holes that look like they solve it and do not. Marked RUNNING rather than SUPPORTING, because RE-S1 defines RUNNING as unfinished or paused on purpose, and this is exactly that.

**TYPE** 🟨 INSIGHT

**DATE** 【作品集提交日前 3 天 — 请填真实日期】
**ID** RE-I16
**Status** RUNNING

**ATTACH：** 挂 `硬件接线现状报告.md`（第 1 节表最后一行就是 Pi 温度实测 + 散热片待办，是你**当时就记下来了**的直接证据——这一点很重要，它证明你不是事后才想起这件事）。如果有下一版外壳的散热结构草图/建模截图，一并挂上。

> 💡 **顺带改一句 `RE-I15`：** batch3 重写版里 RE-I15 结尾写的是"这是这个形状的账单"。建议改成 "…That is the bill for choosing this shape, and RE-I16 is where I record that I chose not to pay it yet." —— 让两张卡接上，读者就看得出这是一条有下文的线，不是一句自我安慰。

---

# 本批 ATTACH 汇总

| ID | 建议附什么 | 你手上有没有 |
|---|---|---|
| RE-M5 | 建模软件截图 / 第一版打印件照片 | `实物图/` 里可能有，需你挑 |
| RE-M6 | 开盖照、探针出口照 | 需你补拍 |
| RE-M7 | **裸灯 vs 装漫射层 对比照** | ⭐ 最值得补拍的一张 |
| RE-M10 | 探针插进土/水的照片 + `硬件接线现状报告.md` | 报告有，照片需补 |
| RE-I16 | `硬件接线现状报告.md` + 下一版散热结构草图（如有） | 报告✅ 草图可选 |
| RE-I15（已写） | `实物图/` 里的外壳照片 | ✅ 有 |
| RE-M8（已写） | **五个失败小壳摆一排的合影** + `mmexport1782951176363.mp4` | ⭐ 失败件如果还没扔，务必拍 |
