# Padlet 附件包 · Plan B 野生型 Step 6–22

配套正文：`../PADLET_U3_wildtype_real_process.md`
Padlet 规则是一帖最多一个文件，所以文件名前缀 = 该帖的 Step 号，按号往对应帖子里拖即可。
`REF_` 前缀的不是任何一帖的附件，是我自己核对数据用的原始文件，可以不上传。

## 一帖一文件对照

| Step | 帖子标题（EN） | ID | 拖这个文件 |
|---|---|---|---|
| 6 | Write the program the sensor board itself runs | `AL-M27` | `Step06_sensor_firmware.ino` |
| 7 | Port the same program onto the cheap beginner board | `AL-M28` | `Step07_sensor_firmware_uno.ino` |
| 8 | Audit the parts list — the code no longer matches the plan | `AL-I10` | 无（纯反思帖） |
| 9 | Build a fake world, so the software can be tested with no hardware | `AL-M29` | `Step09_sensor_bridge.py` |
| 10 | Deliberately make the fake world boring | `AL-I11` | 无 |
| 11 | Add an eighth channel that is not a sense at all | `AL-I12` | 无 |
| 12 | Decide how raw physics turns into feeling | `AL-M30` | `Step12_life_wild.py` |
| 13 | Remove feeding too — let the body run on light and time | `AL-M31` | 无（同一文件已挂在 Step 12） |
| 14 | Build the instrument that will decide whether the experiment worked | `AL-M32` | `Step14_symbol_tracker.py` |
| 15 | First run — and it crashed in the middle of the night | `AL-M33` | `Step15_growth_milestones_wild.jsonl` |
| 16 | Discover the run had quietly overshot | `AL-I13` | `Step16_growth_status_wild_ARCHIVED_6y.json` |
| 17 | Add a stopping rule and throw away a finished run | `AL-M34` | 无（同一文件已挂在 Step 15） |
| 18 | Three of the five feelings had stopped moving | `AL-I14` | `Step18_wild_log_CAPPED_2y.jsonl` |
| 19 | It had stopped responding to the sensor meant to drive it | `AL-I15` | 建议自制一张对比表截图（见下） |
| 20 | Compare against the discarded run — the cap destroyed the phenomenon | `AL-I16` | `Step20_wild_log_ARCHIVED_6y.jsonl` |
| 21 | Audit the success score — it rewards the system for dying | `AL-I17` | `Step21_symbol_log.jsonl` |
| 22 | What the wild type actually shows, and what it does not | `AL-I18` | 无 |

## Step 19 建议自己做的那张图

两个 jsonl 有 2.5 MB，直接挂上去导师不会去读。Step 19 的论点靠一张四格表就说完了，做成图片附件比挂日志有力得多：

| | 有人在场（PIR 触发） | 没人在场 |
|---|---|---|
| **2 岁封顶那次运行** | 连接感 **26.9** | 连接感 **26.9** |
| **6 岁那次（被丢弃的）** | 连接感 **54.8** | 连接感 **27.3** |

上排=断的，下排=活的。这张表同时把 Step 19 和 Step 20 的结论讲完了。

## 关于两个 wild_log 文件的重要说明

这两个日志是**滚动窗口**，只保留最后约 5,000 帧，更早的已被覆盖。所以：

- `Step18_wild_log_CAPPED_2y.jsonl` = 干净重跑的最后 10 分钟（step 139,001–144,000，虚拟 1y11m→2y0m）
- `Step20_wild_log_ARCHIVED_6y.jsonl` = 被丢弃那次的最后 11 分钟（step 428,001–433,458，虚拟 5y11m→6y0m）

**这正是 Step 20 里承认的那个仪器缺陷**：我能证明耦合在 2 岁时不存在、6 岁时存在，但中间过程没有留下来，所以说不出它是什么时候出现的。如果导师问"你怎么知道不是一开始就有"，答案在这两个文件的 step 区间里——它们本身就是那个局限的证据。

## 数据自查用（不必上传）

| 文件 | 用途 |
|---|---|
| `REF_growth_status_wild_CAPPED_2y.json` | 2 岁那次终值：symbol_score 0.6401、structure_ratio 0.9369、n_active_clusters **1** |
| `REF_growth_milestones_wild_ARCHIVED_6y.jsonl` | 6 岁那次的阶段转换与崩溃续跑记录（两条 session_start） |
| `REF_symbol_state.json` | 聚类中心原始值——第二组中心几乎全是 ±0.99，即 Step 21 说的输出压在极值上的直接证据 |
