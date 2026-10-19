/*
 * sensor_firmware_uno.ino — AI Life Wild Type · 原定6传感器固件 (Arduino UNO)
 * ================================================================================
 *
 * 板子: Arduino UNO
 *
 * 这是实验A(野生型)原定计划的完整8通道感知硬件固件。输出的 JSON 字段与
 * sensor_bridge.py 的协议完全一致, Python 端无需改动:
 *     python life_wild.py --real COMx
 *
 * 传感器接线 (UNO):
 *   BH1750   (光照)     → I²C   (SDA=A4, SCL=A5)     地址 0x23
 *   MAX9814  (麦克风)    → A0    (模拟)
 *   DHT22    (温湿度)    → D2    (数字)
 *   HC-SR501 (人体红外)  → D3    (数字)
 *   FSR402   (压力)     → A1    (模拟)
 *   MPU6050  (加速度)    → I²C   (SDA=A4, SCL=A5)     地址 0x68
 *
 *   注: BH1750 与 MPU6050 共用同一条 I²C 总线 (A4/A5), 地址不同不冲突。
 *       UNO 上模拟口 A2/A3 空闲。
 *
 * 串口输出: 115200 baud, 每 SAMPLE_INTERVAL_MS 毫秒一行紧凑 JSON:
 *   {"lux":320.0,"db":45.0,"temp":24.5,"hum":60.0,"pir":1,"prs":512,"ax":0.10,"ay":-0.02,"az":9.80}
 *
 * 依赖库 (Arduino Library Manager 安装):
 *   - BH1750 by Christopher Laws
 *   - DHT sensor library by Adafruit
 *   - Adafruit Unified Sensor (DHT 依赖)
 *   - Wire (IDE 内置, MPU6050 用裸寄存器读取, 无需额外库)
 */

#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>

// ═══════════════════════════════════════════════════════════════
//  引脚定义
// ═══════════════════════════════════════════════════════════════

#define MIC_PIN      A0    // MAX9814 模拟输出
#define FSR_PIN      A1    // FSR402 模拟输出
#define DHT_PIN      2     // DHT22 数据线 (D2)
#define PIR_PIN      3     // HC-SR501 数字输出 (D3)
#define DHT_TYPE     DHT22 // 若你的是 DHT11, 改成 DHT11

// ═══════════════════════════════════════════════════════════════
//  配置
// ═══════════════════════════════════════════════════════════════

#define SAMPLE_INTERVAL_MS  2500   // 采样间隔 (略小于 Python 端 3s 周期)
#define MIC_SAMPLE_WINDOW   50     // 声音采样窗口 (ms)

// ═══════════════════════════════════════════════════════════════
//  全局对象
// ═══════════════════════════════════════════════════════════════

BH1750 lightMeter;
DHT dht(DHT_PIN, DHT_TYPE);

// MPU6050 寄存器
#define MPU_ADDR         0x68
#define MPU_PWR_MGMT_1   0x6B
#define MPU_ACCEL_XOUT_H 0x3B
float accelScale = 16384.0;   // ±2g 量程

bool bhOK = false;
bool mpuOK = false;

// ═══════════════════════════════════════════════════════════════
//  初始化
// ═══════════════════════════════════════════════════════════════

void setup() {
    Serial.begin(115200);
    while (!Serial) { ; }

    Wire.begin();

    // BH1750
    if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
        bhOK = true;
        Serial.println("{\"status\":\"BH1750 OK\"}");
    } else {
        Serial.println("{\"status\":\"BH1750 FAIL\"}");
    }

    // DHT
    dht.begin();
    Serial.println("{\"status\":\"DHT OK\"}");

    // PIR
    pinMode(PIR_PIN, INPUT);

    // MPU6050 唤醒
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(MPU_PWR_MGMT_1);
    Wire.write(0);
    byte err = Wire.endTransmission();
    if (err == 0) {
        mpuOK = true;
        Serial.println("{\"status\":\"MPU6050 OK\"}");
    } else {
        Serial.println("{\"status\":\"MPU6050 FAIL\"}");
    }

    delay(2000);
    Serial.println("{\"status\":\"READY\"}");
}

// ═══════════════════════════════════════════════════════════════
//  传感器读取
// ═══════════════════════════════════════════════════════════════

float readLux() {
    if (!bhOK) return 0;
    float lux = lightMeter.readLightLevel();
    if (lux < 0) lux = 0;
    return lux;
}

float readSoundDB() {
    int maxVal = 0;
    int minVal = 1023;
    unsigned long startMillis = millis();
    while (millis() - startMillis < MIC_SAMPLE_WINDOW) {
        int sample = analogRead(MIC_PIN);
        if (sample > maxVal) maxVal = sample;
        if (sample < minVal) minVal = sample;
    }
    int peakToPeak = maxVal - minVal;
    float voltage = (peakToPeak * 3.3) / 1024.0;
    float db = 20.0 * log10(voltage / 0.00631);   // 参考 6.31mV, 仅相对值
    if (db < 0) db = 0;
    if (db > 120) db = 120;
    return db;
}

float readTemperature() {
    float t = dht.readTemperature();
    if (isnan(t)) return 25.0;   // 读失败给中性值
    return t;
}

float readHumidity() {
    float h = dht.readHumidity();
    if (isnan(h)) return 50.0;
    return h;
}

int readPIR() {
    return digitalRead(PIR_PIN);
}

int readPressure() {
    return analogRead(FSR_PIN);   // 0-1023
}

void readAccel(float &ax, float &ay, float &az) {
    if (!mpuOK) { ax = 0; ay = 0; az = 9.81; return; }
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(MPU_ACCEL_XOUT_H);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDR, 6, true);
    int16_t rawX = Wire.read() << 8 | Wire.read();
    int16_t rawY = Wire.read() << 8 | Wire.read();
    int16_t rawZ = Wire.read() << 8 | Wire.read();
    ax = rawX / accelScale * 9.81;   // → m/s²
    ay = rawY / accelScale * 9.81;
    az = rawZ / accelScale * 9.81;
}

// ═══════════════════════════════════════════════════════════════
//  主循环
// ═══════════════════════════════════════════════════════════════

void loop() {
    float lux  = readLux();
    float db   = readSoundDB();
    float temp = readTemperature();
    float hum  = readHumidity();
    int   pir  = readPIR();
    int   prs  = readPressure();
    float ax, ay, az;
    readAccel(ax, ay, az);

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
