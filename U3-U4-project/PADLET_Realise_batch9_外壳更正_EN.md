# Realise Padlet · Batch 9 — 外壳三张照片 + 措辞更正

> **更正声明：** 上一批我把"壳上有孔"写成了"蛋不是封闭的"。错了。照片 3 里它是一个**完整闭合的蛋形**——两半合起来是一条连续轮廓，靠磁铁吸住，没有开口、没有通风口、没有风扇。孔是**光的出口**，不是气孔。
>
> 这两件事不冲突，而且分清楚之后 `RE-I16` 那张卡反而更硬：**壳上有几十个孔，但它们一个都不是为散热开的。**
>
> 下面：`RE-M6` 整张重写（三次重打 + 三种磁铁），`RE-I15` / `RE-I16` / `RE-M7` 各改一段，三张照片归位。

---

# 1 · RE-M6 重写版（替换 batch4 里带【】那版）

**Title:** Three Reprints, Three Sizes of Magnet

**Body:**

The body is two halves that meet as one continuous egg. No hinge, no catch, no screws, no visible fastener. You lift the top off and put it back, and closed it reads as a single form rather than as a container with a lid.

That is held by magnets set into the rim of both halves, and getting there cost me three complete reprints and three separate orders of magnets.

Here is how that happened, because the shape of the mistake is the point.

I printed the body. I placed the magnets. Then the dimensions changed — the interior had to grow to fit what was actually going inside, which is a Raspberry Pi, a printed case for the Arduino, a battery module, and a great deal of jumper wire that takes up far more room in reality than in a model. So I reprinted at a new size. The rim is now a different thickness, which means the recess for the magnet is a different depth, which means the magnets I already own do not sit flush. Order a new size. Print again. Same thing happens.

By the third one I had three different sizes of magnet in three little bags, and the working set is the third.

What I want visible in this is that the failure was not in the magnets. It was that I kept treating the closure as a detail to be resolved after the body, when in fact the rim thickness, the magnet depth and the interior volume are one problem with three names. Each time I changed one I quietly invalidated the other two, and each time it cost a print run of several hours to find out. This is the same error as RE-M8 — sizing an opening from the model rather than from the physical part — arriving in a different disguise.

Why magnets at all, having paid for them three times.

I open this thing constantly. Any closure that punishes being opened will eventually make me stop opening it and start guessing, and guessing is how a project starts describing an object that is no longer the object on the desk. Screws mean finding a screwdriver at midnight. A printed snap fit fatigues and eventually cracks, and RE-M8 is already a card about how a badly fitting printed part becomes an intermittent fault I will later blame on my code.

And magnets do one thing the other two cannot: they let it be opened in front of somebody, in one motion, without tools. That matters more than it sounds for a project whose whole position is that its process should stay visible. An object you can lift the top off in front of a person is an object whose insides are part of what it is, rather than something sealed behind fasteners.

The lower half stands on three conical legs. It does not sit on a surface, it stands above one — which keeps the probe cable exit off the table and, more importantly, stops it reading as a device that has been placed down and starts it reading as something that is standing there.

**TYPE** 🟩 MAKING

**DATE** 【填最后一次重打的日期】
**ID** RE-M6
**Status** DONE

**ATTACH：**
- ⭐ **照片 1**（碗内特写：四颗嵌进边缘的磁铁 + 手里那一串备用磁铁）—— 手里那串就是证据，别裁掉
- ⭐ **如果三种尺寸的磁铁还在，三小堆并排拍一张**。这张的说服力和"五个失败小壳"是同一类，而且更好懂
- 照片 2（两半并排）

---

# 2 · RE-I15 改一段（batch3 重写版里的"Honest cost"）

把现在那段换成：

> The cost I am not hiding: this is a closed body. Two halves meeting as one form, held by magnets, no vent, no fan, no opening. Inside it a Raspberry Pi runs the emotion network continuously and a battery module feeds it, and a closed curved shell is close to the ideal shape for keeping heat in. I have measured that the Pi stays within safe range under load, and I still printed it without any thermal provision at all. RE-I16 is where I record why, and that I have not paid that bill yet.
>
> The shell is perforated — both halves carry a field of round holes — but those are apertures for light, not vents. Where they sit and how big they are was decided by how the light should look, not by where the heat is. A hole that happens to let some air through is not a cooling design, and calling it one afterwards would be the kind of retrofitted justification this Padlet is meant to catch.

---

# 3 · RE-I16 改两段（batch4 里那张）

把「I did not design anything into the shell to deal with it. No heatsink cavity, no thermal path...」那段之后，加一段：

> One thing I want to be precise about, because a photograph will raise it. The shell is covered in holes. It would be easy to look at it and assume that is ventilation, and easy for me to let that assumption stand.
>
> It is not. Those holes are where the light comes out. Their positions and sizes were decided by the pattern I wanted to see from across the room, and every one of them is in the upper part of the body and around the waist — nowhere near the processor, which sits low in the lower half under the battery and the wiring. There is no path from the hot part to any opening. Air is not moving through this object in any direction I designed or can predict.
>
> So the honest statement is: it is a closed body with decorative perforations, and the perforations do not help. If some incidental air exchange happens through them, that is luck, and I am not going to claim luck as a thermal strategy.

并把结尾那句改成：

> So: a known problem, a deliberate deferral for a stated reason, a solution designed and not yet built — and a shell full of holes that look like they solve it and do not. Marked RUNNING.

---

# 4 · RE-M7 改一段（batch8 那版的开头）

把"我没有做漫射层，我打了孔"那段的语气调准一点——照片 3 显示外形其实读得出一整个身体，所以张力比我原先写的小：

> Closed, the body reads as one continuous form — which is what RE-I15 asked for. What it does not do is glow as one continuous surface. The light leaves through a field of round holes drilled through both halves, so what you see from across the room is a single object carrying a pattern of lit points, not a smooth luminous shell.
>
> The obvious alternative was a diffuser — a translucent layer that scatters the light so the surface glows and the sources disappear. I did not build one. Partly that is time: perforating a printed body was something I could do in the days I had, and a properly diffusing double-wall shell was not. But having lived with it I would argue for it now.
>
> A perfectly even glow has no body. It is a lamp, and it is what every smart speaker and every air purifier already looks like — which is the exact reading RE-I15 was trying to escape. A perforated shell has depth. The holes near the strip are bright, the ones further round are dim, and as the brightness breathes the pattern moves unevenly rather than pulsing as one flat plane. It looks like something lit from inside rather than something that is a light.
>
> The open question, and it belongs to RE-P4 rather than to me: a pattern of points is a different kind of reading from a surface. I designed the mapping, so I cannot tell whether a stranger sees one body changing state or a set of dots. That is worth asking someone, and the question is not "do you like it" — it is "did you read it as one thing."

---

# 5 · 三张照片归位

| 照片 | 挂哪张卡 | 为什么是这张 |
|---|---|---|
| **照片 3** 组装好的整蛋，站在三条腿上，线从底部出来，探头在桌上亮着红灯 | ⭐ **`RE-I15`** 主图 · Padlet 封面 · `RE-S2` | **这是你第一张"成品闭合状态"的照片。** 它同时证明三件事：形是闭合连续的、孔是光孔、它是站着的不是躺着的。而且探头在桌上、线从蛋里出来——`RE-M10` 说的"这个存在必须碰到外面的东西才有话说"在这一张里是自明的 |
| **照片 2** 上下两半并排在木桌上 | ⭐ **`RE-M5`**（外壳成形）· 备选 `RE-S5` | 最干净的一张"解剖图"。一眼看出：两个半球、四颗磁铁、三条腿、两半的孔位不一样 |
| **照片 1** 碗内特写，四颗磁铁 + 手里一串备用磁铁 | ⭐ **`RE-M6`** | 手里那串磁铁就是"三次重打"的物证。**别裁掉手** |

**照片 3 建议再补一张：同机位、同角度、关灯、蛋亮着。** 一亮一灭两张并排 —— 白天它是个安静的白色物体，晚上它是一片会呼吸的光点。这一对是整个 APPEARANCE 板块的封面。

---

# 6 · 还没解决的一件事

上一批问的那个我还是要提一次，因为它牵着两张卡的论证：**照片 3 里桌上那颗探头，还是两根分开的金属叉齿 + 红色指示灯。**

`硬件接线现状报告.md` 写的是"电容式"，而 `RE-M14` 和 `RE-I30` 里我把"我拒绝了会生锈的叉齿式"写成了一个明确论点。如果实物是叉齿式，那两句话得改——改法我上一批写好了，而且改完更强（一个会漂的传感器，正好是 `RE-Q4` 要做自动校准的另一个理由）。

你确认一句就行，我去改。
