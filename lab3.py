# LAB 3: Obstacle-Based Safety Alert System
# Raspberry Pi Pico MicroPython Code
# Components Pin Mapping in comments

from machine import Pin, PWM, I2C
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Ultrasonic Sensor Pins
trig = Pin(3, Pin.OUT)    # GP3 -> TRIG
echo = Pin(2, Pin.IN)     # GP2 -> ECHO

# Obstacle Sensor
obstacle = Pin(4, Pin.IN)  # GP4 -> Obstacle sensor

# LEDs
led_green = Pin(6, Pin.OUT)   # GP6 -> Green LED
led_yellow = Pin(7, Pin.OUT)  # GP7 -> Yellow LED
led_red = Pin(8, Pin.OUT)     # GP8 -> Red LED

# Buzzer (PWM)
buzzer = PWM(Pin(9))  # GP9 -> Active Buzzer

# LCD (I2C)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # GP0->SDA, GP1->SCL
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

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
    obstacle_detected = obstacle.value()
    lcd.clear()
    clear_leds()

    if distance > 50:
        # Safe Zone
        led_green.high()
        buzzer.duty_u16(0)
        lcd.putstr("SAFE ZONE\n{:.1f} cm".format(distance))
    elif 30 < distance <= 50:
        # Warning Zone
        led_yellow.high()
        buzzer_beep(0.5)  # slower beep
        if obstacle_detected:
            lcd.putstr("OBSTACLE DETECTED")
        else:
            lcd.putstr("WARNING ZONE\n{:.1f} cm".format(distance))
    elif 20 < distance <= 30:
        # Very Close
        led_yellow.high()
        buzzer_beep(0.2)  # faster beep
        lcd.putstr("OBJECT NEARBY!\n{:.1f} cm".format(distance))
    else:
        # Danger Zone
        led_red.high()
        for _ in range(3):
            buzzer_beep(0.1)  # fast repeated beep
        lcd.putstr("DANGER ZONE!\nSTOP IMMEDIATELY")
    
    utime.sleep(0.2)
