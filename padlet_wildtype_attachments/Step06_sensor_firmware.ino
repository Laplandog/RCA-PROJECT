/*
 * sensor_firmware.ino — AI Life Wild Type · Arduino传感器固件
 * ============================================================
 *
 * 硬件: Arduino Mega 2560
 *
 * 传感器接线:
 *   BH1750  (光照)  → I²C (SDA=20, SCL=21)
 *   MAX9814 (麦克风) → A0
 *   DHT22   (温湿度) → D2
 *   HC-SR501(红外)   → D3
 *   FSR402  (压力)   → A1
 *   MPU6050 (加速度) → I²C (SDA=20, SCL=21)
 *
 * 串口输出: 115200 baud, 每 SAMPLE_INTERVAL_MS 毫秒一行JSON
 *   {"lux":320,"db":45,"temp":24.5,"hum":60,"pir":1,"prs":512,"ax":0.1,"ay":-0.02,"az":9.8}
 *
 * 依赖库 (Arduino Library Manager):
 *   - BH1750 by Christopher Laws
 *   - DHT sensor library by Adafruit
 *   - MPU6050 by Electronic Cats (或 I2Cdevlib)
 *   - Wire (内置)
 */

#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>

// ═══════════════════════════════════════════════════════════════
//  引脚定义
// ═══════════════════════════════════════════════════════════════

#define MIC_PIN      A0    // MAX9814 模拟输出
#define FSR_PIN      A1    // FSR402 模拟输出
#define DHT_PIN      2     // DHT22 数据线
#define PIR_PIN      3     // HC-SR501 数字输出
#define DHT_TYPE     DHT22

// ═══════════════════════════════════════════════════════════════
//  配置
// ═══════════════════════════════════════════════════════════════

#define SAMPLE_INTERVAL_MS  2500   // 采样间隔 (略小于Python端3s周期)
#define MIC_SAMPLE_WINDOW   50     // 声音采样窗口 (ms)
#define MIC_SAMPLES         50     // 每窗口采样次数

// ═══════════════════════════════════════════════════════════════
//  全局对象
// ═══════════════════════════════════════════════════════════════

BH1750 lightMeter;
DHT dht(DHT_PIN, DHT_TYPE);

// MPU6050 寄存器地址
#define MPU_ADDR 0x68
#define MPU_PWR_MGMT_1 0x6B
#define MPU_ACCEL_XOUT_H 0x3B

float accelScale = 16384.0;  // ±2g量程

// ═══════════════════════════════════════════════════════════════
//  初始化
// ═══════════════════════════════════════════════════════════════

void setup() {
    Serial.begin(115200);
    while (!Serial) { ; }  // 等待串口

    Wire.begin();

    // BH1750 初始化
    if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
        Serial.println("{\"status\":\"BH1750 OK\"}");
    } else {
        Serial.println("{\"status\":\"BH1750 FAIL\"}");
    }

    // DHT22 初始化
    dht.begin();
    Serial.println("{\"status\":\"DHT22 OK\"}");

    // PIR 初始化
    pinMode(PIR_PIN, INPUT);

    // MPU6050 初始化
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(MPU_PWR_MGMT_1);
    Wire.write(0);  // 唤醒
    byte err = Wire.endTransmission();
    if (err == 0) {
        Serial.println("{\"status\":\"MPU6050 OK\"}");
    } else {
        Serial.println("{\"status\":\"MPU6050 FAIL\"}");
    }

    // 预热
    delay(2000);
    Serial.println("{\"status\":\"READY\"}");
}

// ═══════════════════════════════════════════════════════════════
//  传感器读取函数
// ═══════════════════════════════════════════════════════════════

float readLux() {
    float lux = lightMeter.readLightLevel();
    if (lux < 0) lux = 0;
    return lux;
}

float readSoundDB() {
    // MAX9814 输出模拟电压，通过采样峰峰值估算dB
    int maxVal = 0;
    int minVal = 1023;

    unsigned long startMillis = millis();
    while (millis() - startMillis < MIC_SAMPLE_WINDOW) {
        int sample = analogRead(MIC_PIN);
        if (sample > maxVal) maxVal = sample;
        if (sample < minVal) minVal = sample;
    }

    int peakToPeak = maxVal - minVal;
    // 粗略映射到 dB (非精确，仅相对值)
    float voltage = (peakToPeak * 3.3) / 1024.0;
    float db = 20.0 * log10(voltage / 0.00631);  // 参考 6.31mV
    if (db < 0) db = 0;
    if (db > 120) db = 120;
    return db;
}

float readTemperature() {
    float t = dht.readTemperature();
    if (isnan(t)) return -999;  // 读取失败标记
    return t;
}

float readHumidity() {
    float h = dht.readHumidity();
    if (isnan(h)) return -999;
    return h;
}

int readPIR() {
    return digitalRead(PIR_PIN);
}

int readPressure() {
    return analogRead(FSR_PIN);  // 0-1023
}

void readAccel(float &ax, float &ay, float &az) {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(MPU_ACCEL_XOUT_H);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDR, 6, true);

    int16_t rawX = Wire.read() << 8 | Wire.read();
    int16_t rawY = Wire.read() << 8 | Wire.read();
    int16_t rawZ = Wire.read() << 8 | Wire.read();

    ax = rawX / accelScale * 9.81;  // 转换为 m/s²
    ay = rawY / accelScale * 9.81;
    az = rawZ / accelScale * 9.81;
}

// ═══════════════════════════════════════════════════════════════
//  主循环
// ═══════════════════════════════════════════════════════════════

void loop() {
    // 读取所有传感器
    float lux  = readLux();
    float db   = readSoundDB();
    float temp = readTemperature();
    float hum  = readHumidity();
    int   pir  = readPIR();
    int   prs  = readPressure();
    float ax, ay, az;
    readAccel(ax, ay, az);

    // JSON输出 (紧凑格式，减少串口占用)
    Serial.print("{\"lux\":");
    Serial.print(lux, 1);
    Serial.print(",\"db\":");
    Serial.print(db, 1);
    Serial.print(",\"temp\":");
    Serial.print(temp, 1);
    Serial.print(",\"hum\":");
    Serial.print(hum, 1);
    Serial.print(",\"pir\":");
    Serial.print(pir);
    Serial.print(",\"prs\":");
    Serial.print(prs);
    Serial.print(",\"ax\":");
    Serial.print(ax, 3);
    Serial.print(",\"ay\":");
    Serial.print(ay, 3);
    Serial.print(",\"az\":");
    Serial.print(az, 3);
    Serial.println("}");

    delay(SAMPLE_INTERVAL_MS);
}
