#DHT11 Sensor with LCD,diodes and thingspeak
# Aufbau
![Aufbau](aufbau.png)

#Code

'''python
14	sensor = Adafruit_DHT.DHT11
15	pin = 4

186	def getSensorData():
187	    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
188	    return (str(humidity), str(temperature))
'''

