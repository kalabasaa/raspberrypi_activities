# LAB 1: Reaction Time Game
# Raspberry Pi Pico MicroPython Code

from machine import Pin, PWM, I2C
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

trig = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

led_green = Pin(6, Pin.OUT)
led_yellow = Pin(7, Pin.OUT)
led_red = Pin(8, Pin.OUT)

buzzer = PWM(Pin(9))
button = Pin(10, Pin.IN, Pin.PULL_DOWN)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = 0x27

lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

def get_distance():
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(10)
    trig.low()

    while echo.value() == 0:
        start = utime.ticks_us()
    while echo.value() == 1:
        end = utime.ticks_us()

    duration = utime.ticks_diff(end, start)
    return (duration * 0.0343) / 2

def buzzer_beep(speed):
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    utime.sleep(speed)
    buzzer.duty_u16(0)
    utime.sleep(speed)

def clear_leds():
    led_green.low()
    led_yellow.low()
    led_red.low()

while True:
    distance = get_distance()
    lcd.clear()
    clear_leds()

    if distance > 30:
        led_green.toggle()
        lcd.putstr("Green Light ON\n{:.1f} cm".format(distance))
        utime.sleep(0.5)

    elif 20 < distance <= 30:
        led_yellow.toggle()
        buzzer_beep(0.5)
        lcd.putstr("Yellow Light ON\n{:.1f} cm".format(distance))
        utime.sleep(0.5)

    else:
        led_red.high()
        start_time = utime.ticks_ms()
        lcd.putstr("DANGER!\nTime: 0.0 s")

        while button.value() == 0:
            buzzer_beep(0.1)
            elapsed = (utime.ticks_ms() - start_time) / 1000
            lcd.move_to(6, 1)
            lcd.putstr("{:.1f} s".format(elapsed))

        reaction_time = (utime.ticks_ms() - start_time) / 1000
        buzzer.duty_u16(0)
        lcd.clear()
        lcd.putstr("Reaction Time:\n{:.2f} s".format(reaction_time))
        utime.sleep(5)

        for i in range(10, 0, -1):
            lcd.clear()
            lcd.putstr("Resuming in:\n{} s".format(i))
            utime.sleep(1)
