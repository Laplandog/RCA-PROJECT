# RCA Graduate Diploma — IDE Application Portfolio

**Zixun Zhou** | Royal College of Art, Graduate Diploma Design Pathway | 2026
Target programme: Innovation Design Engineering (IDE), RCA + Imperial College

**[ZIXUN_Portfolio.pdf](ZIXUN_Portfolio.pdf)** — Combined design portfolio covering both U2 and U3-U4 projects

---

## U2 — EEG-Driven Tactile Neurofeedback Device

Unit 2 (Material Culture) | March 2026

A wearable haptic neurofeedback device for ADHD self-regulation. A silicone membrane filled with iron powder sits over an electromagnetic coil array driven by Arduino, receiving real-time brainwave data from an OpenBCI Cyton EEG headset. When attention drifts, the magnetic field shifts and the iron powder clusters — the wearer feels the texture change in their palm; when focus returns, the powder disperses and the sensation normalises. Three adaptive tactile modes (alerting / soothing / interactive) switch automatically based on EEG state — a closed-loop tactile neurofeedback system.

**Stage: working prototype** — OpenBCI EEG acquisition verified, 3D-printed EEG cap assembled, Arduino electromagnetic control tested, silicone-iron-powder membrane fabricated.

**Literature gap confirmed**: no prior research has used deformation-based haptics (non-vibration) for neurofeedback (Fleury et al., 2020, Frontiers in Neuroscience).

**[Material Culture Blog (Padlet)](https://padlet.com/royal_college_of_art/zixun-zhou-meterial-culture-n0lgsgwwqyvx3gr6)**

---

## U3 & U4 — Anima: Ecological Emotional Translation Device

Unit 3 (Investigate) & Unit 4 (Realise) | June 2026

An interactive device that reads real-time environmental sensor data (temperature, moisture, light, sound, pH, etc.), interprets it through a neural network (CfC), and translates the ecological state into emotional expressions — a breathing LED light and a web-based life dashboard. Each "life" is born with a genome tied to a specific habitat, and experiences the world differently.

**Stage: functional prototype** — full software pipeline working end-to-end (sensor → emotion → expression); hardware assembled with Arduino + WS2812 LED; web dashboard serving real-time status on mobile.

## Padlet Blog

- **[Investigate Blog](https://padlet.com/royal_college_of_art/zixun-investigate-blog-pxbxtn4oec6obw16)** — U3 research process, field studies, references and concept development
- **[Realise Blog](https://padlet.com/royal_college_of_art/zixun-realise-blog-aar113u0h9evdci8)** — U4 making process, prototyping iterations, hardware build and software development

---

## Project Structure

### `U2-project/` — EEG Tactile Neurofeedback

| Path | Description |
|------|-------------|
| `实物图/` | Prototype photos — silicone membrane, iron powder tests, assembled device |
| `脑电帽模型/` | OpenBCI Mark IV EEG headset — 3D-printable STL files for all electrode mounts and casing |
| `脑机接口/` | BCI software resources — OpenBCI GUI, BrainFlow, Processing, wiring references |
| `开源脑机接口arduino资源/` | Arduino firmware resources for OpenBCI Cyton — libraries, electrode wiring diagrams, modified EEG cap STL models |
| `Vortex_Garden_Project_Proposal_v1.docx` | Original project proposal |
| `16通道脑电帽接线指南.docx` | 16-channel EEG cap wiring guide |
| `脑电帽零基础上手指南.docx` | Beginner's guide to EEG cap setup |
| `脑波采样学习计划表.xlsx` | Brainwave sampling study plan |
| `脑电帽电极位置图.html` | Interactive EEG electrode position map |
| `chladni_skin_full/` | Arduino firmware for the haptic device — controls 3 electromagnets (12V) and 4 vibration motors (3V3) with three neurofeedback modes: Focus (20Hz pulse), Relax (10s sine wave sweep), Alert (3-burst) |
| `padlet_cards_bilingual.html` | Bilingual Padlet blog cards |
| `project2.pdf` | Project documentation PDF |

> Note: large installer binaries (Arduino IDE, Processing, OpenBCI GUI, BrainFlow) are excluded from this repo.

### `U3-U4-project/` — Anima: Ecological Emotional Translation

#### Core Software Pipeline

| File | Description |
|------|-------------|
| `sensory_mapper.py` | Two-layer sensory weighting: maps raw sensor readings through comfort curves and genome-specific weights into a normalised deviation vector |
| `life_core.py` | Emotional brain — CfC (Closed-form Continuous-time) + AutoNCP neural network that takes the 8-channel sensory vector and outputs 5 emotion dimensions (valence, arousal, safety, connection, seeking) |
| `expression_mapper.py` | Translates the 5D emotional state into physical outputs: LED RGB colour and breathing rhythm |
| `led_driver.py` | Real-time WS2812 LED breathing light controller — 5 mood colours (serene/calm/alert/discomfort/threat) with smooth transitions and breathing animation |
| `led_ws2812.py` | Low-level WS2812 serial protocol driver |
| `narrative.py` | Narrative engine that converts sensor deviations into a "life diary" — written from the organism's perspective, triggered by state transitions rather than raw ticks |
| `dashboard.py` | Flask web app serving the life monitor: real-time emotional state, diary entries, life management (birth/freeze/resume/rebirth/death) on mobile browser |
| `calibration.py` | Auto-calibrates comfort zones using real deployment data, replacing literature estimates in genome files |

#### Sensor & Hardware

| File | Description |
|------|-------------|
| `serial_sensor.py` | Reads real Arduino sensor data via USB serial (JSON stream, 115200 baud) |
| `mock_sensor.py` | Simulated sensor stream for testing without hardware |
| `run_demo.py` | End-to-end demo: mock sensors → sensory mapping → CfC emotion → expression output |
| `run_live.py` | Production entry point with real serial sensor input |
| `SERIAL_PROTOCOL.md` | Arduino-Python serial communication protocol specification |
| `arduino/sensor_node/` | Arduino firmware — reads 8 environmental sensors and streams JSON over serial |

#### Genome Presets

`genomes/` — each JSON file defines a habitat-specific "genome": which sensor channels matter, their comfort zones, and baseline emotional parameters.

| Genome | Habitat |
|--------|---------|
| `freshwater.json` | Freshwater aquatic environment (cares about water temperature, pH, EC, light) |
| `indoor_air.json` | Indoor air quality (cares about VOC, humidity, temperature, sound) |
| `tomato_soil.json` | Tomato growing soil (cares about soil moisture, temperature, pH, EC) |

#### Web App

| Path | Description |
|------|-------------|
| `templates/index.html` | Main dashboard UI template |
| `static/` | PWA assets — app icons, manifest, service worker for mobile home-screen install |

#### Portfolio & Documentation

| Path | Description |
|------|-------------|
| `portfolio/` | Product design portfolio — 7-page HTML/SVG presentation (cover, system architecture, sensors, genome, expression, physical object, design principles) + project photos |
| `padlet_wildtype_attachments/` | Supplementary code and data files referenced in the Padlet blog — early firmware iterations, growth logs, symbol tracking |
| `PADLET_Realise_batch*.md` | Realise blog post drafts (appearance, hardware, software, demo, closing) |
| `PADLET_U3_*.md` | Investigate blog post drafts and research notes |
| `U3_Field_Research_5_Participants_EN.*` | U3 field research report — 5 participant user study (PDF, DOCX, MD) |
| `Genome Presets and Sensor Inference Design.pdf` | Technical design document for the genome preset system |
| `Sensory Weighting System Technical Design.pdf` | Technical design document for the sensory weighting pipeline |
