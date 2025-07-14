import RPi.GPIO as GPIO
import time

class DigitalController:
    def __init__(self, pin_number=15, on_time=0.8):
        """Initialize DigitalController with GPIO pin number and on-time duration.

        Args:
            pin_number (int): GPIO pin number (BCM numbering)
            on_time (float): Duration to keep output on in seconds
        """
        self.pin_number = pin_number
        self.on_time = on_time
        self._initialized = False
        self._setup_gpio()

    def _setup_gpio(self):
        """Set up GPIO pin."""
        if not self._initialized:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_number, GPIO.OUT)
            GPIO.output(self.pin_number, GPIO.HIGH)
            self._initialized = True

    def turn_on(self):
        """Turn the output on."""
        if not self._initialized:
            self._setup_gpio()
        try:
            GPIO.output(self.pin_number, GPIO.LOW)
        except Exception as e:
            print(f"Error in turn_on: {e}")
            raise

    def turn_off(self):
        """Turn the output off."""
        if self._initialized:
            try:
                GPIO.output(self.pin_number, GPIO.HIGH)
            except Exception as e:
                print(f"Error in turn_off: {e}")
                raise

    def cleanup(self):
        """Clean up GPIO settings."""
        if self._initialized:
            GPIO.output(self.pin_number, GPIO.HIGH)
            GPIO.cleanup(self.pin_number)
            self._initialized = False
            print(f"GPIO cleaned up for pin {self.pin_number}")

    def __del__(self):
        """Destructor to ensure GPIO cleanup."""
        try:
            self.cleanup()
        except:
            pass



