from machine import Pin, I2C
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR = 0x27  
lcd_rows = 2
lcd_cols = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, lcd_rows, lcd_cols)

lyrics = [
    "and I'm so high",
    "(And I'm so high)",
    "and I'm so high",
    "(And I'm so high)",
    "and I'm so high",
    "(And I'm so high)",
    "and I'm so high",
    "(And I'm so high)"
]

time = 2
time2 = 4
# scl - gp2
#sda - gp0

lcd.clear()
lcd.putstr("start")
lcd.clear()
sleep(1)
for x in range(time):
    
# Word by word display

    
    lcd.putstr("Goin'")
    sleep(0.7)        # wait 0.7 second
    lcd.clear()

    lcd.putstr("back to")
    sleep(0.8)
    lcd.clear()

  

    lcd.putstr("Honolulu")
    sleep(0.7)
    lcd.clear()

    lcd.putstr("Just to")
    sleep(0.7)
    lcd.clear()

    lcd.putstr("get that")
    sleep(0.9)
    lcd.clear()



    lcd.putstr("that")
    sleep(0.5)
    lcd.clear()

    lcd.putstr("Maui, wowie")
    sleep(0.9)
    lcd.clear()

 

    lcd.putstr("that")
    sleep(0.5)
    lcd.clear()

    lcd.putstr("Maui, wowie")
    sleep(0.9)
    lcd.clear()
    sleep(1)
    

for i in range(time * 2):
    lcd.clear()
    lcd.putstr(lyrics[i])
    sleep(1.7) 


# Final message


