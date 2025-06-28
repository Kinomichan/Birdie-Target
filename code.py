import sys, time, board, rtc
import analogio

import setWifiNtp
import displayText

# Analog Input (GP26=A0)
fsr = analogio.AnalogIn(board.A0)

sleepSecDetection = 0.001

sleepSecForNextPlay = 2.0
detectionVoltage = 2.0 # 0.0V~3.3V

def main():
    # Init SSD1306 Display
    display = displayText.initSsd1306()
    # Loading Font
    font = displayText.loadJunctionRegular24Font()

    startScreen(font, display)

    try:
        while True:
            voltage = getVoltage(fsr)

            #print(f"FSR Voltage: {voltage:.2f} V")

            # Hit if the Voltage is larger than detectionVoltage V
            if voltage > detectionVoltage:
                handleHit(voltage, font, display)

            # Dectection Interval
            time.sleep(sleepSecDetection)

    except KeyboardInterrupt:
        print("Interrupted")

    return 0

def startScreen(font, display):
    displayText.showFontText("Ready!", font, display)
    #time.sleep(sleepSecForNextPlay)
    #displayText.clearDisplay(display)


def getVoltage(pin):
    # Converting to 0.0V〜3.3V from 16 bit value
    return (pin.value * 3.3) / 65535


def handleHit(voltage, font, display):
    formatted = setWifiNtp.strftime("%Y-%m-%d %H:%M:%S (%A) %p", rtc.RTC().datetime)
    #print(f"Hit !!! - Time: {formatted}, Voltage: {voltage:.2f}")
    
    displayText.showFontText("Hit!", font, display)
    time.sleep(sleepSecForNextPlay)
    displayText.clearDisplay(display)

    # Sleep for sleepSecForNextPlay second for the next challenge
    time.sleep(sleepSecForNextPlay)


if __name__ == '__main__':
    sys.exit(main())
