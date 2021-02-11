# DHT11 Sensor mit LCD,Dioden und Thingspeak

## Darstellung
### Aufbau
![Aufbau](aufbau.png)

## Code

### Import

```python
1	import Adafruit_DHT
2	import RPi.GPIO as GPIO 
3	import time
4	from time import sleep
5	import numpy as np
6	import matplotlib
7	import matplotlib.pyplot as plt
8	import matplotlib.animation as animation
9	from matplotlib import style
10	import datetime as dt
11	import sys
12	from urllib.request import urlopen

```
Benötigte Bibliotheken werden importiert

### Sensordaten

```python
14	sensor = Adafruit_DHT.DHT11
15	pin = 4

...

186	def getSensorData():
187	    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
188	    return (str(humidity), str(temperature))

```
Benötigt zum Erfassen der Messwerte des DHT11-Sensors.
Bestimmung des Sensors und des Messkanals, anschließende Bestimmung der ausgegebenen Werte.

### Diagramm

```python
150	def update_plot():
151	    axs[0].clear()
152	    axs[1].clear()
	    
154	    axs[0].set_title('Luftfeuchtigkeit')
155	    axs[0].set_xlabel('Zeit (h, min, sec)')
156	    axs[0].set_ylabel('Luftfeuchtigkeit (%)')

158	    axs[1].set_xlabel('Zeit (h, min, sec)')
159	    axs[1].set_title('Temperatur')
160	    axs[1].set_ylabel('Temperatur (°C)')
	    
162	    axs[0].plot(xshum[-5:], yshum[-5:], color='b', label = "Luftfeuchtigkeit")
163	    axs[0].axhline(y = np.average(yshum, axis = None), color = 'g', ls = '-', label = "\u00D8 Luftfeuchtigkeit")
	    
165	    axs[1].plot(xstem[-5:], ystem[-5:], color='r', label = "Temperatur")
166	    axs[1].axhline(y = np.average(ystem, axis = None), color = 'm', ls = '-', label = "\u00D8 Temperatur")

168	    axs[0].legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')
169	    axs[1].legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')

...
	
	#Beschriftung der x-Achsen
190	def xaxisRealtime():
191	    xshum.append(dt.datetime.now().strftime('%H:%M:%S'))
192	    xstem.append(dt.datetime.now().strftime('%H:%M:%S'))
	
	#Beschriftung der y-Achsen    
194	def yaxisMeasure():
195	    yshum.append(humidity)
196	    ystem.append(temperature)

...

204	xshum = []
205	xstem = []
206	yshum = []
207	ystem = []
	
...	

215	plt.ion()
216     fig, axs = plt.subplots(2, 1, constrained_layout=True)
217     fig.canvas.set_window_title('Live Chart')    

```
Darstellung des Computer erstellten Live-Plots

### LCD

```python
	#Verkabelung
31	# The wiring for the LCD is as follows:
32	# 1 : GND
33	# 2 : 5V
34	# 3 : Contrast (0-5V)*
35	# 4 : RS (Register Select)
36	# 5 : R/W (Read Write)       - GROUND THIS PIN
37	# 6 : Enable or Strobe
38	# 7 : Data Bit 0             - NOT USED
39	# 8 : Data Bit 1             - NOT USED
40	# 9 : Data Bit 2             - NOT USED
41	# 10: Data Bit 3             - NOT USED
42	# 11: Data Bit 4
43	# 12: Data Bit 5
44	# 13: Data Bit 6
45	# 14: Data Bit 7
46	# 15: LCD Backlight +5V**
47	# 16: LCD Backlight GND
	
	#Pindefinierung
49	LCD_RS = 26
50	LCD_E  = 19
51	LCD_D4 = 13 
52	LCD_D5 = 6
53	LCD_D6 = 5
54	LCD_D7 = 11
55	LED_ON = 15

57	LCD_WIDTH = 16
58	LCD_CHR = True
59	LCD_CMD = False
60	LCD_LINE_1 = 0x80 
61	LCD_LINE_2 = 0xC0 
62	E_PULSE = 0.00005
63	E_DELAY = 0.00005

65	def lcd_init():
66	  GPIO.setmode(GPIO.BCM)       
67	  GPIO.setup(LCD_E, GPIO.OUT) 
68	  GPIO.setup(LCD_RS, GPIO.OUT)
69	  GPIO.setup(LCD_D4, GPIO.OUT) 
70	  GPIO.setup(LCD_D5, GPIO.OUT) 
71	  GPIO.setup(LCD_D6, GPIO.OUT) 
72	  GPIO.setup(LCD_D7, GPIO.OUT) 
73	  GPIO.setup(LED_ON, GPIO.OUT)  

75	  lcd_byte(0x33,LCD_CMD)
76	  lcd_byte(0x32,LCD_CMD)
77	  lcd_byte(0x28,LCD_CMD)
78	  lcd_byte(0x0C,LCD_CMD)  
79	  lcd_byte(0x06,LCD_CMD)
80	  lcd_byte(0x01,LCD_CMD)  
	
	#Möglichkeiten der Darstellung
82	def lcd_string(message,style):
83	  if style==1:
84	    message = message.ljust(LCD_WIDTH," ")  # style=1 Left justified  
85	  elif style==2:
86	    message = message.center(LCD_WIDTH," ") # style=2 Centred
87	  elif style==3:
88	    message = message.rjust(LCD_WIDTH," ")  # style=3 Right justified

90	  for i in range(LCD_WIDTH):
91	    lcd_byte(ord(message[i]),LCD_CHR)

93	def lcd_byte(bits, mode):
94	  GPIO.output(LCD_RS, mode) 

96	  GPIO.output(LCD_D4, False)
97	  GPIO.output(LCD_D5, False)
98	  GPIO.output(LCD_D6, False)
99	  GPIO.output(LCD_D7, False)
100	  if bits&0x10==0x10:
101	    GPIO.output(LCD_D4, True)
102	  if bits&0x20==0x20:
103	    GPIO.output(LCD_D5, True)
104	  if bits&0x40==0x40:
105	    GPIO.output(LCD_D6, True)
106	  if bits&0x80==0x80:
107	    GPIO.output(LCD_D7, True)

109	  time.sleep(E_DELAY)    
110	  GPIO.output(LCD_E, True)  
111	  time.sleep(E_PULSE)
112	  GPIO.output(LCD_E, False)  
113	  time.sleep(E_DELAY)      

115	  GPIO.output(LCD_D4, False)
116	  GPIO.output(LCD_D5, False)
117	  GPIO.output(LCD_D6, False)
118	  GPIO.output(LCD_D7, False)
119	  if bits&0x01==0x01:
120	    GPIO.output(LCD_D4, True)
121	  if bits&0x02==0x02:
122	    GPIO.output(LCD_D5, True)
123	  if bits&0x04==0x04:
124	    GPIO.output(LCD_D6, True)
125	  if bits&0x08==0x08:
126	    GPIO.output(LCD_D7, True)

128	  time.sleep(E_DELAY)    
129	  GPIO.output(LCD_E, True)  
130	  time.sleep(E_PULSE)
131	  GPIO.output(LCD_E, False)  
132	  time.sleep(E_DELAY)   

	#gemessenen Werte
134	def LCD1():
135	    lcd_byte(LCD_LINE_1, LCD_CMD)
136	    lcd_string("Luft: %d %%" % humidity, 1)
137	    lcd_byte(LCD_LINE_2, LCD_CMD)
138	    lcd_string("Temp: %d \u0027C" % temperature, 1)
	    
140	    sleep(2.5)
	    
	#aktuelle Zeit    
142	def LCD2():
143	    lcd_byte(LCD_LINE_1, LCD_CMD)
144	    lcd_string("Datum:%s" %time.strftime("%m.%d.%Y"), 1)
145	    lcd_byte(LCD_LINE_2, LCD_CMD)
146	    lcd_string("Zeit: %s" %time.strftime("%H:%M:%S"), 1)
	    
148	    sleep(0.5)

...	  
  
246	    lcd_byte(LCD_LINE_1, LCD_CMD)
247         lcd_string("Sending Data",2)
248         sleep(1.5)

...

251         lcd_byte(LCD_LINE_2, LCD_CMD)
252         lcd_string("Data sent",2)
            
254         sleep(1.5)

... 
           
257         lcd_byte(LCD_LINE_2, LCD_CMD)
258         lcd_string("No connection!",2)
259         sleep(1.5)
            
```
Richtige Verkabelung des LCD. Anschließend Definierung des Displays, Möglichkeiten der Darstellung.
Anzeige der aktuellen Zeit und der gemessenen Werte.

### Dioden

```python
	humx = 80
	temx = 20
	
...	
	
	#Einstellen der Ein/Ausgänge
	GPIO.setmode(GPIO.BCM)           
	GPIO.setup(21, GPIO.OUT)

	GPIO.setmode(GPIO.BCM)           
	GPIO.setup(20, GPIO.OUT)

...
	#Definierung der Funktionsweise der Dioden
	def lightsignals():  
	    if humidity >= humx:
		GPIO.output(21, 1)
		time.sleep(1)                 
	     
	    else:
		GPIO.output(21, 0)
		                              
	    if temperature <= temx:
		GPIO.output(20, 1)
		time.sleep(1)                 
	     
	    else:
		GPIO.output(20, 0)
		 
```
Die Dioden gehen bei einem bestimmten Messwert an.

### Thingspeak

```python
	#Write-Key des Projekts
	write_api = '82E9BOZQJOWXKO4W'
...
	baseURL = 'https://api.thingspeak.com/update?api_key=%s' % write_api
...
	#Verzögerung
	send_counter = 0
...
	send_counter += 1
...		
		if send_counter == 3:
...		    
		    try:
		    #Ort an dem geschrieben werden soll
		        f = urlopen(baseURL + "&field1=%s&field2=%s" % (humidity, temperature))
		        
		        #print (f.read())
		        f.close()
		        sleep(1.5)                
...		    
		    #Zurücksetzten des Zählers  
		    send_counter = 0
		    
```
Da nur alle 15sec bei einem kostenlosen Account etwas geschrieben werden kann, ersetzt der Counter die überflüßigen Sekunden, wodurch das Programm weiterhin durchlaufen kann ohne jedes mal warten zu müssen.

### Main_Code

```python
if __name__ == '__main__':
    
    lcd_init()
  
    GPIO.output(LED_ON, False)

    xshum = []
    xstem = []
    yshum = []
    ystem = []
    
    send_counter = 0

    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Booting...",2)
    time.sleep(30)
    
    plt.ion()
    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    fig.canvas.set_window_title('Live Chart')

    
    while True:
        
        update_plot()
        
        humidity_ts, temperature_ts = getSensorData()
        humidity = float(humidity_ts)
        temperature = float(temperature_ts)
            
        humidity_ts, temperature_ts = getSensorData()       
               
        LCD1()    

        LCD2()  

        xaxisRealtime()

        yaxisMeasure()
        
        plt.show()
        plt.pause(0.0001)

        lightsignals()

        send_counter += 1
        
        if send_counter == 3:
            lcd_byte(LCD_LINE_1, LCD_CMD)
            lcd_string("Sending Data",2)
            sleep(1.5)
            try:
                f = urlopen(baseURL + "&field1=%s&field2=%s" % (humidity, temperature))
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("Data sent",2)
                #print (f.read())
                f.close()
                sleep(1.5)
            except:
                lcd_byte(LCD_LINE_2, LCD_CMD)
                lcd_string("No connection!",2)
                sleep(1.5)
                
            send_counter = 0
            
```
Der Teil des Code's der auf die Definierungen zugreift und das Programm ausführt

### Code

```python

	import Adafruit_DHT
	import RPi.GPIO as GPIO 
	import time
	from time import sleep
	import numpy as np
	import matplotlib
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation
	from matplotlib import style
	import datetime as dt
	import sys
	from urllib.request import urlopen

	sensor = Adafruit_DHT.DHT11
	pin = 4
	write_api = '82E9BOZQJOWXKO4W'

	humx = 80
	temx = 20

	baseURL = 'https://api.thingspeak.com/update?api_key=%s' % write_api

	GPIO.setwarnings(False)

	GPIO.setmode(GPIO.BCM)           
	GPIO.setup(21, GPIO.OUT)

	GPIO.setmode(GPIO.BCM)           
	GPIO.setup(20, GPIO.OUT)

	# The wiring for the LCD is as follows:
	# 1 : GND
	# 2 : 5V
	# 3 : Contrast (0-5V)*
	# 4 : RS (Register Select)
	# 5 : R/W (Read Write)       - GROUND THIS PIN
	# 6 : Enable or Strobe
	# 7 : Data Bit 0             - NOT USED
	# 8 : Data Bit 1             - NOT USED
	# 9 : Data Bit 2             - NOT USED
	# 10: Data Bit 3             - NOT USED
	# 11: Data Bit 4
	# 12: Data Bit 5
	# 13: Data Bit 6
	# 14: Data Bit 7
	# 15: LCD Backlight +5V**
	# 16: LCD Backlight GND

	LCD_RS = 26
	LCD_E  = 19
	LCD_D4 = 13 
	LCD_D5 = 6
	LCD_D6 = 5
	LCD_D7 = 11
	LED_ON = 15

	LCD_WIDTH = 16
	LCD_CHR = True
	LCD_CMD = False
	LCD_LINE_1 = 0x80 
	LCD_LINE_2 = 0xC0 
	E_PULSE = 0.00005
	E_DELAY = 0.00005

	def lcd_init():
	  GPIO.setmode(GPIO.BCM)       
	  GPIO.setup(LCD_E, GPIO.OUT) 
	  GPIO.setup(LCD_RS, GPIO.OUT)
	  GPIO.setup(LCD_D4, GPIO.OUT) 
	  GPIO.setup(LCD_D5, GPIO.OUT) 
	  GPIO.setup(LCD_D6, GPIO.OUT) 
	  GPIO.setup(LCD_D7, GPIO.OUT) 
	  GPIO.setup(LED_ON, GPIO.OUT)  

	  lcd_byte(0x33,LCD_CMD)
	  lcd_byte(0x32,LCD_CMD)
	  lcd_byte(0x28,LCD_CMD)
	  lcd_byte(0x0C,LCD_CMD)  
	  lcd_byte(0x06,LCD_CMD)
	  lcd_byte(0x01,LCD_CMD)  

	def lcd_string(message,style):
	  if style==1:
	    message = message.ljust(LCD_WIDTH," ")  # style=1 Left justified  
	  elif style==2:
	    message = message.center(LCD_WIDTH," ") # style=2 Centred
	  elif style==3:
	    message = message.rjust(LCD_WIDTH," ")  # style=3 Right justified

	  for i in range(LCD_WIDTH):
	    lcd_byte(ord(message[i]),LCD_CHR)

	def lcd_byte(bits, mode):
	  GPIO.output(LCD_RS, mode) 

	  GPIO.output(LCD_D4, False)
	  GPIO.output(LCD_D5, False)
	  GPIO.output(LCD_D6, False)
	  GPIO.output(LCD_D7, False)
	  if bits&0x10==0x10:
	    GPIO.output(LCD_D4, True)
	  if bits&0x20==0x20:
	    GPIO.output(LCD_D5, True)
	  if bits&0x40==0x40:
	    GPIO.output(LCD_D6, True)
	  if bits&0x80==0x80:
	    GPIO.output(LCD_D7, True)

	  time.sleep(E_DELAY)    
	  GPIO.output(LCD_E, True)  
	  time.sleep(E_PULSE)
	  GPIO.output(LCD_E, False)  
	  time.sleep(E_DELAY)      

	  GPIO.output(LCD_D4, False)
	  GPIO.output(LCD_D5, False)
	  GPIO.output(LCD_D6, False)
	  GPIO.output(LCD_D7, False)
	  if bits&0x01==0x01:
	    GPIO.output(LCD_D4, True)
	  if bits&0x02==0x02:
	    GPIO.output(LCD_D5, True)
	  if bits&0x04==0x04:
	    GPIO.output(LCD_D6, True)
	  if bits&0x08==0x08:
	    GPIO.output(LCD_D7, True)

	  time.sleep(E_DELAY)    
	  GPIO.output(LCD_E, True)  
	  time.sleep(E_PULSE)
	  GPIO.output(LCD_E, False)  
	  time.sleep(E_DELAY)   

	def LCD1():
	    lcd_byte(LCD_LINE_1, LCD_CMD)
	    lcd_string("Luft: %d %%" % humidity, 1)
	    lcd_byte(LCD_LINE_2, LCD_CMD)
	    lcd_string("Temp: %d \u0027C" % temperature, 1)
	    
	    sleep(2.5)
	    
	def LCD2():
	    lcd_byte(LCD_LINE_1, LCD_CMD)
	    lcd_string("Datum:%s" %time.strftime("%m.%d.%Y"), 1)
	    lcd_byte(LCD_LINE_2, LCD_CMD)
	    lcd_string("Zeit: %s" %time.strftime("%H:%M:%S"), 1)
	    
	    sleep(0.5)
	    
	def update_plot():
	    axs[0].clear()
	    axs[1].clear()
	    
	    axs[0].set_title('Luftfeuchtigkeit')
	    axs[0].set_xlabel('Zeit (h, min, sec)')
	    axs[0].set_ylabel('Luftfeuchtigkeit (%)')

	    axs[1].set_xlabel('Zeit (h, min, sec)')
	    axs[1].set_title('Temperatur')
	    axs[1].set_ylabel('Temperatur (°C)')
	    
	    axs[0].plot(xshum[-5:], yshum[-5:], color='b', label = "Luftfeuchtigkeit")
	    axs[0].axhline(y = np.average(yshum, axis = None), color = 'g', ls = '-', label = "\u00D8 Luftfeuchtigkeit")
	    
	    axs[1].plot(xstem[-5:], ystem[-5:], color='r', label = "Temperatur")
	    axs[1].axhline(y = np.average(ystem, axis = None), color = 'm', ls = '-', label = "\u00D8 Temperatur")

	    axs[0].legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')
	    axs[1].legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')
	    
	def lightsignals():  
	    if humidity >= humx:
		GPIO.output(21, 1)
		time.sleep(1)                 
	     
	    else:
		GPIO.output(21, 0)
		                              
	    if temperature <= temx:
		GPIO.output(20, 1)
		time.sleep(1)                 
	     
	    else:
		GPIO.output(20, 0) 

	def getSensorData():
	    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	    return (str(humidity), str(temperature))

	def xaxisRealtime():
	    xshum.append(dt.datetime.now().strftime('%H:%M:%S'))
	    xstem.append(dt.datetime.now().strftime('%H:%M:%S'))
	    
	def yaxisMeasure():
	    yshum.append(humidity)
	    ystem.append(temperature)

	if __name__ == '__main__':
	    
	    lcd_init()
	  
	    GPIO.output(LED_ON, False)

	    xshum = []
	    xstem = []
	    yshum = []
	    ystem = []
	    
	    send_counter = 0

	    lcd_byte(LCD_LINE_1, LCD_CMD)
	    lcd_string("Booting...",2)
	    time.sleep(30)
	    
	    plt.ion()
	    fig, axs = plt.subplots(2, 1, constrained_layout=True)
	    fig.canvas.set_window_title('Live Chart')

	    
	    while True:
		
		update_plot()
		
		humidity_ts, temperature_ts = getSensorData()
		humidity = float(humidity_ts)
		temperature = float(temperature_ts)
		    
		humidity_ts, temperature_ts = getSensorData()       
		       
		LCD1()    

		LCD2()  

		xaxisRealtime()

		yaxisMeasure()
		
		plt.show()
		plt.pause(0.0001)

		lightsignals()

		send_counter += 1
		
		if send_counter == 3:
		    lcd_byte(LCD_LINE_1, LCD_CMD)
		    lcd_string("Sending Data",2)
		    sleep(1.5)
		    try:
		        f = urlopen(baseURL + "&field1=%s&field2=%s" % (humidity, temperature))
		        lcd_byte(LCD_LINE_2, LCD_CMD)
		        lcd_string("Data sent",2)
		        #print (f.read())
		        f.close()
		        sleep(1.5)
		    except:
		        lcd_byte(LCD_LINE_2, LCD_CMD)
		        lcd_string("No connection!",2)
		        sleep(1.5)
		        
		    send_counter = 0
            
```

