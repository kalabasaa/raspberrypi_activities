from machine import Pin, time_pulse_us
import time

# Ultrasonic pins
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)

# LED pins
led_far = Pin(18, Pin.OUT)     # GP18
led_mid = Pin(19, Pin.OUT)     # GP19
led_close = Pin(20, Pin.OUT)   # GP20

# Buzzer pin
buzzer = Pin(15, Pin.OUT)      # GP15

def get_distance():
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()

    duration = time_pulse_us(ECHO, 1, 30000)
    if duration < 0:
        return None

    distance = (duration * 0.0343) / 2
    return distance

while True:
    dist = get_distance()

    if dist is not None:
        print("Distance:", dist, "cm")

        # Turn OFF all LEDs + buzzer first
        led_far.low()
        led_mid.low()
        led_close.low()
        buzzer.low()

        # Distance zones
        if dist > 50:
            led_far.high()      # Far
        elif dist > 20:
            led_mid.high()      # Medium
        else:
            led_close.high()    # Close

        # Buzzer when object is very close
        if dist < 15:
            buzzer.high()
        else:
            buzzer.low()

    else:
        print("No sensor reading")
        buzzer.low()

    time.sleep(0.1)

