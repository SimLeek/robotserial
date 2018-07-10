import glob
import struct
import sys
from threading import Thread, Lock

import serial


def is_3(): return sys.version_info[0] >= 3


if is_3():
    from typing import Optional


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system

        https://stackoverflow.com/a/14224477/782170
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class SerialError(Exception):
    pass


def check_byte_packing(ser):
    test_float_bytes = ser.read(4)
    if len(test_float_bytes) != 4:
        raise SerialError("Initial test bytes not read. Short serial timeout likely cause.")
    test_float = struct.unpack('f', test_float_bytes)[0]
    if not (3.14160 > test_float > 3.14158):
        raise SerialError("Test float not converted correctly.")


class SerialFloatArrayIn(object):
    def __init__(self, serial_instance, num_floats, read_callback=None):
        self.serial = serial_instance
        self.floats = [0.0] * num_floats
        self.read_callback = read_callback
        self.read_lock = None

    def read(self):
        for i in range(len(self.floats)):
            self.floats[i] = struct.unpack('f', self.serial.read(4))[0]

        if self.read_callback is not None and (self.read_lock is None or self.read_lock.locked()):
            self.read_callback(*self.floats)
        if self.read_lock is not None and self.read_lock.locked():
            self.read_lock.release()

    def unlock_once(self, blocking=True, timeout=3600):
        self.read_lock.acquire(*[blocking, timeout] if is_3() else [])

    def unlock(self):
        self.read_lock = None

    def lock(self):
        self.read_lock = Lock()


class SerialStateMachine(object):
    def __init__(self, ser):
        self.ser = ser

        self.accelerometer = SerialFloatArrayIn(ser, 3)
        self.gyroscope = SerialFloatArrayIn(ser, 3)
        self.magnetometer = SerialFloatArrayIn(ser, 3)

        # STATE MACHINE
        self.start_state = {}
        self.current_state = {}
        self.inertial_state = {}

        self.current_state = self.start_state

        self.start_state[b'I'] = self.run_inertial_state

        self.inertial_state[b'a'] = self.run_read_acceleration
        self.inertial_state[b'm'] = self.run_read_magnetometer
        self.inertial_state[b'g'] = self.run_read_gyroscope
        self.inertial_state[b'I'] = self.run_inertial_state

        self.exit = False

    def __call__(self, character):
        while character == b'\n':
            return

        self.current_state[character]()

    def run_inertial_state(self):
        self.current_state = self.inertial_state

    def run_read_acceleration(self):
        self.accelerometer.read()
        self.run_inertial_state()

    def run_read_gyroscope(self):
        self.gyroscope.read()
        self.run_inertial_state()

    def run_read_magnetometer(self):
        self.magnetometer.read()
        self.run_inertial_state()


class SerialStateMachineThread(Thread):
    def __init__(self, serial_port=None, baud_rate=9600, time_out=10):
        super(SerialStateMachineThread, self).__init__(target=self.thread)
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.time_out = time_out
        self.serial_state_machine = None  # type: Optional[SerialStateMachine]
        self.ssm_lock = Lock()
        self.ssm_lock.acquire()
        self.exit = False

    def _wait_for_serial_connection(self, time_out=3600):
        if not self.ssm_lock.acquire(**{'timeout': time_out} if is_3() else {}):
            raise SerialError("Serial connection timed out.")

    def start(self, time_out=3600):
        super(SerialStateMachineThread, self).start()
        self._wait_for_serial_connection(time_out)

    def join(self, timeout=None):
        self.exit = True
        super(SerialStateMachineThread, self).join(timeout=timeout)

    def thread(self):
        if isinstance(self.serial_port, (tuple, list)):
            all_ports = self.serial_port
        elif self.serial_port is not None:
            all_ports = [self.serial_port]
        else:
            all_ports = serial_ports()

        for p in all_ports:
            with serial.Serial(p, self.baud_rate, timeout=self.time_out) as ser:
                check_byte_packing(ser)

                self.serial_state_machine = SerialStateMachine(ser)
                self.ssm_lock.release()
                while not (self.serial_state_machine.exit or self.exit):
                    self.serial_state_machine(ser.read(1))
            if not self.ssm_lock.locked():
                self.ssm_lock.acquire()
