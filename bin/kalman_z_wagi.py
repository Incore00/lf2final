from bin.measure import measureHolder
import serial


def set_offset ():
	measureHolder.calibrations['offset'] = measureHolder.last_value
	print(f"offset: + {(measureHolder.calibrations['offset'])}")


def set_scale (entry_weight):
	measureHolder.calibrations['scale'] = (measureHolder.last_value - measureHolder.calibrations['offset']) / int(
		entry_weight)
	print(f"scale: + {(measureHolder.calibrations['scale'])}")
	with open("/home/rcs/Rscale/bin/measure/scale.txt", "w") as file:
		file.write(str(measureHolder.calibrations['scale']))


class SetConnection():
	def __init__ (self):

		self.serial1 = serial.Serial('/dev/ttyACM0', 9600)

		with open("/home/rcs/Rscale/bin/measure/scale.txt", "r") as file:
			measureHolder.calibrations['scale'] = float(file.read())
		print(measureHolder.calibrations['scale'])

		self.data_list = []

	def value_checker (self, source):
		data = str(self.serial1.read())
		if data[2] != "Q":
			self.data_list.append(data[2])
		elif data[2] == "Q":
			connected_data = [str(item) for item in self.data_list]
			string_data = "".join(connected_data)
			print(string_data)
			self.data_list = []
			# measureHolder.last_value = int(string_data)
			noisy_value = float(
				(int(string_data) - measureHolder.calibrations['offset']) / measureHolder.calibrations['scale'])
			measureHolder.Pc = measureHolder.P + measureHolder.wspolczynnik
			measureHolder.G = measureHolder.Pc / (measureHolder.Pc + measureHolder.wariacja)
			measureHolder.P = (1 - measureHolder.G) * measureHolder.Pc
			measureHolder.Xp = measureHolder.Xe
			measureHolder.Zp = measureHolder.Xp
			measureHolder.Xe = measureHolder.G * (noisy_value - measureHolder.Zp) + measureHolder.Xp
			measureHolder.last_value = measureHolder.Xe
		source.after(10, self.value_checker, source)

	def log_saver (self, source):
		print(len(measureHolder.readings_list))
		if len(measureHolder.readings_list) >= 100:
			with open("/home/rcs/Rscale/bin/measure/logs.txt", "a") as file:
				print('saving into file')
				for item in measureHolder.readings_list:
					file.write(item + "\n")
			measureHolder.readings_list = ['W']
		else:
			pass
		source.after(1000, self.log_saver, source)