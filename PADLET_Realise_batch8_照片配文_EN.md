# Realise Padlet · Batch 8 — 五张照片的配文与归位

> 你给的六张里第五张（EEG 手绘架构）属于脑电帽项目，已忽略。
>
> **⚠️ 照片和文档有三处对不上，先读第 0 节再贴任何东西。**

---

# 0 · 照片暴露的三处冲突（必须先处理）

## 0.1 🔴 土壤湿度探头：文档说电容式，照片看着像电阻式

第一张照片里桌上那颗探头是**两根分开的金属叉齿 + 小板 + 红色指示灯**。那是典型的电阻式（YL-69 那一类）外形。而 `硬件接线现状报告.md` 写的是「**电容式**土壤湿度传感器」，我在 `RE-M14` 和 `RE-I30` 里都把「我拒绝了会生锈的叉齿式、选了电容式」写成了一个论点。

**为什么这条最危险：** 这不是一个笔误，是一张卡的整个论证。如果老师看照片看出是叉齿式，而你的卡在讲"我特意避开了叉齿式"，那不是技术问题，是可信度问题。

**请你确认是哪种**，然后：

- **如果确实是电阻式** → `RE-M14` / `RE-I30` 的那句话必须改。改法不难，而且改完更好看：「我知道电容式更耐用，但我手上是叉齿式的。它会生锈，读数会随时间漂移，所以我在**5 号做的那次标定只在标定当天有效**——这正是 `RE-Q4` 要做自动校准的另一个理由：一个会漂的传感器，更需要设备自己反复重新认识环境，而不是信一个写死的数字。」这个版本比原来强。
- **如果照片里那颗只是早期测试件、正式用的是电容式** → 保持原文，但**别把这张照片挂在 `RE-M14` 上**，会自相矛盾。

## 0.2 🟡 蛋不是封闭的——上下两半都有一圈圆孔

第六张照片看得很清楚：上盖和下碗都打了整片圆孔，光就是从这些孔里出来的。

但 `RE-I15` 和 `RE-I16` 现在写的都是 "closed / sealed egg"。这个说法照片一贴就站不住。

**好消息是改完更好。** 见下面 `RE-I16 修订` —— 「壳上有几十个孔，但它们一个都不是为散热开的」这句话比「我没留散热」有力得多：它说明你的开孔是**表达驱动的**，不是功能驱动的，而你清楚知道这个区别。

## 0.3 🟡 「漫射层」这个说法要改成「穿孔」

我在 `RE-M7` 里留的【请补：漫射靠什么实现】，照片答了：**不是漫射层，是穿孔**。灯带贴在上盖内圈，光从孔里出来，外面看到的是一片发光的点阵，不是一整块柔光面。

这和 `RE-I15` 里「glows as one soft body」有张力。下面 `RE-M7` 我重写了，把这个张力写成卡的内容而不是藏起来。

---

# 1 · 照片 6（暗光下开盖，灯带亮着）→ 全 Padlet 的头图

这张是你手上最好的一张照片，别浪费在中间。**建议一图三用：**

| 用途 | 位置 | 说明 |
|---|---|---|
| **主用** | `RE-M7` 光学 | 灯带 + 穿孔 + 光从孔里出来，一眼说明白 |
| 次用 | `RE-S2` Overview / Padlet 封面 | 整个项目的形象图 |
| 次用 | `RE-M32` 生命模型 | 如果拍一张"休眠"极暗蓝的同角度对照，两张并排 |

---

## RE-M7 最终版（替换 batch4 里那版 · 已并入 batch9 的更正）

**Title:** Light Through Holes — Not a Diffuser, a Perforated Skin

**Body:**

Inside the upper half there is a strip of individually controllable LEDs running around the inner rim. Bare, that is a row of bright dots, and a row of bright dots reads as an appliance. A router has lights. A charger has lights. Nothing in a room full of indicator lights invites you to read it as a state.

Closed, the body reads as one continuous form — two halves meeting as a single egg, which is what RE-I15 asked for. What it does not do is glow as one continuous surface. The light leaves through a field of round holes drilled through both halves, so what you see from across the room is a single object carrying a pattern of lit points, not a smooth luminous shell.

The obvious alternative was a diffuser — a translucent layer that scatters the light so the surface glows and the sources disappear. I did not build one.

Partly that is time. Perforating a printed body was something I could do in the days I had; a properly diffusing double-wall shell was not. But having lived with it I would argue for it now, and here is the argument.

A perfectly even glow has no body. It is a lamp, and it is what every smart speaker and every air purifier already looks like — which is the exact reading RE-I15 was trying to escape. A perforated shell has depth. The holes near the strip are bright, the ones further round are dim, and as the brightness breathes the whole pattern moves unevenly rather than pulsing as one flat plane. It looks like something lit from inside rather than something that is a light.

Two things I want to keep straight, because both are easy to get wrong from a photograph.

These holes are apertures, not vents. Where they sit and how large they are was decided by how the light should look, and there is no path from them to the processor. RE-I16 is the card about heat, and it says plainly that the perforations do not help with it.

And a pattern of points is a different kind of reading from a surface. I designed the mapping, so I cannot tell whether a stranger sees one body changing state or a set of dots that happen to move together. That is worth asking someone rather than deciding myself, and it belongs to RE-P4. The question is not "do you like it." It is "did you read it as one thing."

**TYPE** 🟩 MAKING

**DATE** 【填打印/装灯的真实日期】
**ID** RE-M7
**Status** DONE

**ATTACH：** ⭐ 暗光开盖那张（看得见灯带贴在上盖内圈 + 光从孔里出来）。**再补一张同机位、盖着、亮着、关灯拍的**——"里面长这样 / 外面看到的是这样"，两张并排就是这张卡的全部论证。

---

# 2 · 照片 1（白天开盖俯拍，探头在桌上）→ RE-M6 / RE-S5

这张的价值不在好看，在**它是唯一一张能看见"里面到底塞了什么"的图**：Pi、白色打印的 Arduino 外壳（就是第六版那个）、电池、一团接线、边缘的圆形磁铁。

它同时替我答了 `RE-M6` 里那个【请补：盖子怎么固定】——**照片上看是磁铁**。

---

## RE-M6 修订（替换 batch4 里带【】那版的中段）

把「【请补：你实际怎么解决的——卡扣？磁铁？螺丝？摩擦配合？】」换成：

> The lid is held by magnets set into the rim of both halves. That was chosen over screws and over a snap fit for one reason: I open this thing constantly, and any closure that punishes being opened will eventually make me stop opening it and start guessing. Screws mean finding a screwdriver at midnight. A snap fit in printed plastic fatigues and eventually cracks — and RE-M8 is already a card about how a badly fitting printed part becomes an intermittent fault that I will later blame on my code.
>
> Magnets also do something the other two do not: they let the object be opened in front of someone. That matters more than it sounds for a project whose whole position is that its process should be visible. An object you can lift the top off in one motion is an object whose insides are part of what it is, rather than something hidden behind fasteners.

**ATTACH：** ⭐ 照片 1（能看见边缘磁铁和内部堆叠）。

---

## RE-S5 补一句

在引脚表下面加：

> A photograph of the open body is attached rather than a tidy diagram, on purpose. The wiring is a tangle of jumper leads, and that is what it actually looks like at this stage. A clean diagram of this build would be a drawing of an intention.

**ATTACH：** ⭐ 照片 1。

---

# 3 · 照片 2 + 3（LED 灯带商品页 + 厂商升级卡）→ 新卡 RE-M33

这两张放一起是一张完整的卡。第二张是你买的东西（WS2812E，60 灯/米，1 米，5V，不防水，只有灯带没有控制器），第三张是厂商随货附的说明卡，上面**主动承认**旧版本的失败模式：裸露导线、端子松脱易断、普通铜芯电阻高有过热风险、双面胶会脆化。

---

## RE-M33 · 新卡

**Title:** Choosing the Light — and a Vendor Who Lists How the Old Version Failed

**Body:**

The light is a WS2812E strip: sixty individually addressable pixels per metre, one metre bought, running on 5 volts, not waterproof, sold as bare strip with no controller. The driver in RE-M27 runs thirty of them, so half the reel became the ring inside the lid and the rest is spare.

Two things about this purchase are worth a card rather than a line in a parts list.

**Bare strip, no controller, on purpose.** The version with a controller box would have been easier and would have made the light a separate product bolted into mine. Everything about how this object expresses itself — the five moods, the breathing rhythm, the unsteadiness when safety drops — is in my code, driven directly from the emotion state. A controller in between would have meant choosing from somebody else's animation menu. RE-M27 describes writing the driver from scratch for the same reason: the expression layer is the argument, and it cannot be outsourced.

**Not waterproof, and the probes go into water.** This is a real mismatch and it belongs in the account. The light lives sealed in the upper shell and the probes leave through the lower one, so nothing wet reaches the strip in normal use. But "in normal use" is doing a lot of work in that sentence, and RE-M10 already flags that I have not sealed the cable exits properly. A device intended to sit beside a tank for months would need a waterproof strip and a sealed boundary. Mine is a bench prototype and I am calling it one.

And a small thing I did not expect to find useful. The strip arrived with a card from the manufacturer describing how the previous version of the product failed: exposed wires with poor insulation, connectors that loosen and break with repeated use, thin copper with high resistance and an overheating risk, and adhesive that goes brittle. They are advertising, obviously — the card exists to tell me the new one is better. But it is also the most candid list of failure modes anyone handed me during this build, and every item on it is a way an object dies slowly rather than dramatically. Connectors that fail on the fifth reconnection are exactly the fault RE-M8 is about, and it was oddly clarifying to see a factory print it on a card. I have kept it.

**TYPE** 🟩 MAKING

**DATE** 【填收到灯带的日期】
**ID** RE-M33
**Status** DONE

**ATTACH：** 照片 2（商品页）+ 照片 3（厂商升级说明卡）。挂在 SOFTWARE 板块 `RE-M27` 之前，或 HARDWARE 板块末尾——**建议放 HARDWARE**，因为它讲的是买了什么、不是怎么驱动。

---

# 4 · 照片 4（90° 直角 USB-A 转 USB-C 数据线）→ RE-I19 + RE-M8

这张比它看起来重要。它是一根**直角、20cm、明确标 10Gbps 数据传输**的线。三件事同时说明了：

1. **直角** —— 因为蛋是弧形的，直插头顶在壳壁上会把 Arduino 那个唯一的 USB-C 口顶歪。这直接呼应 `RE-M8` 六版小壳的问题。
2. **20cm** —— 因为两块板在同一个壳里，普通 1 米线在里面会变成一团。
3. **明确写着 Data Transfer** —— 因为 `RE-I19` 那个坑。你买这根线的时候，是在**主动排除**"这根线到底能不能传数据"这个变量。

---

## RE-I19 结尾加一段

在现有正文末尾加：

> There is a small physical postscript to this. The cable now permanently inside the object is a short right-angled one, chosen with the data specification printed on the listing, and both of those are consequences of this afternoon. Right-angled because a straight plug pushes against a curved shell and stresses the Arduino's only socket — the same problem RE-M8 spent six printed attempts on. Short because two boards in one shell do not need a metre of cable coiled between them. And explicitly specified for data, because I am no longer willing to have "can this cable carry data" as an unknown in a system where the failure looks exactly like success.

**ATTACH：** ⭐ 照片 4。**如果能补一张这根线装在蛋里、直角贴着壳壁的照片，那张更好**——它同时证明了三件事。

---

# 5 · 全部照片归位速查

| 照片 | 主挂 | 次挂 | 要不要补拍 |
|---|---|---|---|
| ⭐ 6 暗光开盖亮灯 | `RE-M7` | `RE-S2` 封面 · `RE-M32` | 建议补：**盖着的、亮着的、从外面看**的同一角度 |
| 1 白天开盖俯拍 | `RE-M6`（磁铁） | `RE-S5`（内部实况） | 先确认探头是电容还是电阻式 |
| 2 灯带商品页 | `RE-M33` | — | — |
| 3 厂商升级说明卡 | `RE-M33` | — | — |
| 4 直角数据线 | `RE-I19` | `RE-M8` | 建议补：装在蛋里的样子 |
| 5 EEG 手绘 | ❌ 不属于本项目 | — | — |

---

# 6 · 还缺的三张（之前列过，照片没覆盖到）

1. **五个失败小壳摆一排** → `RE-M8`
2. **五种心情的灯光横排**（同一角度，只换颜色）→ `RE-M27` ——照片 6 已经给了你拍法：暗环境、开盖或不开盖、固定机位
3. **一镜到底：浇水/吹热风 → 灯变** → `RE-M29` / `RE-P1` / `RE-P2`

照片 6 证明你完全拍得出好照片。第 2 项按同一套灯光再拍五张就行，是投入产出比最高的一次补拍。
