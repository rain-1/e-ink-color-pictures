#pragma once
#define WIFI_SSID     "your-ssid"
#define WIFI_PASS     "your-password"
// raw URL of the repo's current/ folder, no trailing slash
#define BASE_URL      "https://raw.githubusercontent.com/OWNER/REPO/main/current"
// for sensor + button reporting (fine-grained PAT, contents:write on this repo). Optional.
#define GH_REPO       "OWNER/REPO"
#define GH_TOKEN      ""
#define TZ_STRING     "CET-1CEST,M3.5.0,M10.5.0/3"   // POSIX TZ; see https://github.com/nayarsystems/posix_tz_db
