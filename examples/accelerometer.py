from robotserial import SerialStateMachineThread
import time

def print_accelerometer(a, b, c):
    print( "accelerometer xyz: [{}, {}, {}]".format(a,b,c))

ssmt = SerialStateMachineThread()
ssmt.start() # accelerometer currently needs to be found before it can be called

ssmt.accelerometer.set_callback( print_accelerometer )

time.sleep(1)
ssmt.join()