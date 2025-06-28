import os, time, wifi, rtc
import wifi, socketpool, ssl
import adafruit_ntp

ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
maxRetries = 3

def main():
    connectToWifi()
    syncToNtp()


def connectToWifi():
    connected = False
    retries  = 0
    while not connected and retries < maxRetries:
        try:
            # Connecting to WiFi
            print("Connecting to Wi-Fi...")
            wifi.radio.connect(ssid, password)
            print("Connected to", ssid)
            print("IP address:", wifi.radio.ipv4_address)
            connected = True
        except OSError as e:
            retries += 1
            print("Wifi Connection Failed:", e)
            time.sleep(1)


def syncToNtp():
    connected = False
    retries = 0
    while not connected and retries < maxRetries:
        try:
            # Syncing to NTP
            pool = socketpool.SocketPool(wifi.radio)
            ntp = adafruit_ntp.NTP(pool, tz_offset=-7)  # TZ: America/Los_Angeles
            # Setting to RTC
            rtc.RTC().datetime = ntp.datetime
            connected = True
        except OSError as e:
            print("NTP sync failed:", e)
            retries += 1
            time.sleep(1)

    formatted = strftime("%Y-%m-%d %H:%M:%S (%A) %p", rtc.RTC().datetime)
    print("Time synced: ", formatted)


def strftime(formatString, t):
    weekdayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekdayAbbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    replacements = {
        "%Y": "{:04}".format(t.tm_year),
        "%m": "{:02}".format(t.tm_mon),
        "%d": "{:02}".format(t.tm_mday),
        "%H": "{:02}".format(t.tm_hour),
        "%M": "{:02}".format(t.tm_min),
        "%S": "{:02}".format(t.tm_sec),
        "%A": weekdayNames[t.tm_wday],
        "%a": weekdayAbbr[t.tm_wday],
        "%p": "AM" if t.tm_hour < 12 else "PM"
    }

    for key, val in replacements.items():
        formatString = formatString.replace(key, val)

    return formatString


if __name__ == "__main__":
    main()