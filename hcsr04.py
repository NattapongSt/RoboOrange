import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        # Disable warnings
        GPIO.setwarnings(False)

        # GPIO Mode (BCM)
        GPIO.setmode(GPIO.BCM)

        # Set the trigger and echo pins
        self.TRIG = trig_pin
        self.ECHO = echo_pin

        # Set up GPIO pins
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def get_distance(self):
        # Ensure the TRIG is low for a short time
        GPIO.output(self.TRIG, False)

        # Send a 10µs pulse to trigger the sensor
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        # Initialize pulse_start and pulse_end
        pulse_start = pulse_end = 0

        # Wait for the ECHO pin to go HIGH and record the start time
        timeout = time.time() + 1  # 1 second timeout
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
            if time.time() > timeout:
                print("Timeout: Failed to detect object")
                return None

        # Wait for the ECHO pin to go LOW and record the end time
        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        # Calculate the pulse duration
        pulse_duration = pulse_end - pulse_start

        # Calculate distance (Speed of sound is 34300 cm/s)
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance

    def cleanup(self):
        # Clean up GPIO on exit
        GPIO.cleanup()

# Example usage of the class
if __name__ == "__main__":
    try:
        # Create an instance of the UltrasonicSensor class
        sensor = UltrasonicSensor(trig_pin=23, echo_pin=24)

        while True:
            dist = sensor.distance()
            if dist is not None:
                print(f"Distance: {dist} cm")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        sensor.cleanup()
