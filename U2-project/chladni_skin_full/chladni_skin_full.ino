// Chladni Skin - 完整控制
// 3x 电磁铁 (12V) + 4x 振动马达 (3V3)
// 三种神经反馈模式: Focus / Relax / Alert

// === 电磁铁引脚 (12V) ===
const int MAG_1 = 5;   // Q1
const int MAG_2 = 6;   // Q2
const int MAG_3 = 7;   // Q3

// === 振动马达引脚 (3V3) ===
const int VM_CENTER = 15;  // M1 掌心 劳宫 PC-8
const int VM_THENAR = 18;  // M2 大鱼际 鱼际 LU-10 (Board R j15-17)
const int VM_HYPO   = 17;  // M3 小鱼际 少府 HT-8 (Board R j11-13)
const int VM_WRIST  = 16;  // M4 掌根 大陵 PC-7 (Board L c15-17)

// 马达最低启动PWM (3V rail, ~2.3V启动 ≈ 195/255)
const int VM_MIN = 195;
const int VM_MAX = 255;

// 模式状态
int currentMode = 0; // 0=off, 1=focus, 2=relax, 3=alert
unsigned long lastUpdate = 0;
int waveStep = 0;

void setup() {
  Serial.begin(115200);

  // 电磁铁
  pinMode(MAG_1, OUTPUT);
  pinMode(MAG_2, OUTPUT);
  pinMode(MAG_3, OUTPUT);
  digitalWrite(MAG_1, LOW);
  digitalWrite(MAG_2, LOW);
  digitalWrite(MAG_3, LOW);

  // 振动马达
  pinMode(VM_CENTER, OUTPUT);
  pinMode(VM_THENAR, OUTPUT);
  pinMode(VM_HYPO, OUTPUT);
  pinMode(VM_WRIST, OUTPUT);
  analogWrite(VM_CENTER, 0);
  analogWrite(VM_THENAR, 0);
  analogWrite(VM_HYPO, 0);
  analogWrite(VM_WRIST, 0);

  Serial.println("=== Chladni Skin Control ===");
  Serial.println("Commands:");
  Serial.println("  1/2/3    = toggle electromagnet 1/2/3");
  Serial.println("  m1/m2/m3/m4 = toggle motor 1/2/3/4");
  Serial.println("  f = FOCUS mode");
  Serial.println("  r = RELAX mode");
  Serial.println("  t = ALERT mode (3-burst test)");
  Serial.println("  s = ALL OFF");
}

void loop() {
  handleSerial();

  switch (currentMode) {
    case 1: runFocus(); break;
    case 2: runRelax(); break;
    case 3: runAlert(); break;
  }
}

// ============ 串口控制 ============
void handleSerial() {
  if (!Serial.available()) return;

  String input = Serial.readStringUntil('\n');
  input.trim();

  if (input == "1") {
    digitalWrite(MAG_1, !digitalRead(MAG_1));
    Serial.print("Mag1: "); Serial.println(digitalRead(MAG_1) ? "ON" : "OFF");
  }
  else if (input == "2") {
    digitalWrite(MAG_2, !digitalRead(MAG_2));
    Serial.print("Mag2: "); Serial.println(digitalRead(MAG_2) ? "ON" : "OFF");
  }
  else if (input == "3") {
    digitalWrite(MAG_3, !digitalRead(MAG_3));
    Serial.print("Mag3: "); Serial.println(digitalRead(MAG_3) ? "ON" : "OFF");
  }
  else if (input == "m1") {
    toggleMotor(VM_CENTER, "M1-Center");
  }
  else if (input == "m2") {
    toggleMotor(VM_THENAR, "M2-Thenar");
  }
  else if (input == "m3") {
    toggleMotor(VM_HYPO, "M3-Hypo");
  }
  else if (input == "m4") {
    toggleMotor(VM_WRIST, "M4-Wrist");
  }
  else if (input == "f") {
    allOff();
    currentMode = 1;
    Serial.println(">>> FOCUS MODE <<<");
    Serial.println("20Hz pulse on center motor, alternating thenar/hypo");
  }
  else if (input == "r") {
    allOff();
    currentMode = 2;
    waveStep = 0;
    Serial.println(">>> RELAX MODE <<<");
    Serial.println("Slow wave: thenar -> center -> hypo -> wrist (10s cycle)");
  }
  else if (input == "t") {
    allOff();
    currentMode = 3;
    waveStep = 0;
    lastUpdate = millis();
    Serial.println(">>> ALERT MODE <<<");
    Serial.println("3 sharp bursts on all motors");
  }
  else if (input == "s") {
    allOff();
    currentMode = 0;
    Serial.println("ALL OFF");
  }
}

void toggleMotor(int pin, const char* name) {
  static bool states[4] = {false, false, false, false};
  int idx;
  if (pin == 15) idx = 0;
  else if (pin == 18) idx = 1;
  else if (pin == 17) idx = 2;
  else idx = 3;
  states[idx] = !states[idx];
  analogWrite(pin, states[idx] ? VM_MAX : 0);
  Serial.print(name); Serial.print(": ");
  Serial.println(states[idx] ? "ON" : "OFF");
}

// ============ FOCUS mode ============
// 20Hz 脉冲包络 (50ms周期, 25ms ON / 25ms OFF)
// 主: 掌心, 副: 大鱼际/小鱼际交替
void runFocus() {
  unsigned long now = millis();
  unsigned long phase = now % 50; // 50ms = 20Hz

  if (phase < 25) {
    // ON phase
    analogWrite(VM_CENTER, VM_MAX);
    // 每500ms切换大鱼际/小鱼际
    if ((now / 500) % 2 == 0) {
      analogWrite(VM_THENAR, VM_MAX);
      analogWrite(VM_HYPO, 0);
    } else {
      analogWrite(VM_THENAR, 0);
      analogWrite(VM_HYPO, VM_MAX);
    }
  } else {
    // OFF phase
    analogWrite(VM_CENTER, 0);
    analogWrite(VM_THENAR, 0);
    analogWrite(VM_HYPO, 0);
  }
}

// ============ RELAX mode ============
// 10秒慢波扫掌: M2(thenar) -> M1(center) -> M3(hypo) -> M4(wrist)
// 正弦渐强渐弱, 配合6次/分钟呼吸
void runRelax() {
  unsigned long now = millis();
  unsigned long cycle = now % 10000; // 10s cycle
  float t = cycle / 10000.0; // 0.0 ~ 1.0

  // 每个马达在周期中占25%时间, 正弦包络
  int v1 = sineEnvelope(t, 0.0, 0.25);   // M2 thenar
  int v2 = sineEnvelope(t, 0.25, 0.50);  // M1 center
  int v3 = sineEnvelope(t, 0.50, 0.75);  // M3 hypoS
  int v4 = sineEnvelope(t, 0.75, 1.0);   // M4 wrist

  analogWrite(VM_THENAR, v1);
  analogWrite(VM_CENTER, v2);
  analogWrite(VM_HYPO, v3);
  analogWrite(VM_WRIST, v4);
}

int sineEnvelope(float t, float start, float end) {
  if (t < start || t > end) return 0;
  float phase = (t - start) / (end - start); // 0~1 within window
  float val = sin(phase * PI); // 0 -> 1 -> 0
  int pwm = VM_MIN + (int)(val * (VM_MAX - VM_MIN));
  return pwm;
}

// ============ ALERT mode ============
// 3次急促短震 (100ms ON, 100ms OFF) 然后停止
void runAlert() {
  unsigned long elapsed = millis() - lastUpdate;

  if (waveStep < 3) {
    if (elapsed < 100) {
      // ON
      analogWrite(VM_CENTER, VM_MAX);
      analogWrite(VM_THENAR, VM_MAX);
      analogWrite(VM_HYPO, VM_MAX);
      analogWrite(VM_WRIST, VM_MAX);
    }
    else if (elapsed < 200) {
      // OFF
      analogWrite(VM_CENTER, 0);
      analogWrite(VM_THENAR, 0);
      analogWrite(VM_HYPO, 0);
      analogWrite(VM_WRIST, 0);
    }
    else {
      waveStep++;
      lastUpdate = millis();
    }
  }
  else {
    // 3次完成, 停止
    allOff();
    currentMode = 0;
    Serial.println("Alert burst complete");
  }
}

// ============ 全关 ============
void allOff() {
  digitalWrite(MAG_1, LOW);
  digitalWrite(MAG_2, LOW);
  digitalWrite(MAG_3, LOW);
  analogWrite(VM_CENTER, 0);
  analogWrite(VM_THENAR, 0);
  analogWrite(VM_HYPO, 0);
  analogWrite(VM_WRIST, 0);
}