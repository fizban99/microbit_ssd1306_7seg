from ssd1306_7seg import initialize, disp_number, blink
from microbit import running_time, sleep, button_a, button_b

initialize(1, 1)
minutes, seconds, timer = 0, 0, 0
while True:
    while not (button_a.is_pressed() and button_b.is_pressed()):
        i = 0
        if button_a.is_pressed() and not button_b.is_pressed():
            while i < 300 and button_a.is_pressed() and not button_b.is_pressed():
                sleep(10)
                i = i + 10
            if not button_b.is_pressed():
                minutes = (minutes + 1) % 100
                disp_number(minutes * 100 + seconds)
        elif button_b.is_pressed() and not button_a.is_pressed():
            while i < 300 and button_b.is_pressed() and not button_a.is_pressed():
                sleep(10)
                i = i + 10
            if not button_a.is_pressed():
                seconds = (seconds + 1) % 60
                disp_number(minutes * 100 + seconds)
    start = running_time()
    timer = (minutes * 60 + seconds)
    left = timer * 1000 + 999
    while left > 0:
        minutes, seconds = (left // 1000) // 60, (left // 1000) % 60
        disp_number(minutes * 100 + seconds)
        sleep(100)
        left = timer * 1000 - (running_time() - start) + 999
    blink(2000)