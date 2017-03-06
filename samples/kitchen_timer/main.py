from ssd1306_7seg import initialize, disp_number, blink
from microbit import running_time, sleep, button_a, button_b
from music import play


def wait_unpressed():
    while button_a.is_pressed() or button_b.is_pressed():
        sleep(100)


def wait_unpressed2(button1, button2):
    i = 0
    while i < 300 and button1.is_pressed() and not button2.is_pressed():
        sleep(10)
        i = i + 10


initialize(1, 1)
minutes, seconds, timer, offset, increments = 0, 0, 0, 0, True
while True:
    while not (button_a.is_pressed() and button_b.is_pressed()):
        if button_a.is_pressed() and not button_b.is_pressed():
            wait_unpressed2(button_a, button_b)
            if not button_b.is_pressed():
                minutes = (minutes + 1) % 100
                play(["B6:1"], wait=False)
                increments, offset = False, 0
                disp_number(minutes * 100 + seconds)
        elif button_b.is_pressed() and not button_a.is_pressed():
            wait_unpressed2(button_b, button_a)
            if not button_a.is_pressed():
                seconds = (seconds + 1) % 60
                play(["B6:1"], wait=False)
                increments, offset = False, 0
                disp_number(minutes * 100 + seconds)
    start = running_time()
    timer = minutes * 60 + seconds
    currTime = timer * 1000 + 999
    stopped = False
    play(["B6:1"], wait=False)
    wait_unpressed()
    print(minutes, seconds)
    while not stopped:
        minutes, seconds = (currTime // 1000) // 60, (currTime // 1000) % 60
        disp_number(minutes * 100 + seconds)
        sleep(100)
        if increments:
            currTime = ((running_time() - start) + offset +timer*1000) % 1000000
        else:
            currTime = timer * 1000 - (running_time() - start) + 999 - offset
            if currTime <= 0:
                start, offset, currTime = running_time(), 0, 0 
                play((["B6:1"]*4 + ["R:2"])*3, wait=False)
                increments, timer = True, 0
        if button_a.is_pressed() or button_b.is_pressed():
            stopped = True
            play(["B6:1"], wait=False)
            offset = (running_time()-start+offset) % 1000
            wait_unpressed()
