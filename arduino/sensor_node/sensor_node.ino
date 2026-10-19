/*
  生态环境情感化转译设备 —— Arduino 传感器采集固件

  功能：读取所有已接线的传感器，每隔 SEND_INTERVAL_MS 毫秒
        以 SERIAL_PROTOCOL.md 规定的 JSON 格式，通过串口发给树莓派。

  烧录前必读：
  1. 波特率 115200 是"业务数据"波特率，跟烧录这块板子时 avrdude
     用的 57600（bootloader握手波特率）无关，两者不要混淆，本文件
     里 Serial.begin(115200) 不要改。
  2. 本文件必须用 Windows 电脑 + Arduino IDE 烧录，不要尝试从树莓派
     远程烧录这块板子（已知该板子bootloader在树莓派上有兼容性问题，
     详见 硬件接线现状报告.md 第1.1节）。
  3. 需要先在 Arduino IDE 的"库管理器"里安装以下三个库，否则编译报错：
       - "DHT sensor library" (作者 Adafruit)
       - "Adafruit BMP280 Library" (作者 Adafruit)
       - "Adafruit Unified Sensor" (作者 Adafruit，前两个库的依赖)
  4. 下方"用户配置区"里标了 TODO 的地方，需要你实测/标定后手动改数值，
     否则先用默认值也能跑起来，只是数值不准，仅用于联调阶段验证流程。

  引脚分配（详见 硬件接线现状报告.md 第2节）：
    A0  — 光敏电阻
    A1  — 土壤湿度 (SIG)
    A2  — 声音 MAX4466 (OUT)
    A4  — BMP280 SDA (I2C, Uno硬件固定引脚)
    A5  — BMP280 SCL (I2C, Uno硬件固定引脚)
    A6  — pH传感器 Po (默认禁用，接线完成后开启)
    A7  — TDS模块 AOUT (默认禁用，接线完成后开启)
    D2  — DHT 数据线
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>

// ============================ 用户配置区 ============================

// 如果你的温湿度传感器型号是 DHT22 / AM2302，把下面这行改成 DHTTYPE DHT22
#define DHTTYPE DHT11
#define DHTPIN  2

const uint8_t PIN_LIGHT = A0;
const uint8_t PIN_SOIL  = A1;
const uint8_t PIN_SOUND = A2;
const uint8_t PIN_PH    = A6;
const uint8_t PIN_EC    = A7;

// pH 未接线，保持 false；EC(TDS)已接在A7，重新启用
const bool ENABLE_PH = false;
const bool ENABLE_EC = true;   // TDS模块已接线(A7)，用厂商默认经验公式，未精确标定

// 每隔多久发送一行 JSON（毫秒），对齐 SERIAL_PROTOCOL.md 建议的 2 秒
const unsigned long SEND_INTERVAL_MS = 2000;

// ---- 土壤湿度标定：已用实测值标定（2026-07-05） ----
// 实测：空气中 0-4，泡水中 350-370（取各自区间中点）。
// 注意这颗传感器是"湿度越高、原始值越大"的方向，跟另一些型号相反，
// 但下面这条公式是方向无关的，只要常量填对，两种方向都能正确换算。
const int SOIL_DRY_RAW = 2;
const int SOIL_WET_RAW = 360;

// ---- 光照粗略换算：非精确lux，仅用于判断相对明暗趋势 ----
const float LIGHT_REF_RAW = 1023.0;
const float LIGHT_REF_LUX = 20000.0; // 满量程大致对应的lux上限经验值

// ---- pH 标定：TODO 用 pH4.0 / pH7.0 标准缓冲液做两点标定后替换 ----
// 标定方法：探头分别插入pH4.0和pH7.0缓冲液，记录各自稳定后的电压值
// (voltage = analogRead(PIN_PH) * 5.0 / 1023.0)，代入两点式算出斜率和截距。
const float PH_SLOPE     = -5.70;   // TODO: 标定后替换
const float PH_INTERCEPT = 21.34;   // TODO: 标定后替换

// ---- TDS/EC 换算：模块常见经验公式，标定后可微调 ----
const float TDS_VREF = 5.0;

// ============================ 用户配置区结束 ============================

Adafruit_BMP280 bmp;
DHT dht(DHTPIN, DHTTYPE);

bool bmpOk = false;
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();

  Wire.begin();
  bmpOk = bmp.begin(0x76);
  if (!bmpOk) {
    bmpOk = bmp.begin(0x77);
  }
  // 注意：BMP280 目前只做初始化检测，不参与JSON输出。
  // 原因：SERIAL_PROTOCOL.md 定义的字段里没有"气压"这一项，
  // 项目官方传感器方案用BME680(含VOC)而非BMP280，这属于第3节里
  // 待决策的差异项。等决策明确后再决定要不要启用气压读数。
}

float readSoilMoisturePercent() {
  int raw = analogRead(PIN_SOIL);
  float pct = (float)(SOIL_DRY_RAW - raw) / (float)(SOIL_DRY_RAW - SOIL_WET_RAW) * 100.0;
  if (pct < 0) pct = 0;
  if (pct > 100) pct = 100;
  return pct;
}

float readSoundLevel() {
  // 音频信号是快速交流波形，单次analogRead没有意义。
  // 在30ms窗口内连续采样，取峰峰值(最大值-最小值)代表声音强度，
  // 再归一化到0-100，对齐SERIAL_PROTOCOL.md里"相对强度(0-100)"的定义。
  unsigned long start = millis();
  int minVal = 1023;
  int maxVal = 0;
  while (millis() - start < 30) {
    int v = analogRead(PIN_SOUND);
    if (v < minVal) minVal = v;
    if (v > maxVal) maxVal = v;
  }
  int peakToPeak = maxVal - minVal;
  float level = (float)peakToPeak / 1023.0 * 100.0;
  if (level > 100.0) level = 100.0;
  return level;
}

float readPh() {
  int raw = analogRead(PIN_PH);
  float voltage = raw * (5.0 / 1023.0);
  return PH_SLOPE * voltage + PH_INTERCEPT;
}

float readEc() {
  int raw = analogRead(PIN_EC);
  float voltage = raw * (TDS_VREF / 1023.0);
  // 常见TDS传感器模块的经验拟合公式（未做温度补偿，25°C环境下误差可接受）
  float tdsValue = (133.42 * voltage * voltage * voltage
                     - 255.86 * voltage * voltage
                     + 857.39 * voltage) * 0.5;
  if (tdsValue < 0) tdsValue = 0;
  return tdsValue;
}

void loop() {
  unsigned long now = millis();
  if (now - lastSend < SEND_INTERVAL_MS) {
    return;
  }
  lastSend = now;

  // ---- 采集所有传感器 ----
  float humidityAir = dht.readHumidity();
  float temperature = dht.readTemperature();
  bool dhtOk = !isnan(humidityAir) && !isnan(temperature);

  int lightRaw = analogRead(PIN_LIGHT);
  float lightLux = (float)lightRaw / LIGHT_REF_RAW * LIGHT_REF_LUX;

  float soilPct = readSoilMoisturePercent();
  float soundLevel = readSoundLevel();

  // ---- 按 SERIAL_PROTOCOL.md 格式拼接 JSON ----
  // 原则：读取失败/未接线的传感器，直接不写这个字段，不写null/0。
  String json = "{";
  bool first = true;

  if (dhtOk) {
    if (!first) json += ",";
    json += "\"temperature\":";
    json += String(temperature, 2);
    first = false;

    json += ",\"humidity_air\":";
    json += String(humidityAir, 2);
  }

  if (!first) json += ",";
  json += "\"moisture\":";
  json += String(soilPct, 2);
  first = false;

  json += ",\"light\":";
  json += String(lightLux, 1);

  json += ",\"sound\":";
  json += String(soundLevel, 2);

  if (ENABLE_PH) {
    json += ",\"ph\":";
    json += String(readPh(), 2);
  }

  if (ENABLE_EC) {
    json += ",\"ec\":";
    json += String(readEc(), 1);
  }

  json += "}";

  Serial.println(json);
}
