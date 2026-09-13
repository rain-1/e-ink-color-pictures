// PaperColor curator client — UNTESTED DRAFT written before the device arrived.
// Loop: wake → Wi-Fi → NTP → pick slot by hour → fetch current/N.png → draw → report sensors → sleep to next slot.
#include <M5Unified.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <time.h>
#include "config.h"

static const int SLOT_HOURS[5] = {6, 10, 14, 18, 22};   // must match scripts/publish.py
RTC_DATA_ATTR int lastSlotShown = -1;                      // survives deep sleep

int slotForHour(int h) {
  int s = 5;  // before 06:00 counts as last night's piece
  for (int i = 0; i < 5; i++) if (h >= SLOT_HOURS[i]) s = i + 1;
  return s;
}

uint64_t secondsToNextSlot(struct tm& t) {
  int now = t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec;
  for (int i = 0; i < 5; i++) {
    int start = SLOT_HOURS[i] * 3600;
    if (start > now) return start - now;
  }
  return 24 * 3600 - now + SLOT_HOURS[0] * 3600;
}

bool connectWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) delay(250);
  return WiFi.status() == WL_CONNECTED;
}

bool showSlot(int slot) {
  WiFiClientSecure client; client.setInsecure();
  HTTPClient http;
  String url = String(BASE_URL) + "/" + slot + ".png";
  http.begin(client, url);
  int code = http.GET();
  if (code != 200) { http.end(); return false; }
  M5.Display.setEpdMode(epd_mode_t::epd_quality);
  M5.Display.startWrite();
  bool ok = M5.Display.drawPng(http.getStreamPtr(), 0, 0);   // 400x600, already on the 6-colour palette
  M5.Display.endWrite();
  M5.Display.display();
  http.end();
  return ok;
}

void postEvent(const char* type, const String& payloadJson) {
  if (strlen(GH_TOKEN) == 0) return;
  WiFiClientSecure client; client.setInsecure();
  HTTPClient http;
  http.begin(client, String("https://api.github.com/repos/") + GH_REPO + "/dispatches");
  http.addHeader("Authorization", String("Bearer ") + GH_TOKEN);
  http.addHeader("Accept", "application/vnd.github+json");
  http.addHeader("Content-Type", "application/json");
  http.POST(String("{\"event_type\":\"") + type + "\",\"client_payload\":" + payloadJson + "}");
  http.end();
}

void reportSensors() {
  // SHT40 on the system I2C bus (0x44). M5Unified may expose this; if not, use a SHT4x lib.
  // Placeholder values until verified on hardware:
  float t = NAN, rh = NAN;
  // TODO: read SHT40
  float v = M5.Power.getBatteryVoltage() / 1000.0f;
  postEvent("sensor", String("{\"temp_c\":") + t + ",\"rh\":" + rh + ",\"batt_v\":" + v + "}");
}

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);

  // Button wake: A/B/C → feedback for the piece currently on screen
  esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();
  if (cause == ESP_SLEEP_WAKEUP_EXT1 && connectWifi()) {
    uint64_t mask = esp_sleep_get_ext1_wakeup_status();
    const char* btn = (mask & (1ULL << 10)) ? "A" : (mask & (1ULL << 9)) ? "B" : "C";
    postEvent("feedback", String("{\"slot\":") + lastSlotShown + ",\"button\":\"" + btn + "\"}");
  }

  if (!connectWifi()) { esp_sleep_enable_timer_wakeup(15ULL * 60 * 1000000); esp_deep_sleep_start(); }

  configTzTime(TZ_STRING, "pool.ntp.org", "time.nist.gov");
  struct tm t;
  if (!getLocalTime(&t, 10000)) { esp_sleep_enable_timer_wakeup(15ULL * 60 * 1000000); esp_deep_sleep_start(); }

  int slot = slotForHour(t.tm_hour);
  if (slot != lastSlotShown && showSlot(slot)) lastSlotShown = slot;
  reportSensors();

  uint64_t sleepSec = secondsToNextSlot(t) + 60;   // a minute past the slot boundary
  // wake on any of the three user buttons (G1, G9, G10 per the pin map — verify polarity)
  esp_sleep_enable_ext1_wakeup((1ULL << 1) | (1ULL << 9) | (1ULL << 10), ESP_EXT1_WAKEUP_ANY_LOW);
  esp_sleep_enable_timer_wakeup(sleepSec * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
