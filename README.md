# robotserial

robotserial is a library that transmits robot sensor and actuator
information through serial ports. It supports USBs as well as any other
port that supports serial data transmission. Multiple serial ports may
be used at once.

# Table of Contents
1. [Example](#example)
1. [Installation](#installation)
1. [License](#license)

-----

## Example

This will print all values from an attached accelerometer for one
second:

    from robotserial import SerialStateMachineThread
    import time

    def print_accelerometer(a, b, c):
        print( "accelerometer xyz: [{}, {}, {}]".format(a,b,c))

    ssmt = SerialStateMachineThread()
    ssmt.start() # accelerometer currently needs to be found before it can be accessed

    ssmt.accelerometer.set_callback( print_accelerometer )

    time.sleep(1)
    ssmt.join()

The corresponding code to send the data from an Arduino is currently:

    Serial.write("I");
    Serial.write("\na");
    Serial.write(aX.bytes, 4);Serial.write(aY.bytes, 4);Serial.write(aZ.bytes, 4);
    Serial.write("\ng");
    Serial.write(gX.bytes, 4);Serial.write(gY.bytes, 4);Serial.write(gZ.bytes, 4);
    Serial.write("\nm");
    Serial.write(mX.bytes, 4);Serial.write(mY.bytes, 4);Serial.write(mZ.bytes, 4);
    Serial.write("\n");

This will change once a C/C++ library is made for embedded
 devices.

## Installation

    $ pip install robotserial

robotserial is distributed on [PyPI](https://pypi.org) as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+ and PyPy.

## License

robotserial is distributed under the terms of both

- [MIT License](https://choosealicense.com/licenses/mit)
- [Apache License, Version 2.0](https://choosealicense.com/licenses/apache-2.0)

at your option.
