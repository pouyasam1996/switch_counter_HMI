import tkinter as tk
import time
import threading
import RPi.GPIO as GPIO
from hmi import HMIApp
from submit_share_drive import FolderManager
from GPIOControlClass import DigitalController

class MainProgram:
    def __init__(self):
        self.is_running = False
        self.counter = 0
        self.total_counts = 0
        self.batch_size = 10
        self.folder_manager = FolderManager()
        self.switch_controller = DigitalController(pin_number=23, on_time=0.8)  # Pin 15 for output
        self.last_switch_time = 0
        self.last_detection_time = 0
        self.last_save_time = time.time()
        self.debounce_time = 0.2  # 0.2s debounce
        self.cooldown_time = 0.7  # 0.6s cooldown
        self.save_interval = 60  # 1 minute
        self.prev_switch_state = True  # Pull-up, HIGH is default (not pressed)
        self.switch_pin = 17  # GPIO pin 10 for switch input
        self.relay_activate = 0.8 #the timer that shows for how long the conveyor should be turned on
        self._setup_gpio()

    def _setup_gpio(self):
        """Set up GPIO pin 10 as input with pull-up resistor."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def toggle_running(self):
        self.is_running = not self.is_running

    def read_switch(self):
        """Read the current state of the switch on pin 10."""
        try:
            return GPIO.input(self.switch_pin) == GPIO.LOW  # LOW is pressed (pull-up)
        except Exception as e:
            print(f"Error reading pin {self.switch_pin}: {e}")
            return False

    def activate_output(self):
        """Activate pin 15 for 0.8s in a separate thread."""
        self.switch_controller.turn_on()
        time.sleep(self.relay_activate)
        self.switch_controller.turn_off()

    def update_counter(self):
        if not self.is_running:
            return

        current_time = time.time()
        # Read switch state
        switch_state = self.read_switch()

        # Debounce: only process if enough time has passed since last switch
        if current_time - self.last_switch_time < self.debounce_time:
            return

        # Detect falling edge (HIGH to LOW, switch pressed)
        if self.prev_switch_state and not switch_state:
            # Check cooldown for detection
            if current_time - self.last_detection_time >= self.cooldown_time:
                self.counter += 1
                self.total_counts += 4
                self.last_detection_time = current_time
                if self.counter >= self.batch_size:
                    self.counter = 0
                    # Start output activation in a separate thread
                    threading.Thread(target=self.activate_output, daemon=True).start()
                print(f"Switch pressed, counter: {self.counter}, total: {self.total_counts}")

        self.prev_switch_state = switch_state
        self.last_switch_time = current_time

        # Save total_counts every minute
        if current_time - self.last_save_time >= self.save_interval:
            self.folder_manager.data_saving_function(self.total_counts)
            self.last_save_time = current_time
            print(f"Saved total_counts: {self.total_counts}")

if __name__ == "__main__":
    program = MainProgram()
    root = tk.Tk()
    app = HMIApp(root, program)

    # Main loop for non-blocking switch detection
    def main_loop():
        program.update_counter()
        root.after(10, main_loop)  # Check every 10ms

    root.after(10, main_loop)
    root.mainloop()

    # Cleanup GPIO on exit
    GPIO.cleanup(program.switch_pin)
    program.switch_controller.cleanup()