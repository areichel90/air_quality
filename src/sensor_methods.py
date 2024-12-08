import board, busio
from adafruit_pm25.uart import PM25_UART


class Sensor:
    def __init__(self):
        uart = busio.UART(board.TX, board.RX, baudrate=9600)
        reset_pin = None
        self.pm25 = PM25_UART(uart, reset_pin)

if __name__ == "__main__":
    print("script complete.")