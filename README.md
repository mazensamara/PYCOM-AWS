# PYSCAN_AWS
- Connect Pycom Board (PYSCAN) to AWS IOT CORE and send data using MQTT 
- Create a new device in AWS console and download certificates 
- Copy AWS certificates to your Pycom board into /flash/cert (I used WinSCP)
- Use MQTT to publish and suscribe
- Connect Pycom board to AWS using WIFI
- Using Pyscan and Fipy
- Board will send voltage, lumen, lux, acceleration, roll and pitch
- Publish to a topic and subscribe to a different topic to receive data back from AWS
