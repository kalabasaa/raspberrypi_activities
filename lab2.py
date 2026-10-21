# LAB 2: Distance-Based Safety Alert System with Reaction Timer
# Raspberry Pi Pico MicroPython Code
# Components Pin Mapping in comments

from machine import Pin, PWM, I2C
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Ultrasonic Sensor Pins
trig = Pin(3, Pin.OUT)  # GP3 -> TRIG
echo = Pin(2, Pin.IN)   # GP2 -> ECHO

# LEDs
led_green = Pin(6, Pin.OUT)   # GP6 -> Green LED
led_yellow = Pin(7, Pin.OUT)  # GP7 -> Yellow LED
led_red = Pin(8, Pin.OUT)     # GP8 -> Red LED

# Buzzer (PWM)
buzzer = PWM(Pin(9))  # GP9 -> Active Buzzer

# Push Button
button = Pin(10, Pin.IN, Pin.PULL_DOWN)  # GP10 -> Push Button

# LCD (I2C)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # GP0->SDA, GP1->SCL

lcd = I2cLcd(i2c, I2C_ADDR, 0x27, 2, 16)

# Functions
def get_distance():
    # Send trigger pulse
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(10)
    trig.low()

    # Measure pulse duration
    while echo.value() == 0:
        start = utime.ticks_us()
    while echo.value() == 1:
        end = utime.ticks_us()

    duration = utime.ticks_diff(end, start)
    distance_cm = (duration * 0.0343) / 2
    return distance_cm

def buzzer_beep(speed):
    buzzer.freq(1000)
    buzzer.duty_u16(30000)  # 50% duty
    utime.sleep(speed)
    buzzer.duty_u16(0)
    utime.sleep(speed)

def clear_leds():
    led_green.low()
    led_yellow.low()
    led_red.low()

# Main Loop
while True:
    distance = get_distance()
    lcd.clear()
    clear_leds()

    if distance > 30:
        # Safe Zone
        led_green.toggle()
        buzzer.duty_u16(0)
        lcd.putstr("Green Light ON\n{:.1f} cm".format(distance))
        utime.sleep(0.5)
    elif 10 <= distance <= 30:
        # Warning Zone
        led_yellow.high()
        buzzer_beep(0.5)  # slow beep
        lcd.putstr("Yellow Light ON\n{:.1f} cm".format(distance))
        utime.sleep(0.5)
    else:
        # Danger Zone
        led_red.high()
        start_time = utime.ticks_ms()
        lcd.putstr("DANGER! PRESS!")

        # Wait for button press while fast beeping
        while button.value() == 0:
            buzzer_beep(0.1)
            elapsed = (utime.ticks_ms() - start_time) / 1000
            lcd.move_to(0,1)
            lcd.putstr("Time: {:.1f}s".format(elapsed))

        # Button pressed → record reaction time
        reaction_time = (utime.ticks_ms() - start_time) / 1000
        buzzer.duty_u16(0)
        led_red.low()
        lcd.clear()
        lcd.putstr("Reaction Time:\n{:.2f} s".format(reaction_time))
        utime.sleep(5)

        # 10-second countdown before resuming
        for i in range(10, 0, -1):
            lcd.clear()
            lcd.putstr("Resuming in:\n{} s".format(i))
            utime.sleep(1)
