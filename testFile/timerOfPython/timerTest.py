from threading import Timer;

timer = 0

def func_timer():
    print('test')
    # global timer
    timer = Timer(5.5, func_timer)
    timer.start()

timer = Timer(1, func_timer)
timer.start()