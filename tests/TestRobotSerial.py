import time
import unittest as ut

import robotserial as rs


class TestRobotSerial(ut.TestCase):
    def testGetAccelLocking(self):
        ssmt = rs.SerialStateMachineThread()
        ssmt.start()

        self.call_count = 0

        def accel_callback(a, b, c):
            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(c, float)
            self.call_count += 1

        ssmt.serial_state_machine.accelerometer.lock()
        ssmt.serial_state_machine.accelerometer.read_callback = accel_callback

        ssmt.serial_state_machine.accelerometer.unlock_once()
        ssmt.serial_state_machine.accelerometer.unlock_once()
        ssmt.serial_state_machine.accelerometer.unlock_once()

        ssmt.join()

        self.assertGreater(self.call_count, 0)

    def testGetAccelCallback(self):
        ssmt = rs.SerialStateMachineThread()
        ssmt.start()

        self.call_count = 0

        def accel_callback(a, b, c):
            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(c, float)
            self.call_count += 1

        ssmt.serial_state_machine.accelerometer.read_callback = accel_callback

        time.sleep(1)

        ssmt.join()

        self.assertGreater(self.call_count, 0)

    def testGetMagnetometerLocking(self):
        ssmt = rs.SerialStateMachineThread()
        ssmt.start()

        self.call_count = 0

        def magnetometer_callback(a, b, c):
            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(c, float)
            self.call_count += 1

        ssmt.serial_state_machine.magnetometer.lock()
        ssmt.serial_state_machine.magnetometer.read_callback = magnetometer_callback
        ssmt.serial_state_machine.magnetometer.unlock_once()
        ssmt.serial_state_machine.magnetometer.unlock_once()
        ssmt.serial_state_machine.magnetometer.unlock_once()

        ssmt.join()

        self.assertGreater(self.call_count, 0)

    def testGetMagnetometerCallback(self):
        ssmt = rs.SerialStateMachineThread()
        ssmt.start()

        self.call_count = 0

        def magnetometer_callback(a, b, c):
            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(c, float)
            self.call_count += 1

        ssmt.serial_state_machine.magnetometer.read_callback = magnetometer_callback

        time.sleep(1)

        ssmt.join()

        self.assertGreater(self.call_count, 0)

    def testGetGyroscopeLocking(self):
        ssmt = rs.SerialStateMachineThread()
        ssmt.start()

        self.call_count = 0

        def gyroscope_callback(a, b, c):
            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(c, float)
            self.call_count += 1

        ssmt.serial_state_machine.gyroscope.lock()
        ssmt.serial_state_machine.gyroscope.read_callback = gyroscope_callback

        ssmt.serial_state_machine.gyroscope.unlock_once()
        ssmt.serial_state_machine.gyroscope.unlock_once()
        ssmt.serial_state_machine.gyroscope.unlock_once()

        ssmt.join()

        self.assertGreater(self.call_count, 0)

    def testGetGyroscopeCallback(self):
        ssmt = rs.SerialStateMachineThread()
        ssmt.start()

        self.call_count = 0

        def gyroscope_callback(a, b, c):
            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(c, float)
            self.call_count += 1

        ssmt.serial_state_machine.gyroscope.read_callback = gyroscope_callback

        time.sleep(1)

        ssmt.join()

        self.assertGreater(self.call_count, 0)
