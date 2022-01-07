import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


class Hardware:
    def __init__(self, pump_pin: int):
        self.pump_pin = pump_pin
        GPIO.setup(pump_pin, GPIO.OUT)
        GPIO.output(pump_pin, GPIO.LOW)

    def water_cycle(self, seconds: int) -> None:
        GPIO.output(self.pump_pin, GPIO.HIGH)
        time.sleep(seconds)
        GPIO.output(self.pump_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
