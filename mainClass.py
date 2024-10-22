from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition
import pydobot
from weighingScale import weighingScale
from time import sleep
from hcsr04 import UltrasonicSensor
from detection import Detector

class OrangeSys:
    def __init__(self):
        available_port = list_ports.comports()
        print(f'Available ports: {[x.device for x in available_port]}')
        port = available_port[0].device
        
        self.arm = pydobot.Dobot(port=port, verbose=True)
        self.device = Dobot(port=port)
        self.weight = weighingScale()
        self.detector = Detector('./orange_ncnn_model')
        self.sensor = UltrasonicSensor(trig_pin=23, echo_pin=24)
        self.totalWeight = 0
        self.arm.speed(velocity=980, acceleration=980)
        self.goHome()

    def goHome(self):
        r = 0
        (x_home, y_home, z_home) = 220.9254, 20.6777, 120
        self.arm.move_to(x_home, y_home, z_home, r, wait=True)

    def getToScale(self):
        x_conv, y_conv, z_conv = 122.6158, -219.4215, 80
        self.arm.move_to(x_conv, y_conv, 120, r=0, wait=True)
        self.arm.move_to(x_conv, y_conv, z_conv, r=0, wait=True)
        self.arm.suck(True)

        (x_Scale, y_Scale, z_Scale) = 220.9254, 20.6777, 74.0159
        self.arm.move_to(x_conv, y_conv, 120, r=0, wait=True)
        self.arm.move_to(x_Scale, y_Scale, 120, r=0, wait=True)
        self.arm.move_to(x_Scale, y_Scale, z_Scale, r=0, wait=True)
        self.arm.suck(False)
        self.goHome()

    def getToConv2(self):
        (x_Scale, y_Scale, z_Scale) =220.9254, 20.6777, 74.0159
        self.arm.move_to(x_Scale, y_Scale, z_Scale, r=0, wait=True)
        self.arm.suck(True)
        self.arm.move_to(x_Scale, y_Scale, 120, r=0, wait=True)

        x_conv, y_conv, z_conv = 176.0082, 199.6422, 70.3996
        self.arm.move_to(x_conv, y_conv, 120, r=0, wait=True)
        self.arm.move_to(x_conv, y_conv, z_conv, r=0, wait=True)
        self.arm.suck(False)

    def getToBin(self):
        (x_Scale, y_Scale, z_Scale) = 220.9254, 20.6777, 74.0159
        self.arm.move_to(x_Scale, y_Scale, z_Scale, r=0, wait=True)
        self.arm.suck(True)
        self.arm.move_to(x_Scale, y_Scale, 120, r=0, wait=True)

        (x_bin, y_bin, z_bin) = 263.3515, -101.7431, 47.1343
        self.arm.move_to(x_bin, y_bin, z_bin, r=0, wait=True)
        self.arm.suck(False)

    def run(self, threshold):
        self.totalWeight = 0
        # Get user input for weight threshold
        #self.threshold = float(input('Weight in basket (grams): '))
        self.threshold = threshold
        self.sd = [self.threshold + 5, self.threshold - 5]  # Update the threshold range dynamically
        
        # Assign sensor pins
        sensor_pins = {'trig': 23, 'echo': 24}
        self.sensor = UltrasonicSensor(trig_pin=sensor_pins['trig'], echo_pin=sensor_pins['echo'])
		
		# Start fruit sorting process
        while True:
            dist = self.sensor.get_distance()
            if dist < 10 and self.totalWeight <= self.threshold:
                self.device.conveyor_belt_distance(speed_mm_per_sec=100, distance_mm=25, direction=1)
                self.device.conveyor_belt(speed=0)

                if self.totalWeight <= self.threshold:
                    self.goHome()
                    self.getToScale()
                    clsOutput = self.detector.run()
                    print(clsOutput)
                    
                    if clsOutput == 'Fresh Orange':
                        w = self.weight.getWeight()
                        self.totalWeight += w
                        print(f"[WEIGHT] {w} | [TOTAL WEIGHT] {self.totalWeight}")
                        self.getToConv2()
                    else:
                        self.getToBin()

            elif self.totalWeight >= self.threshold or (self.totalWeight <= self.sd[0] and self.totalWeight >= self.sd[1]):
                print('Process successful')
                self.device.conveyor_belt(speed=0)
                break
            self.device.conveyor_belt(speed=1, direction=1)

if __name__ == '__main__':
    fruit_sorter = OrangeSys()
    fruit_sorter.run(20)
