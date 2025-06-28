import sys, time, board, rtc, os
import analogio
import gc

import kintone
import setWifiNtp
import displayText

# Analog Input (GP26=A0)
fsr = analogio.AnalogIn(board.A0)

sleepSecDetection = 0.001

sleepSecForNextPlay = 0.4
detectionVoltage = 2.0 # 0.0V~3.3V

def main():
    # Init SSD1306 Display
    display = displayText.initSsd1306()
    # Loading Font... Rendering 24-point font looks better, but it's slow...
    #font = displayText.loadJunctionRegular24Font()
    font = displayText.loadLeagueSpartanBold16Font()

    try:
        while True:
            showMemoryUsage()
            
            startScreen(font, display)
            mainLoop(display)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted")

    return 0


def mainLoop(display):
    try:
        while True:
            voltage = getVoltage(fsr)

            #print(f"FSR Voltage: {voltage:.2f} V")

            # Start Game if touch detected
            if voltage > detectionVoltage:
                playGame(display)
                break

            # Dectection Interval
            time.sleep(sleepSecDetection)

    except KeyboardInterrupt:
        print("Interrupted")


def startScreen(font, display):
    displayText.showFontText("TOUCH\nTO START!", font, display)
    #time.sleep(sleepSecForNextPlay)
    #displayText.clearDisplay(display)


def getVoltage(fsr):
    # Converting to 0.0V〜3.3V from 16 bit value
    return (fsr.value * 3.3) / 65535


def handleHit(font, display):
    displayText.showFontText("HIT!", font, display)
    time.sleep(sleepSecForNextPlay)
    displayText.clearDisplay(display)

    # Sleep for sleepSecForNextPlay second for the next challenge
    # time.sleep(sleepSecForNextPlay)


def playGame(display):
    duration = int(os.getenv("PLAY_TIME"))
    
    #Rendering 24-point font looks better, but it's slow...
    #font = displayText.loadJunctionRegular24Font()
    font = displayText.loadLeagueSpartanBold16Font()
    
    gameStart(font, display)
    score = 0
    startTime = time.time()
    
    try:
        while True:
            voltage = getVoltage(fsr)

            #print(f"FSR Voltage: {voltage:.2f} V")

            # Hit if the Voltage is larger than detectionVoltage V
            if voltage > detectionVoltage:
                handleHit(font, display)
                score += 1

            # Game ends after {duration} seconds
            if time.time() - startTime > duration:
                gameEnd(font, display, startTime, score)
                break

            # Dectection Interval
            time.sleep(sleepSecDetection)

    except KeyboardInterrupt:
        print("Interrupted")

    return 0


def gameStart(font, display):
    for n in range(3, 0, -1):
        displayText.showFontText(str(n), font, display)
        time.sleep(1)
        
    displayText.showFontText("START", font, display)

    return 0


def gameEnd(font, display, startTime, score):
    appId = os.getenv("APP_ID")
    sdomain = os.getenv("SUB_DOMAIN")
    token = os.getenv("API_TOKEN")

    start = setWifiNtp.strftime("%Y-%m-%d %H:%M:%S (%A) %p", time.localtime(startTime))
    end = setWifiNtp.strftime("%Y-%m-%d %H:%M:%S (%A) %p", rtc.RTC().datetime)

    displayText.showFontText("END", font, display)
    time.sleep(1)
    displayText.showFontText("SCORE: " + str(score), font, display)
    time.sleep(1)

    # Uploading the score to Kintone
    setWifiNtp.connectToWifi()

    payload = {"app": appId,
               "record": {"start": {"value": start },
                          "end": {"value": end },
                          "score": {"value": score} }}

    recordId = kintone.uploadRecord(subDomain=sdomain,
                                    apiToken=token,
                                    record=payload)
    
    setWifiNtp.disconnectWifi()

    displayText.showFontText("UPLOADED", font, display)
    time.sleep(sleepSecForNextPlay)

    return 0


def showMemoryUsage():
    free_mem = gc.mem_free()
    alloc_mem = gc.mem_alloc()

    print("-----")
    print("Free memory:", free_mem, "bytes")
    print("Allocated memory:", alloc_mem, "bytes")
    print("Total heap size:", free_mem + alloc_mem, "bytes")
    print("-----")


if __name__ == '__main__':
    sys.exit(main())
