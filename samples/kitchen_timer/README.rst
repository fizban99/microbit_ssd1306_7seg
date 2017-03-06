Kitchen Timer
#############

This sample program converts your micro:bit into a kitchen timer, using an SSD1306 OLED display connected to the I2C bus and a buzzer connected between pins 0 and GND. 
To install the program, flash an empty file with mu and use the file uploader within mu to upload main.py, ssd1306_7seg.py and segments.bin. Reboot the micro:bit.

* Button A will increase the minutes. You should hear a beep at each button press.
* Button B will increase the seconds. You should hear a beep at each button press.
* Pressing both buttons at the same time will start the timer.
* When counting, if any of the two buttons is pressed, the timer will pause. To restart the timer, press both buttons at the same time again.
* When the counter reaches 00:00, the microbit will beep and the counter will start counting up.
* If both buttons are pressed without setting the timer first, the timer will count up.
