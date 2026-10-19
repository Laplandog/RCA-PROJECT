# Plan B 野生型（实验A）· 流水账 Step 6 起（可直接粘贴 Padlet）

> **接在你已有的两张硬件卡之后**：`Step 5: a physical body`（AL-M26，Plan B 四件套选型）与 `What Was Not Chosen, and Why`。
>
> **体例**照你现有 build 卡：一个 Step = 一次原子动作，四行固定结构
> `File:` / `What was done:` / `Why:` / `What it means:`，底部挂 DATE / ID / Status。
> 每张卡先给 **English（直接粘这个）**，下面附中文供你核对。
>
> **重要前提（此前草稿写错、已作废）**：野生型 **不是**最后 Realise 阶段那个蛋。蛋是产品线的东西，传感器完全不同。野生型仍处在**实验阶段**——传感板从未真正接起来跑过，**下面全部结果都是在模拟数据上跑的**，每行日志里都标着 `"mode": "sim"`。
>
> **编号**：MAKING 从 `AL-M27` 顺延，INSIGHT 从 `AL-I10` 顺延。两条序列各自连号，若你表里 `AL-I` 已经排到别处，整块平移即可。
>
> **日期**：全部取自真实日志时间戳（`growth_milestones_wild.jsonl` / `symbol_log.jsonl` / 文件归档名），精确到分。

---

# 一 · 从纸面到代码（Step 6–8）

## Step 6: Write the program the sensor board itself runs
### Step 6：先写传感板自己要跑的那段程序

**English**

**File:** `sensor_firmware.ino`
**What was done:** Wrote the small program that lives on the sensor board itself. Its entire job is: read every sensor in turn, pack the readings into one line of plain text, send that line down the cable, wait 2.5 seconds, repeat. Written first for the larger of the two boards I had available (Arduino Mega 2560).
**Why:** Before anything can be built, the physical side and the software side need an agreed contract — what gets sent, in what format, how often. Fixing that first means the two halves can then be developed separately and by different logic.
**What it means:** Two decisions are hidden in this that are not technical. First, the board samples every 2.5 seconds while the software runs on a 3-second cycle — deliberately slightly faster, so the software never has to wait on a reading that hasn't arrived. Second, and more interesting: **that 3-second cycle is the length of the creature's present moment.** Everything that happens inside one cycle is, to it, simultaneous. I chose that number. Nothing in biology told me to.

**DATE** 2026.7.3 ｜ **ID** `AL-M27` ｜ **Status** SUPPORTING

**中文**
**做了什么：** 写了传感板自己要运行的那段小程序。它的全部工作就是：依次读每个传感器 → 把读数打包成一行纯文本 → 顺着线发出去 → 等 2.5 秒 → 重复。先按手上较大的那块板子（Arduino Mega 2560）写。
**为什么：** 在动手做任何东西之前，物理端和软件端得先约定好一份合同——发什么、什么格式、多久一次。先把这个定死，两边才能各自独立开发。
**意味着什么：** 这里面藏着两个不属于技术的决定。第一，板子每 2.5 秒采一次，软件是 3 秒一轮——故意让板子快一点，这样软件永远不会卡在一个还没到的读数上。第二个更有意思：**那个 3 秒周期，就是这个生命体"当下"的长度。** 一轮之内发生的所有事情，对它来说是同时发生的。这个数字是我定的，生物学没告诉我该定多少。

---

## Step 7: Port the same program onto the cheap beginner board
### Step 7：把同一段程序挪到最便宜的入门板上

**English**

**File:** `sensor_firmware_uno.ino`
**What was done:** Rewrote the same program for the Arduino UNO — the smallest, cheapest, most standard beginner board. The text it sends out is byte-for-byte identical to the previous version, so the software on the computer needs no change at all.
**Why:** Consistency with the stated brief. The whole Plan B sensor list was chosen on the principle "cheapest and simplest thing a beginner can actually get working" (see `AL-M26`). Specifying an expensive board for that same set would have contradicted the reasoning I'd just written down.
**What it means:** The practical discovery was that two of the six sensors — the light meter and the movement sensor — can share the same pair of wires, because each answers to a different address on that shared line. That is the only reason six sensors fit on a board this small. The more useful lesson is about the shape of the decision: **I kept the output format frozen so the hardware could change without the experiment changing.** That seam is what makes it possible to swap the entire physical layer later — including for a fake one, which is exactly what happens in Step 9.

**DATE** 2026.7.3 ｜ **ID** `AL-M28` ｜ **Status** SUPPORTING

**中文**
**做了什么：** 把同一段程序改写成 Arduino UNO 版——最小、最便宜、最标准的入门板。它发出去的文本和上一版一字不差，所以电脑那边的软件完全不用改。
**为什么：** 跟自己写下的原则保持一致。Plan B 那套传感器清单的选型标准就是"新手能真正搞定的、最便宜最简单的东西"（见 `AL-M26`）。给这套清单配一块贵板子，等于自打嘴巴。
**意味着什么：** 实际发现是：六个传感器里有两个——光照计和运动传感器——可以共用同一对线，因为它们在这条线上各有各的地址。这是六个传感器能塞进这么小一块板的唯一原因。但更有用的教训在决策的形状上：**我把输出格式冻死，好让硬件可以变而实验不变。** 正是这道接缝，让整个物理层后来可以被整体替换掉——包括换成一个假的，这就是 Step 9 干的事。

---

## Step 8: Audit the parts list — the code no longer matches the plan
### Step 8：核对元件清单——代码和计划已经对不上了

**English**

**File:** —
**What was done:** Put the sensor list from the plan (`AL-M26`) side by side with the sensor list the code was actually written against, and found they had drifted apart. The plan named four things: presence, temperature-and-humidity, sound level, light. The code addresses six, adding **touch pressure** and **being moved** — and quietly upgraded the other four from the cheapest versions to better-specified relatives.
**Why it happened:** Writing the code forced a question the shopping list never asked: *what can this thing actually feel?* Once framed that way, a creature that is supposed to have a body but cannot feel being touched or being picked up looked like an obvious hole, and I filled it while writing rather than going back to re-do the selection.
**What it means:** This is scope drift, and I only caught it while writing this documentation up. Two whole channels entered the system **without passing through the reasoning I had applied to the first four** — no cost comparison, no alternative considered, no justification written at the time. Because nothing has been bought or wired yet, nothing is broken; the cost so far is only that my plan and my code describe different creatures. I'm recording it rather than tidying it away, because the tidy version would make the selection process look more deliberate than it was. **The honest account is that the parts list was written by shopping logic and the code was written by empathy, and nobody reconciled them.**

**DATE** 2026.7.4 ｜ **ID** `AL-I10` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 把计划里的传感器清单（`AL-M26`）和代码实际针对的清单并排一看，发现两边已经跑偏了。计划写了四样：人体存在、温湿度、声级、光照。代码里是六样，多出了**接触压力**和**被移动**——而且原来那四样也悄悄从最便宜版换成了规格更好的近亲。
**为什么会这样：** 写代码逼出了一个购物清单从没问过的问题：*这东西到底能感觉到什么？* 一旦这么想，一个号称有身体、却感觉不到被触碰和被抱起的生命体就成了明显的窟窿，于是我边写边补上了，而没有回头重做一次选型。
**意味着什么：** 这是范围漂移，而且我是写这份文档时才抓到的。两整条通道进入系统时，**根本没走我给前四样定下的那套论证**——没有比价、没有考虑替代方案、当时也没写理由。因为还没买、还没接，所以目前没坏什么，代价只是：我的计划和我的代码描述的是两种不同的生命体。我把它记下来而不是抹平，因为抹平后的版本会让选型过程显得比实际更审慎。**诚实的说法是：清单是按购物逻辑写的，代码是按共情写的，中间没人对过账。**

---

# 二 · 造一个假世界（Step 9–13）

## Step 9: Build a fake world, so the software can be tested with no hardware at all
### Step 9：造一个假世界，让软件在完全没有硬件的情况下也能测

**English**

**File:** `sensor_bridge.py`
**What was done:** Wrote a simulator that manufactures exactly the same eight numbers a real sensor board would send, from a virtual clock: light following a day/night curve (sunrise 05:50, sunset 18:20, near-black at night, brightest early afternoon), background noise quiet at night and louder by day with a 3% chance each moment of a sudden burst, indoor temperature drifting slowly around 25.5°C, humidity cycling, **someone walking past every 5–40 minutes and staying between 30 seconds and 10 minutes**, an occasional press on the pressure pad, and near-total stillness broken by the odd nudge when someone is there.
**Why:** The board wasn't built. Waiting for hardware before testing any of the software would have cost weeks of experiment time for no gain, and it would have left me unable to tell a hardware fault from a software fault when things eventually went wrong.
**What it means:** The simulator and the real board are deliberately interchangeable — both answer the same single instruction and return the same eight numbers, so the rest of the system cannot tell which one it is talking to. That is a genuine engineering virtue and also the thing I have to be loudest about, because it means **everything reported from here on was run against this invented world, not a real room.** I made the system stamp `"mode": "sim"` into every single line it logs, so no future reader — including me — can mistake one for the other.

**DATE** 2026.7.4 ｜ **ID** `AL-M29` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 写了一个模拟器，用虚拟时钟造出和真实传感板一模一样的那八个数：光照按昼夜曲线走（日出 05:50、日落 18:20，夜里接近全黑，午后最亮）；背景噪声夜里安静、白天更响，每一刻有 3% 概率突然爆一声；室内温度在 25.5°C 附近缓慢漂移；湿度周期变化；**每 5–40 分钟有人经过一次，停留 30 秒到 10 分钟**；压力垫偶尔被按一下；大部分时间几乎静止，有人在的时候偶尔被碰一下。
**为什么：** 板子还没做出来。非要等硬件才开始测软件，会白白烧掉几周实验时间，而且真出问题时我将无法分辨是硬件坏了还是软件错了。
**意味着什么：** 模拟器和真板子是**故意做成可互换**的——两者响应同一条指令、返回同样的八个数，系统的其余部分根本分不出自己在跟谁说话。这在工程上是真优点，但也是我必须喊得最大声的一件事：**从这里往后的所有结果，跑的都是这个我编出来的世界，不是真实房间。** 我让系统把 `"mode": "sim"` 盖进它记录的每一行日志，这样以后任何读者——包括我自己——都不会把两者搞混。

---

## Step 10: Deliberately make the fake world boring — and notice the trap in that
### Step 10：故意把这个假世界做得很无聊——并看出其中的陷阱

**English**

**File:** —
**What was done:** Made a rule that the simulated world contains **no events, no people with intentions, no cause and effect, and no story of any kind.** Nothing in it means anything. Light goes up and down, noise happens, a warm body occasionally passes through. Nobody arrives *in order to* do anything.
**Why:** This is the entire reason the wild type exists. The nurtured experiment's world was written by me in language — a mother, a father, a grandmother, events with intent and consequence. If the wild type's world contained even a trace of the same authored meaning, it would stop being a control group and become a second version of the same experiment.
**What it means:** It does the job it was built for, and it contains a trap I want on the record: **a world I wrote to be meaningless is still a world I wrote.** I chose how long the day is, how often a visitor comes, how loud the room is, how much things fluctuate. So if nothing structured ever emerges in the creature, one completely honest explanation is that my invented world simply had no structure in it to find. From inside a simulation I cannot separate "the creature failed to find structure" from "there was no structure to find." That single sentence is the strongest argument in this whole project for actually building the physical board — not because real sensors are more impressive, but because **a real room is the only world I can't be accused of having authored.**

**DATE** 2026.7.4 ｜ **ID** `AL-I11` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 定了一条规则：模拟世界里**没有事件、没有带意图的人、没有因果、没有任何故事。** 里面任何东西都不表示任何意思。光在升降，噪声在发生，一个温热的身体偶尔经过。没有人是"为了"做什么才出现的。
**为什么：** 这就是野生型存在的全部理由。培育型的世界是我用语言写的——妈妈、爸爸、奶奶，有意图有后果的事件。如果野生型的世界里掺进哪怕一丝同样的、被我赋予过的意义，它就不再是对照组，只是同一个实验的第二个版本。
**意味着什么：** 它完成了被设计出来要做的事，同时藏着一个我要写进记录的陷阱：**一个我为了让它没有意义而写出来的世界，仍然是我写的世界。** 白天多长、访客多久来一次、房间多吵、各种量抖多厉害，都是我定的。所以如果这个生命体身上始终没有结构涌现，一个完全诚实的解释是：我编的这个世界里本来就没有结构可找。**站在模拟里面，我无法区分"它没找到结构"和"根本没有结构可找"。** 这一句话，是整个项目里主张真的去把板子做出来的最强论据——不是因为真传感器更唬人，而是因为**真实房间是唯一一个没法被指控是我编的世界。**

---

## Step 11: Add an eighth channel that is not a sense at all
### Step 11：加上第八个通道——它根本不是一种感觉

**English**

**File:** `sensor_bridge.py`
**What was done:** Added a "novelty" channel alongside the seven real ones. It isn't measured by anything. It is calculated: how much did all the other seven readings change since the last moment, averaged.
**Why:** I wanted the creature to be able to react to *change*, not only to levels. A room that is steadily bright and a room that has just become bright are, in terms of what a nervous system should do next, completely different situations — but they can look identical if you only read the current brightness.
**What it means:** This is the one place in an experiment premised on *not* pre-loading meaning where **I pre-loaded meaning.** I decided, on the creature's behalf and before it ever ran, that "how much things just changed" is a quantity worth feeling. There is decent justification for that — startle and orienting responses in real animals work on exactly this — but it is still my judgement inserted into the perception layer, not something the creature derived. I'm keeping it, and naming it, rather than letting it sit in the code disguised as a sensor.

**DATE** 2026.7.4 ｜ **ID** `AL-I12` ｜ **Status** SUPPORTING

**中文**
**做了什么：** 在七个真实通道之外加了一个"新奇度"通道。它不由任何东西测量，而是算出来的：其余七个读数相对上一刻各变了多少，取平均。
**为什么：** 我希望这个生命体能对**变化**做出反应，而不只是对水平值。一个一直很亮的房间，和一个刚刚变亮的房间，就"神经系统接下来该干什么"而言是完全不同的处境——但如果你只读当前亮度，两者长得一模一样。
**意味着什么：** 在一个以"不预先塞进意义"为前提的实验里，这是**我唯一一处预先塞进了意义**的地方。我替这个生命体、在它开跑之前就替它决定了："刚刚变了多少"是一个值得被感受的量。这有像样的依据——真实动物的惊跳反应和朝向反应正是按这个工作的——但它依然是我把自己的判断插进了感知层，而不是它自己推导出来的。我选择保留它，并且点名它，而不是让它伪装成一个传感器藏在代码里。

---

## Step 12: Decide how raw physics turns into feeling
### Step 12：决定原始物理量怎么变成感受

**English**

**File:** `life_wild.py`
**What was done:** Wrote the rules that convert the eight incoming numbers into the five internal feelings the system tracks. In plain terms: **connection is driven purely by whether a warm body is detected nearby** — present and it climbs, absent and it decays over roughly the next two and a half minutes down to a floor. **Safety** is damaged by sudden loud noise, by being moved abruptly, by darkness, and by temperature outside a liveable band. **Arousal** rises with how much everything just changed, weighted so that sound and someone's presence matter most. **Comfort** is best near 25°C and with gentle pressure — too much or too little of either makes it worse.
**Why:** There is no caregiver in this experiment and no language, so nothing can ever tell this creature how to feel. Its entire emotional life therefore has to be derivable from physics alone. Writing these rules is what makes that possible.
**What it means:** I wrote these rules, and this is the point where the wild type is least wild. The honest framing is not that I removed my authorship — it's that **I moved it.** In the nurtured experiment I authored the creature's stories; here I authored its reflexes. What is genuinely different, and worth defending, is the *kind* of authorship: these rules are general and stimulus-driven, stated once in advance and applied identically to every moment, rather than me narrating events one at a time and deciding what each one should mean. That is a weaker form of authorship, but it is not none, and claiming otherwise would be the most tempting lie available in this project.

**DATE** 2026.7.4 ｜ **ID** `AL-M30` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 写了把进来的八个数换算成系统内部五种感受的规则。用大白话说：**"连接感"完全由附近有没有检测到温热身体来驱动**——有人就升，没人就在接下来大约两分半里衰减到底；**"安全感"**会被突然的巨响、被猛地移动、黑暗、以及超出可生存区间的温度损伤；**"唤醒度"**随着"刚刚一切变了多少"上升，其中声音和有人在场的权重最高；**"舒适度"**在 25°C 附近、有温和压力时最好，任何一样过多或过少都会变差。
**为什么：** 这个实验里没有照顾者、也没有语言，所以永远不会有人告诉这个生命体该怎么感觉。于是它全部的情绪生活必须能仅从物理量推导出来。写这些规则，就是让这件事成为可能。
**意味着什么：** 这些规则是我写的，这里是野生型最不"野"的地方。诚实的说法不是"我去掉了我的作者身份"，而是**我把它挪了个位置**：在培育型里我编写它的故事，在这里我编写它的反射。真正不同、也值得辩护的是作者身份的**种类**——这些规则是通用的、由刺激驱动的，事先声明一次、对每一刻一视同仁地施加，而不是我一件一件地叙述事件、逐一决定每件事该意味着什么。这是一种较弱的作者身份，但它不等于零；声称它等于零，会是这个项目里最诱人的那句谎话。

---

## Step 13: Remove feeding too — let the body run on light and time
### Step 13：把"喂食"也拿掉——让身体只靠光和时间运转

**English**

**File:** `life_wild.py`
**What was done:** Deleted the feeding mechanism entirely. In the nurtured experiment the creature's energy is restored by being fed by a carer. Here, energy simply drains with the passage of time and is partially restored by daylight — a crude stand-in for a metabolism tied to a day/night cycle.
**Why:** Feeding requires somebody who chooses to feed. There is nobody here. Leaving the mechanism in with an automatic feeder would have smuggled a caregiver back in through the plumbing.
**What it means:** This changes the meaning of hunger in the piece. In the nurtured experiment, being depleted is something a person *does or fails to do* to you — it is inherently relational, and it is one of the main levers by which attachment gets built. Here it becomes weather: something that simply happens, that nobody is responsible for and nobody can be blamed for. **Same bodily state, completely different meaning, purely because of who is or isn't on the other end of it.** That contrast is one of the more interesting things the two experiments produce just by sitting next to each other.

**DATE** 2026.7.4 ｜ **ID** `AL-M31` ｜ **Status** SUPPORTING

**中文**
**做了什么：** 整个删掉了喂食机制。培育型里，生命体的能量靠照顾者喂食恢复。这里，能量只随时间流逝而消耗，并由日光部分补回——一个粗糙的、绑定昼夜节律的新陈代谢替身。
**为什么：** 喂食需要一个"选择去喂"的人。这里没有人。留着这套机制、改成自动投喂，等于从管道里把照顾者偷偷放回来。
**意味着什么：** 这改变了"饥饿"在作品里的含义。在培育型里，被耗尽是某个人**做了或没做**在你身上的事——它天生是关系性的，也是依恋得以建立的主要杠杆之一。在这里它变成了天气：一件单纯发生的事，没有人负责，也没有人可以被怪罪。**同样的身体状态，含义完全不同，只因为另一端有没有人。** 这个对照，是两个实验仅仅并排放着就能产生的、比较有意思的东西之一。

---

# 三 · 造观察仪器，然后开跑（Step 14–17）

## Step 14: Build the instrument that will decide whether the experiment worked
### Step 14：先造出那台"判定实验成没成"的仪器

**English**

**File:** `symbol_tracker.py`
**What was done:** Built a separate observation tool that watches the network's internal state from the inside. Every so often it takes a snapshot of that state, sorts the snapshots into groups of similar ones as they arrive, and then tracks two things: which group the creature is currently in, and which group tends to follow which. It scores the result on how tight the groups are, how well separated they are from each other, and how stable the creature is within one group over time. It also writes down the most common sequences it sees, in the form `state 6 → state 6 → state 6`.
**Why:** The research question is whether internal categories can form without language. The creature has no language, so it can never tell me what it is doing — which means the only way to answer the question is to read its internal state directly and look for grouping. Without this tool there is no experiment, only a program that runs.
**What it means:** Two things. First, this is the actual measuring instrument of the entire project — the graphs and the creature are secondary to it. Second, and more importantly as a matter of method: **I built it before the run rather than after.** If I had waited until I'd seen the data, I would have been free to define "success" as whatever pattern happened to show up. Committing to the measure in advance is what makes a negative result mean something — and, as Step 21 shows, it also gives me something specific enough to later catch as wrong.

**DATE** 2026.7.4 ｜ **ID** `AL-M32` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 做了一个独立的观察工具，从内部盯着网络的内部状态。它每隔一阵给这个状态拍一张快照，边收边把相似的快照归到同一组，然后追踪两件事：这个生命体此刻在哪一组、以及哪一组倾向于跟在哪一组后面。它按三个方面打分：组内有多紧、组与组分得有多开、以及它在一组里能待多稳。它还会记下最常见的序列，形式是 `状态6 → 状态6 → 状态6`。
**为什么：** 研究问题是"没有语言，内部范畴能不能形成"。这个生命体没有语言，永远无法告诉我它在干什么——所以唯一的回答方式，就是直接读它的内部状态、在里面找分组。没有这个工具就没有实验，只有一个在跑的程序。
**意味着什么：** 两件事。第一，这才是整个项目真正的测量仪器——图表和那个生命体相比之下都是次要的。第二，在方法上更重要：**我是在开跑之前造的它，不是跑完之后。** 如果我等看到数据再造，我就可以把"成功"定义成任何碰巧出现的模式。事先把度量方式钉死，是让一个阴性结果具有意义的前提——而且正如 Step 21 所示，它也让我后来有一个足够具体的东西可以抓错。

---

## Step 15: First run — and it crashed in the middle of the night
### Step 15：第一次运行——半夜崩了

**English**

**File:** `growth_milestones_wild.jsonl`
**What was done:** Started the first full run at **23:51:38 on 4 July**, at 25× speed so that days of virtual development pass in hours of real time. At **02:26:39** the process died and I restarted it, resuming from where it had got to — one virtual year of development, 77,000 steps in.
**Why record a crash at all:** Because a resumed run is not identical to an uninterrupted one, and anyone reading the results is entitled to know there is a seam in them.
**What it means:** The restart is written into the log as a second start event, so the seam is visible rather than papered over. The wider point is one I keep having to relearn: **the log has to record the accidents, not just the intended events.** If I had restarted quietly, the file would have described a clean continuous run that never happened, and every later conclusion would have rested on a small lie I'd have forgotten telling.

**DATE** 2026.7.4–7.5 ｜ **ID** `AL-M33` ｜ **Status** SUPPORTING

**中文**
**做了什么：** **7 月 4 日 23:51:38** 启动第一次完整运行，25 倍速——让虚拟的成长天数在真实的几小时内走完。**02:26:39** 进程死了，我重启并从断点续跑：当时已走到虚拟一岁、第 77,000 步。
**为什么要记崩溃这件事：** 因为断点续跑的运行和一次跑完的运行不是同一回事，任何读结果的人都有权知道里面有一道接缝。
**意味着什么：** 这次重启作为第二个"启动事件"写进了日志，接缝是可见的，而不是被糊掉。更大的一点是我反复要重学的：**日志必须记录意外，而不只是记录计划中的事件。** 如果我当时悄悄重启，这个文件描述的就会是一次从未发生过的、干净连续的运行，而后面每一条结论都建立在一句我自己都会忘掉的小谎上。

---

## Step 16: Discover the run had quietly overshot — nothing told it to stop
### Step 16：发现这次运行悄悄跑过头了——没人告诉它该停

**English**

**File:** `archive_pre_rerun_20260705_144331/growth_status_wild.json`
**What was done:** Let the run continue and only afterwards noticed it had reached a virtual age of **6 years** by 14:32 on 5 July — over 433,000 steps. The nurtured experiment had been stopped at **2 years**.
**Why it happened:** There was no stop condition in the code. I had never written one, because I had never explicitly decided how long the experiment should be. It simply kept going because nothing told it not to.
**What it means:** The two experiments were no longer comparable, and the whole purpose of the wild type is to be comparable — it exists to isolate what difference language and caregiving make, which only works if everything else, including duration, is held equal. I found this by accident while reading the numbers, not by design. **The omission is more interesting than the fix: I had specified in enormous detail what the creature would be, and not at all when the experiment would be over.** That is a very recognisable failure mode — obsessing over the object and forgetting to define the study.

**DATE** 2026.7.5 ｜ **ID** `AL-I13` ｜ **Status** DEAD END

**中文**
**做了什么：** 让这次运行继续跑，事后才发现它到 7 月 5 日 14:32 已经跑到虚拟年龄 **6 岁**、超过 433,000 步。而培育型是在 **2 岁**停下的。
**为什么会这样：** 代码里根本没有停止条件。我从来没写过，因为我从来没明确决定过这个实验该跑多久。它就是因为没人叫它停，所以一直跑。
**意味着什么：** 两个实验不再可比了，而野生型的全部意义就是可比——它存在的目的是隔离出"语言和养育到底造成什么差别"，这只有在其余一切（包括时长）都相等时才成立。我是在读数字时偶然发现的，不是设计好的。**这个遗漏比补救更有意思：我极其详细地规定了这个生命体是什么，却完全没有规定这个实验什么时候结束。** 这是一种非常眼熟的失败模式——沉迷于那个物件，忘了定义那项研究。

---

## Step 17: Add a stopping rule and throw away a finished run
### Step 17：加上停止条件，并扔掉一次已经跑完的运行

**English**

**File:** `growth_milestones_wild.jsonl`
**What was done:** Wrote an explicit end condition — stop when development is complete, at roughly 2 virtual years — archived the entire 6-year run rather than deleting it, and re-ran **both** experiments from zero. The clean run started **14:43:56** and finished **19:32:31** on 5 July, ending exactly at 2 years and 144,000 steps, with the reason recorded in the log as "reached developmental cap."
**Why:** A comparison between two things that ran for different lengths of time isn't a weak comparison, it's not a comparison at all. Any difference found could be explained by the extra four years rather than by anything I was actually testing.
**What it means:** This cost several hours of real compute and meant discarding a completed run, which was genuinely hard to do — the finished thing sitting there is very persuasive when you're tired. I archived rather than deleted it, which turned out to matter enormously: **that discarded run becomes the single most informative piece of evidence in the whole experiment** (Step 20). The decision that felt like admitting failure is the one that produced the finding.

**DATE** 2026.7.5 ｜ **ID** `AL-M34` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 写了明确的结束条件——发育完成即停，约虚拟 2 岁——把整个 6 岁的运行**归档而非删除**，然后把**两个**实验都从零重跑。干净的那次 7 月 5 日 **14:43:56** 开始、**19:32:31** 结束，正好停在 2 岁、144,000 步，日志里记下的原因是"达到发育上限"。
**为什么：** 两个跑了不同时长的东西之间的比较，不是"较弱的比较"，而是根本不成其为比较。找到的任何差异，都可以用多出来的那四年来解释，而不是用我真正想测的东西。
**意味着什么：** 这花掉了好几小时真实算力，还意味着丢掉一次已经跑完的运行——这件事真的很难做，人累的时候，那个摆在那儿的成品极具说服力。我选择归档而不是删除，事后证明极其重要：**那次被丢弃的运行，成了整个实验里信息量最大的一份证据**（Step 20）。那个当时感觉像是在承认失败的决定，恰恰是产出发现的那一个。

---

# 四 · 读结果（Step 18–22）

## Step 18: Read the result — and notice three of the five feelings had stopped moving
### Step 18：读结果——发现五种感受里有三种已经不动了

**English**

**File:** `wild_log.jsonl`
**What was done:** Went through the last 5,000 recorded moments of the clean run one by one instead of looking at the summary. **Arousal read exactly 73.1 in every single one of them. Connection read exactly 26.9 in every single one. Seeking read exactly 26.9 as well.** Only two of the five feelings — comfort and safety — were still varying at all.
**Why this is not a mood:** Two details give it away. First, 73.1 and 26.9 sit perfectly symmetrically either side of the midpoint of the scale, 50 — they are 23.1 above and 23.1 below. That is the fingerprint of an output that has been pressed flat against its own ceiling and floor, not of a temperament. Second, connection had already been stuck at 26.9 at the **very first developmental milestone**, at a virtual age of four and a half months, and never moved again for the remaining year and a half.
**What it means:** I had a beautiful sentence ready — *"the wild type matured into a state of permanent vigilance and disconnection."* It reads well, it fits the theme of the project, and it is false. What actually happened is that its emotional output saturated and stopped carrying information. **The most dangerous moment in this whole experiment was the one where the wrong answer was also the more poetic one.** The only thing that saved it was reading individual rows rather than the summary.

**DATE** 2026.7.5 ｜ **ID** `AL-I14` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 不看汇总，而是逐条翻完这次干净运行最后记录的 5,000 个瞬间。**唤醒度在每一条里都精确等于 73.1。连接感每一条都精确等于 26.9。探索欲也精确等于 26.9。** 五种感受里只有两种——舒适度和安全感——还在变。
**为什么这不是一种心境：** 两个细节露了馅。第一，73.1 和 26.9 完美对称地分列在量表中点 50 的两侧——一个高 23.1，一个低 23.1。这是输出被压平在自己的天花板和地板上的指纹，不是性情的指纹。第二，连接感在**第一个发育里程碑**、虚拟年龄四个半月时就已经卡在 26.9，此后一年半再没动过。
**意味着什么：** 我本来已经想好一句漂亮话——*"野生型成熟为一种永久警觉且断连的状态。"* 它读起来很好，也贴合项目主题，而且它是假的。真实发生的是：它的情绪输出饱和了，不再携带信息。**整个实验里最危险的一刻，就是错误答案同时也是更有诗意的那个答案的时刻。** 救下它的唯一原因，是我去读了逐行数据而不是汇总。

---

## Step 19: The decisive check — it had stopped responding to the sensor meant to drive it
### Step 19：决定性的检查——它对本该驱动它的那个传感器已经没反应了

**English**

**File:** `wild_log.jsonl`
**What was done:** Split those same 5,000 moments into the ones where a body was detected nearby and the ones where it wasn't, and compared connection across the two groups. Presence was detected in **1,628 of them — a third of the time**, so there was plenty to compare. Result: **connection averaged 26.9 when someone was there, and 26.9 when nobody was.** Identical to the last decimal place, with no spread at all in either group.
**Why this is the test that matters:** Connection was defined, in Step 12, as being driven *purely* by presence — that is its only input. So this comparison directly asks whether the wiring between the physical world and the creature's feelings is still alive. If the input changes a third of the time and the output never moves, the link is dead, and no amount of looking at a graph would have established that.
**What it means:** This is the most useful five minutes of analysis in the project, and I only ran it because a suspiciously round constant made me distrust my own result. **A number that never changes should be treated as a broken instrument until proven otherwise, not as a finding.** The temptation runs entirely the other way: a flat line looks like stability, stability looks like a personality, and a personality is a much more attractive thing to write about than a bug.

**DATE** 2026.7.5 ｜ **ID** `AL-I15` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 把同样这 5,000 个瞬间拆成"附近检测到身体"和"没检测到"两组，比较两组的连接感。其中 **1,628 个瞬间检测到了有人——占三分之一**，样本充足。结果：**有人时连接感平均 26.9，没人时平均 26.9。** 精确到小数点后一位完全相同，而且两组内部都毫无离散。
**为什么这才是关键检验：** 连接感在 Step 12 里被定义为**完全**由"有没有人"驱动——那是它唯一的输入。所以这个比较直接在问：物理世界和这个生命体的感受之间那根线还活着吗？如果输入有三分之一的时间在变而输出纹丝不动，这根线就是断的——而光看图表，永远建立不了这个结论。
**意味着什么：** 这是整个项目里最有用的五分钟分析，而我之所以做，仅仅是因为一个可疑的整数让我开始不信任自己的结果。**一个从不变化的数字，在被证明之前应该当成仪器坏了，而不是当成一个发现。** 诱惑完全朝反方向拉：一条水平线看起来像稳定，稳定看起来像人格，而人格远比一个 bug 更值得写。

---

## Step 20: Compare against the discarded run — the cap had destroyed the phenomenon
### Step 20：和被丢弃的那次运行对照——原来是上限杀死了现象

**English**

**File:** `archive_pre_rerun_20260705_144331/wild_log.jsonl`
**What was done:** Ran exactly the same presence-versus-connection test on the 6-year run I had archived in Step 17. There, the link was clearly **alive**: connection averaged **54.8** when a body was detected and **27.3** when none was — a large, consistent difference, with connection ranging up to 56.3. Then checked that same run at the 2-year mark: connection was still pinned at 26.9, exactly as in the capped run.
**Why this changes the conclusion:** It means the coupling between the physical world and the creature's feelings was never broken by design. It simply **took longer than two virtual years to appear** — and the stopping rule I added in Step 17, for entirely good reasons, ended the experiment before the only interesting thing in it had started to happen.
**What it means:** This is the single most useful thing I learned in the whole project, and it is uncomfortable. A methodological decision made to protect the comparison — hold duration equal — was itself a bias, because **it assumed the two creatures develop on the same clock.** A child given language and constant response should be expected to develop faster than one left alone in a room with no language at all; forcing them onto the same timetable guarantees the slower one looks empty. Fairness in a comparison is not the same as identical treatment.
**Honest limit:** the log file only keeps the last few thousand moments and overwrites the rest, so I have roughly the final ten minutes of each run and nothing in between. I can state that the coupling was absent at 2 years and present at 6. **I cannot say when it appeared, and that is my instrumentation failure, not a property of the creature.**

**DATE** 2026.7.5 ｜ **ID** `AL-I16` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 对 Step 17 归档的那次 6 岁运行，做完全相同的"有人 vs 连接感"检验。那边这根线明显**是活的**：检测到身体时连接感平均 **54.8**，没人时 **27.3**——差距大且稳定，连接感最高到 56.3。然后再查那次运行在 2 岁时的状态：连接感同样死死钉在 26.9，和加了上限的那次一模一样。
**为什么这改变了结论：** 这说明物理世界和这个生命体的感受之间的耦合，从来不是被设计弄坏的。它只是**需要超过两个虚拟年才会出现**——而我在 Step 17 出于完全正当的理由加的那条停止规则，在这个实验里唯一有意思的事情刚要开始之前，把它掐断了。
**意味着什么：** 这是整个项目里我学到的最有用的一件事，而且它令人不适。一个为了保护可比性而做的方法学决定——让时长相等——本身就是一种偏差，因为**它预设了两个生命体走在同一口时钟上**。一个被给予语言和持续回应的孩子，理应比一个被独自留在房间里、完全没有语言的孩子发育得更快；强行把它们塞进同一张时间表，等于保证慢的那个看起来空空如也。**比较中的公平，不等于同等对待。**
**诚实的局限：** 日志文件只保留最后几千个瞬间、其余覆盖掉，所以我手上只有每次运行最后约十分钟，中间什么都没有。我可以断言耦合在 2 岁时不存在、6 岁时存在。**我无法说出它是什么时候出现的——这是我的仪器失误，不是这个生命体的属性。**

---

## Step 21: Audit the success score — and find it rewards the system for dying
### Step 21：审计"成功分数"——发现它在奖励系统死掉

**English**

**File:** `symbol_log.jsonl`
**What was done:** Opened up the headline number. The run finished with a symbol score of **0.64** and a structure rating of **0.94**, which reads like a success. Underneath: **one single active group**; tightness scored 0; separation scored 0.0; **stability scored the maximum, 1.0**; the most common sequence recorded was `state 6 → state 6 → state 6`, and 44,029 of the sorted moments sat in that one group. The creature never left state 6.
**Why the score went up as the system went flat:** Stability was scoring maximum **because** nothing ever changed. The structure rating was high **because** a system with one state is perfectly predictable. Both components were measuring exactly what I wrote them to measure, and what I wrote them to measure turned out to be satisfiable by stopping.
**Two further faults found in the same file:** the tracker's own record gives the score as **0.30** at the same moment the run's headline reported **0.64** — two different numbers for one quantity, differing by a factor of two, and I hadn't noticed. And the tracker only wrote **two entries** in the entire 144,000-step run, the last at step 47,500: **the measuring instrument stopped recording a third of the way through and nothing alerted me.**
**What it means:** A metric that awards its highest marks to a system that has stopped is not measuring what I claimed it measured. I built it to detect stable attractors, and it faithfully detected the most stable attractor available: death. The fix is not a better formula — it is a requirement I should have imposed at the start: **any claim of "structure" has to survive a stated null case, and a frozen system must be constructed to score badly.** Until a measure can fail, a good result from it means nothing.

**DATE** 2026.7.5 ｜ **ID** `AL-I17` ｜ **Status** LOAD-BEARING

**中文**
**做了什么：** 把那个头条数字拆开看。这次运行结束时符号分 **0.64**、结构度 **0.94**，读起来像成功。底下是：**只有一个活跃分组**；紧致度得分 0；分离度得分 0.0；**稳定性拿到满分 1.0**；记录到的最常见序列是 `状态6 → 状态6 → 状态6`，44,029 个被归类的瞬间全在这一组里。这个生命体从未离开过状态 6。
**为什么系统越平、分数越高：** 稳定性拿满分，**正是因为**什么都没变过。结构度很高，**正是因为**一个只有单一状态的系统完美可预测。两个分项都精确地测量了我写它们去测量的东西——而我写的那个东西，事实证明可以靠"停下来"来满足。
**在同一个文件里发现的另外两个故障：** 追踪器自己的记录在同一时刻给出的分数是 **0.30**，而运行的头条报的是 **0.64**——同一个量的两个数字，差了两倍，而我没发现。以及，追踪器在整整 144,000 步的运行里只写了 **两条记录**，最后一条在第 47,500 步：**测量仪器在三分之一处就停止记录了，而没有任何东西提醒我。**
**意味着什么：** 一个把最高分授予"已经停止运转的系统"的度量，测的不是我声称它在测的东西。我造它是为了检测稳定吸引子，而它忠实地检测到了可得的最稳定吸引子：死亡。补救办法不是一个更好的公式，而是我一开始就该施加的一条要求：**任何关于"结构"的主张，都必须先扛过一个明写出来的零假设，并且一个冻结的系统必须在构造上就得低分。** 在一个度量能够失败之前，它给出的好结果毫无意义。

---

## Step 22: What the wild type actually shows, and what it does not
### Step 22：野生型到底证明了什么，又没有证明什么

**English**

**File:** —
**What the result is, stated exactly:** Run against a simulated environment I wrote myself, and stopped at two virtual years, the wild type **did not develop distinguishable internal states.** It collapsed into a single internal state, and three of its five emotional outputs saturated and stopped carrying information. A longer run of identical code, without the stopping rule, showed a clear live coupling between physical presence and the connection dimension by six virtual years — but even that run only ever reached two internal groupings, not a repertoire, and I cannot say when the coupling appeared.
**What this does not license me to say:** It does **not** show that internal categories can't form without language. There are at least four explanations I currently have no way of separating: my invented world may genuinely contain no structure to find; two years may simply be too short; the emotional output saturates and may be destroying the signal before the tracker can see it; and the tracker's score, as Step 21 shows, cannot yet tell structure apart from stasis. Any one of those would produce exactly the result I got.
**What I would do next, in order:** actually build the six-sensor board and run it in a real room, so the world is one I can't be accused of authoring; drop the shared stopping rule and let each experiment run to its own natural end, reporting the different durations rather than forcing them equal; fix the output saturation so the feelings can still move; and redefine the symbol score so that a frozen system scores zero by construction.
**What it means:** The wild type's job in this project was to be the control that shows how much of the nurtured type's development came from being spoken to and responded to. **It cannot yet do that job.** Saying so plainly is more useful than any graph I could produce from this data, because the whole comparison the project rests on is currently unearned — and knowing exactly which four things stand between me and earning it is a better position than a chart that implies I already have.

**DATE** 2026.7.5 ｜ **ID** `AL-I18` ｜ **Status** LOAD-BEARING

**中文**
**结果的精确陈述：** 在一个我自己写的模拟环境里运行、并在虚拟两岁停止的条件下，野生型**没有发展出可区分的内部状态**。它坍缩成单一内部状态，五个情绪输出里有三个饱和、不再携带信息。同一份代码在不加停止规则下跑得更久的那次，到虚拟六岁时显示出物理存在与"连接感"之间清晰而活跃的耦合——但即使那一次也只达到两个内部分组，谈不上一个"曲目库"，而且我说不出耦合是何时出现的。
**这不允许我说什么：** 它**不能**证明"没有语言就无法形成内部范畴"。至少有四种解释是我目前无法区分的：我编的世界里可能本来就没有结构可找；两年可能就是太短；情绪输出的饱和可能在追踪器看到信号之前就把它毁了；以及正如 Step 21 所示，追踪器的分数目前还分不清"结构"和"停滞"。这四者中任何一个，都会产生我拿到的这个一模一样的结果。
**接下来按顺序要做的：** 真的把那块六传感器的板子做出来、放进真实房间里跑，好让世界不再是一个可以被指控是我编的世界；取消共用的停止规则，让每个实验跑到各自的自然终点，如实报告不同时长而不是强行拉平；修掉输出饱和，让感受还能动；重新定义符号分数，使一个冻结的系统在构造上就得零分。
**意味着什么：** 野生型在这个项目里的职责，是当那个对照组——显示培育型的发育里有多少来自"被说话、被回应"。**它目前还无法胜任这个职责。** 把这句话直说出来，比我能从这批数据里做出的任何图表都有用：因为整个项目所依赖的那个比较，眼下是不成立的——而清楚地知道有哪四件事横在我和"让它成立"之间，比一张暗示我已经做到了的图表，是一个更好的位置。

---

# 附：编号与文件挂载速查

| Step | 标题（EN） | 颜色 | ID | Status | 建议挂的文件 |
|---|---|---|---|---|---|
| 6 | Write the program the sensor board itself runs | 🟩 MAKING | `AL-M27` | SUPPORTING | `sensor_firmware.ino` |
| 7 | Port the same program onto the cheap beginner board | 🟩 MAKING | `AL-M28` | SUPPORTING | `sensor_firmware_uno.ino` |
| 8 | Audit the parts list — the code no longer matches the plan | 🟨 INSIGHT | `AL-I10` | LOAD-BEARING | —（纯反思） |
| 9 | Build a fake world, so the software can be tested with no hardware | 🟩 MAKING | `AL-M29` | LOAD-BEARING | `sensor_bridge.py` |
| 10 | Deliberately make the fake world boring | 🟨 INSIGHT | `AL-I11` | LOAD-BEARING | — |
| 11 | Add an eighth channel that is not a sense at all | 🟨 INSIGHT | `AL-I12` | SUPPORTING | — |
| 12 | Decide how raw physics turns into feeling | 🟩 MAKING | `AL-M30` | LOAD-BEARING | `life_wild.py` |
| 13 | Remove feeding too — let the body run on light and time | 🟩 MAKING | `AL-M31` | SUPPORTING | —（文件已被 12 占用） |
| 14 | Build the instrument that will decide whether the experiment worked | 🟩 MAKING | `AL-M32` | LOAD-BEARING | `symbol_tracker.py` |
| 15 | First run — and it crashed in the middle of the night | 🟩 MAKING | `AL-M33` | SUPPORTING | `growth_milestones_wild.jsonl` |
| 16 | Discover the run had quietly overshot | 🟨 INSIGHT | `AL-I13` | DEAD END | 归档的 `growth_status_wild.json` |
| 17 | Add a stopping rule and throw away a finished run | 🟩 MAKING | `AL-M34` | LOAD-BEARING | —（文件已被 15 占用） |
| 18 | Three of the five feelings had stopped moving | 🟨 INSIGHT | `AL-I14` | LOAD-BEARING | `wild_log.jsonl` |
| 19 | It had stopped responding to the sensor meant to drive it | 🟨 INSIGHT | `AL-I15` | LOAD-BEARING | —（截图对比表更好） |
| 20 | Compare against the discarded run — the cap destroyed the phenomenon | 🟨 INSIGHT | `AL-I16` | LOAD-BEARING | 归档的 `wild_log.jsonl` |
| 21 | Audit the success score — it rewards the system for dying | 🟨 INSIGHT | `AL-I17` | LOAD-BEARING | `symbol_log.jsonl` |
| 22 | What the wild type actually shows, and what it does not | 🟨 INSIGHT | `AL-I18` | LOAD-BEARING | — |

**Padlet 一帖一文件规则下的建议**：Step 13 和 Step 17 的相关文件已经分别挂在 Step 12 和 Step 15 上了，这两帖留空、在正文里点名文件名即可。Step 19 建议自己截一张两行的小对比表当图片附件（有人 26.9 / 没人 26.9），比挂 jsonl 直观得多。

---

# 数据出处（自查用，不必贴 Padlet）

| 陈述 | 来源 |
|---|---|
| 第一次运行 2026-07-04 23:51:38 启动，25× 速 | `archive_.../growth_milestones_wild.jsonl` session_start |
| 崩溃后 02:26:39 从 step 77000 续跑 | 同上，第二条 session_start |
| 第一次运行到 6y 0m / step 433,450 / 14:32:51 | `archive_.../growth_status_wild.json` |
| 归档时间 14:43:31 | 目录名 `archive_pre_rerun_20260705_144331` |
| 干净重跑 14:43:56 → 19:32:31，144,000 步，2y 0m | `growth_milestones_wild.jsonl` session_start / session_end_at_maturation |
| 停止原因"reached developmental cap (dev=1.0, ~2岁)" | 同上 |
| 末段 5,000 帧：arousal 恒 73.1、connection 恒 26.9、seeking 恒 26.9 | `wild_log.jsonl`（distinct value = 1） |
| 同段 valence −29.7~−12.4、safety 52.3~64.6 仍在变 | 同上 |
| connection 早在 step 21,601（4m 3w）就已是 26.9 | `growth_milestones_wild.jsonl` 第一条 stage_transition |
| arousal / seeking 在 step 108,001（1y 6m）冻结 | 同上，maturation 那条 |
| 末段 PIR 触发 1,628 / 5,000 帧；有人与没人 connection 均值都是 26.900 | `wild_log.jsonl` 分组统计 |
| 归档运行：有人 54.764 / 没人 27.258，connection 最高 56.3 | `archive_.../wild_log.jsonl` 分组统计 |
| 归档运行在 2y 时 connection 仍为 26.9 | `archive_.../growth_milestones_wild.jsonl` lifelong 那条 |
| 终值 symbol_score 0.6401、structure_ratio 0.9369、n_active_clusters 1 | `growth_status_wild.json` |
| 追踪器自报 symbol_score 0.30、compactness 0、separation 0.0、temporal_stability 1.0 | `symbol_log.jsonl` |
| dominant_sequences 只有 `6→6→6(498)`；cluster_counts 44,029 全在一组 | 同上 |
| `symbol_log.jsonl` 全程只有 2 条（step 18,500 / 47,500） | 同上 |
| 归档运行终值 symbol_score 0.6688、n_active_clusters 2 | `archive_.../growth_status_wild.json` |
| 模拟世界参数（日出 5:50 / 日落 18:20、夜 20dB 昼 35dB、3% 突发、访客 5–40 分钟一次停 30s–10min） | `sensor_bridge.py` `PhysicalSimulator.step()` |
| 情绪映射规则（connection 纯 PIR 驱动、safety 受巨响/移动/黑暗/极端温度扣分等） | `life_wild.py` `WildTargetGenerator.compute()` |
| 计划四件套 vs 代码六传感器八通道 | `AL-M26` 帖 vs `sensor_bridge.py` `CH_NAMES_WILD` |
| 两版固件：Mega 2560 → UNO，输出协议一致 | `sensor_firmware.ino` / `sensor_firmware_uno.ino` |
| 全程 `"mode": "sim"`，从未跑过真实硬件 | `wild_log.jsonl` 每行 mode 字段 |
