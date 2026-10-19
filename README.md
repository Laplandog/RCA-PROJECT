# Anima — Ecological Emotional Translation Device

RCA Graduate Diploma, Information Experience Design (IDE)
Unit 3 (Investigate) & Unit 4 (Realise) | June 2026

An interactive device that reads real-time environmental sensor data (temperature, moisture, light, sound, pH, etc.), interprets it through a neural network (CfC), and translates the ecological state into emotional expressions — a breathing LED light and a web-based life dashboard. Each "life" is born with a genome tied to a specific habitat, and experiences the world differently.

**Stage: functional prototype** — full software pipeline working end-to-end (sensor → emotion → expression); hardware assembled with Arduino + WS2812 LED; web dashboard serving real-time status on mobile.

## Padlet Blog

- **[Investigate Blog](https://padlet.com/royal_college_of_art/zixun-investigate-blog-pxbxtn4oec6obw16)** — U3 research process, field studies, references and concept development
- **[Realise Blog](https://padlet.com/royal_college_of_art/zixun-realise-blog-aar113u0h9evdci8)** — U4 making process, prototyping iterations, hardware build and software development

## Project Structure

### `U3-U4-project/`

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
