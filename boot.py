# import machine
#
# from ssd1306 import SSD1306_I2C
#
# try:
#   import usocket as socket
# except:
#   import socket
#
# from machine import Pin
# import network
# from machine import Pin, ADC, SoftI2C
#
# import time
#
# import esp
# esp.osdebug(None)
#
# import gc
# gc.collect()
#
#
# def do_connect(SSID, PASSWORD, oled=None):
#   import network  # importa el módulo network
#   sta_if = network.WLAN(network.STA_IF)  # instancia el objeto -sta_if- para controlar la interfaz STA
#   if not sta_if.isconnected():  # si no existe conexión...
#     count = 0
#     sta_if.active(True)  # activa el interfaz STA del ESP32
#     #sta_if.ifconfig(('192.168.130.24', '255.255.255.0', '192.168.130.1', '8.8.8.8'))
#     sta_if.connect(SSID, PASSWORD)  # inicia la conexión con el AP
#     if oled:
#       oled.fill(0)
#       oled.text("Conectando a la ", 10, 10)
#       oled.text("red " + SSID + "...", 10, 20)
#       oled.show()
#
#     else:
#       print('Conectando a la red', SSID + "...")
#     while not sta_if.isconnected():  # ...si no se ha establecido la conexión...
#       time.sleep(0.1)
#       count+=1
#
#       if count > 100:
#         machine.reset()
#
#       pass  # ...repite el bucle...
#
#   if oled:
#     oled.fill(0)
#     oled.text("Configuración de red (IP/netmask/gw/DNS): " + str(sta_if.ifconfig()), 10, 10)
#     oled.show()
#
#   else:
#     print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())
#   time.sleep(2)
#
#
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
#
# # temp & hum max min
# maxim_temp = 0
# minim_temp = 100
# maxim_hum = 0
# minim_hum = 100
#
# # definir oled width and height
# oled_width = 128
# oled_height = 64
# # create an SSD1306_I2C object called oled
# oled = SSD1306_I2C(oled_width, oled_height, i2c)
#
# #do_connect("ECAIB", "08034138", oled=oled)