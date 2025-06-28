import sys
import setWifiNtp
import supervisor

def main():
    supervisor.runtime.autoreload = False
    supervisor.set_next_code_file(None)

    # Connecting to WiFi
    setWifiNtp.connectToWifi()
    # Setting NTP datetime and syncing to RTC
    setWifiNtp.syncToNtp()
    
if __name__ == '__main__':
    sys.exit(main())
