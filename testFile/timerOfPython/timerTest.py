from threading import Timer;

timer = 0

def func_timer(i, index):
    print('cur i', i)
    print('cur index', index)
    # global timer
    timer1 = Timer(5.5, func_timer, (i,index))
    timer1.start()

timer = Timer(1, func_timer, (1,2))
timer.start()