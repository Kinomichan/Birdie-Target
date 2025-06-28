import sys, board, busio
import i2cdisplaybus
import displayio
import adafruit_displayio_ssd1306
import adafruit_bitmap_font.bitmap_font as bitmap_font
from adafruit_display_text import label
import terminalio

WIDTH = 128
HEIGHT = 64

def main():
    display = initSsd1306()
    
    text = "Hello, World!"
    showBigText(text, display)
    return 0


def initSsd1306():
    displayio.release_displays()

    i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

    return display


def loadLeagueSpartanBold16Font():
    font = bitmap_font.load_font("/fonts/LeagueSpartan-Bold-16.bdf")
    return font


def loadJunctionRegular24Font():
    font = bitmap_font.load_font("/fonts/Junction-regular-24.bdf")
    return font


def showText(text, display):
    splash = displayio.Group()
    text_area = label.Label(terminalio.FONT, text=text, x=10, y=30)
    splash.append(text_area)
    display.root_group = splash


def showFontText(text, font, display):
    text_area = label.Label(font, text=text)

    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (WIDTH // 2, HEIGHT // 2)
    
    splash = displayio.Group()
    splash.append(text_area)
    display.root_group = splash

def clearDisplay(display):
    display.root_group = None

if __name__ == '__main__':
    sys.exit(main())
