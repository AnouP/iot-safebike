# iot-safebike
This is a tracker that connects to The Things Network with a lopy4-pytrack and through a nano-gateway that runs on an other lopy4 with an expansion board.
An MQTT client is used to communicate with ba publishing commands to the device.

You need to enter some config data in the config.py file for the nano-gateway:Just enter your personal WIFI SSID and WIFI password. make sure that the cloud server and LoRa frequency are adapted to your region.
  
  https://lora-alliance.org/wp-content/uploads/2021/05/RP002-1.0.3-FINAL-1.pdf
  
  
For the client-mqtt, you need to input some data too : Procedure to get the USER, PASSWORD, PUBLIC_TLS_ADDRESS and PUBLIC_TLS_ADDRESS_PORT:
  1. Login to The Things Stack Community Edition console
    https://console.cloud.thethings.network/
  2. Select Go to applications
  3. Select your application
  4. On the left hand side menu, select Integrations | MQTT
  5. See Connection credentials
  6. For the password press button: Generate new API key
  
In the pytrack node you need to get some keys from your TTN interface
dev_eui = binascii.unhexlify('________________')
app_eui = binascii.unhexlify('________________')
app_key = binascii.unhexlify('_______________________________')

Finally with the donwlinkSend.py -> use "00" or "03" on line 85 to deactivate and activate the alarm
