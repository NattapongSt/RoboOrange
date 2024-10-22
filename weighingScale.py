from time import sleep
import RPi.GPIO as GPIO
from hx711v0_5_1 import HX711
from numpy import median

class weighingScale:
	def __init__(self, dout=5, sck=6, reference_unit=365):
		self.hx = HX711(dout, sck)
		self.hx.setReadingFormat("MSB", "MSB")
		self.hx.autosetOffset()
		self.referenceUnit = reference_unit
		self.hx.setReferenceUnit(self.referenceUnit)
		
	def printWeight(self):
		RawBytes = self.hx.getRawBytes()
		weight = round(self.hx.rawBytesToWeight(RawBytes), 2)
		if weight < 1:
			weight = 0
		print(f"[WEIGHT] {weight} grams")
		
	def getWeight(self):
		weight = []
		for i in range(5):
			RawBytes = self.hx.getRawBytes()
			weight.append(round(self.hx.rawBytesToWeight(RawBytes), 2))
		return median(weight) if median(weight) > 1 else 0
		
			
	def read(self):
		while True:
			try:
				self.printWeight()    
			
			except (KeyboardInterrupt, SystemExit):
				GPIO.cleanup()
				print("[INFO] 'KeyboardInterrupt Exception' detected. Cleaning and exiting...")

if __name__ == '__main__':
	weightValue = weighingScale()
	
	for i in range(3, 0, -1):
		print('insert weight:', i)
		sleep(1)
		
	print(weightValue.getWeight())
