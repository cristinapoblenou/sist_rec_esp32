import time
import machine
import dht
from machine import Pin, ADC, SoftI2C
from umqtt.simple import MQTTClient

from ssd1306 import SSD1306_I2C


def do_connect(SSID, PASSWORD, oled=None):
    import network  # importa el módulo network
    sta_if = network.WLAN(network.STA_IF)  # instancia el objeto -sta_if- para controlar la interfaz STA
    if not sta_if.isconnected():  # si no existe conexión...
        sta_if.active(True)  # activa el interfaz STA del ESP32
        try:
            sta_if.connect(SSID, PASSWORD)  # inicia la conexión con el AP
        except Exception:
            machine.reset()
        if oled:
            oled.fill(0)
            oled.text("Conectando a la ", 10, 10)
            oled.text("red " + SSID + "...", 10, 20)
            oled.show()

        else:
            print('Conectando a la red', SSID + "...")
        while not sta_if.isconnected():  # ...si no se ha establecido la conexión...
            pass  # ...repite el bucle...
    if oled:
        oled.fill(0)
        oled.text("Configuración de red (IP/netmask/gw/DNS): " + str(sta_if.ifconfig()), 10, 10)
        oled.show()

    else:
        print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())
    time.sleep(2)


def get_client(oled):
    do_connect("ECAIB", "08034138", oled=oled)
    client = MQTTClient(
        client_id="sistema_regat",
        server="mqtt.flespi.io",
        port=1883,
        user="q0ckhaAGh2EVOwM7oTxeMaJ7cSlFlp4zd5Hl37PaXjUBGuwSdUWPUtKUbVnk8gKb",
        password=""
    )
    client.connect()

    return client


def main():
    # OLED
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    oled_width = 128  # definir oled width and height
    oled_height = 64
    oled = SSD1306_I2C(oled_width, oled_height, i2c)  # create an SSD1306_I2C object called oled



    # capactive soil
    hum_data_port = 34
    POT = ADC(Pin(hum_data_port))
    POT.atten(ADC.ATTN_11DB)
    HUM_MAX = 3640
    HUM_MIN = 1450



    # capactive soil 2
    hum_data_port_2 = 32
    POT_2 = ADC(Pin(hum_data_port_2))
    POT_2.atten(ADC.ATTN_11DB)
    HUM_MAX_2 = 3640
    HUM_MIN_2 = 1450

    # definir variable rgb con sus pines
    green = Pin(26, Pin.OUT)
    red = Pin(25, Pin.OUT)
    blue = Pin(27, Pin.OUT)
    red.off()
    green.off()
    blue.off()

    # definir pin motor
    motor_1 = Pin(18, Pin.OUT)
    motor_1.off()

    # sensor dht
    sensor = dht.DHT11(Pin(0))
    # temp & hum max min
    maxim_temp = 0
    minim_temp = 100
    maxim_hum = 0
    minim_hum = 100

    oled.fill(0)
    oled.show()
    time.sleep(1)



    while True:
        oled.fill(0)

        # Mostrar por pantalla la temperatura y humedad (dht)
        sensor.measure()
        oled.text("temp: {}. hum {}".format(sensor.temperature(), sensor.humidity()), 0, 0)


        # capactive soil sensor numero 1
        HUM_DATA = POT.read()
        HUM = 100 / (HUM_MIN - HUM_MAX) * (HUM_DATA - HUM_MAX)  # formula calculo humedad %
        oled.text("HUM: " + str(int(HUM)), 0, 20)
        oled.text(str(HUM_DATA), 0, 30)
        oled.text(" ", 10, 40)


        # capactive soil sensor numero 2
        HUM_DATA_2 = POT_2.read()
        HUM_2 = 100 / (HUM_MIN_2 - HUM_MAX_2) * (HUM_DATA_2 - HUM_MAX_2)  # formula calculo humedad %
        oled.text("HUM_2: " + str(int(HUM_2)), 60, 20)
        oled.text("2: " + str(HUM_DATA_2), 60, 30)
        oled.text(" ", 10, 40)

        '''
        if POT.read() >= 2900:  # si la humedad (sin%) es mayor que x la led roja se enciende
            red.on()
            green.off()
        elif POT.read() < 2900:  # si la humedad (sin%) es menor que x la led verde se enciende
            red.on()
            green.on()
            red.off()
        
        # condicion: si la humedad (en %) es mayor a x, enciende el motor
        if HUM < 15:
            motor_1.on()
        else:
            motor_1.off()
        '''

        #TEST
        if POT.read()>= 2900 or POT_2.read() < 2900:  # si la humedad (sin%) es mayor que x la led roja se enciende
            red.on()
            green.off()
        elif POT.read() < 2900 or POT_2.read() < 2900:  # si la humedad (sin%) es menor que x la led verde se enciende
            red.on()
            green.on()
            red.off()

        # condicion: si la humedad (en %) es mayor a x, enciende el motor
        if HUM < 15 or HUM_2 < 15:
            motor_1.on()
        else:
            motor_1.off()

        '''
        # que te de el minimo y el maximo de la temp registrada
        value_dht = [sensor.temperature()]

        for valor in value_dht:
            if valor < minim_temp:
                minim_temp = valor
            if valor > maxim_temp:
                maxim_temp = valor
        oled.text("TEMP: " + str(maxim_temp) + "  " + str(minim_temp), 10, 50)

        # que te de el minimo y el maximo de la hum registrada
        value_dht_hum = [sensor.humidity()]

        for valor_1 in value_dht_hum:
            if valor_1 < minim_hum:
                minim_hum = valor_1
            if valor_1 > maxim_hum:
                maxim_hum = valor_1
        oled.text("HUM:   " + str(maxim_hum) + " " + str(minim_hum), 10, 70)
     
        '''
        oled.show()
        time.sleep(0.2)


main()
