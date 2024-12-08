import board, busio
from adafruit_pm25.i2c import PM25_I2C


class Sensor:
    def __init__(self):
        uart = busio.I2C(board.SCL, board.SDA, frequency=100000)
        reset_pin = None
        self.pm25 = PM25_I2C(uart, reset_pin)

if __name__ == "__main__":
    print("script complete.")