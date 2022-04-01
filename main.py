import time
import machine
import dht
from machine import Pin, ADC, SoftI2C
from ssd1306 import SSD1306_I2C


def main():
    hum_data_port = 34
    POT = ADC(Pin(hum_data_port))
    POT.atten(ADC.ATTN_11DB)
    HUM_MAX = 3640
    HUM_MIN = 1450

    # definir variable rgb con sus pines
    red = Pin(32, Pin.OUT)
    green = Pin(25, Pin.OUT)
    blue = Pin(27, Pin.OUT)

    # definir pin motor
    motor_1 = Pin(18, Pin.OUT)

    sensor = dht.DHT11(Pin(0))

    # oled
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

    # temp & hum max min
    maxim_temp = 0
    minim_temp = 100
    maxim_hum = 0
    minim_hum = 100


    # definir oled width and height
    oled_width = 128
    oled_height = 64
    # create an SSD1306_I2C object called oled
    oled = SSD1306_I2C(oled_width, oled_height, i2c)

    red.off()
    green.off()
    blue.off()

    oled.fill(0)
    oled.show()
    time.sleep(1)

    while True:
        oled.fill(0)

        sensor.measure()
        oled.text("temp: {}. hum {}".format(sensor.temperature(), sensor.humidity()), 0, 0)

        HUM_DATA = POT.read()
        HUM = 100 / (HUM_MIN - HUM_MAX) * (HUM_DATA - HUM_MAX)
        oled.text("HUMITAT : " + str(int(HUM)), 10, 20)
        oled.text(str(HUM_DATA), 0, 30)
        oled.text(" ", 10, 40)

        # condicion humedad (sin %)
        if POT.read() >= 2900:
            red.on()
            green.off()
        elif POT.read() < 2900:
            green.on()
            red.off()

        # condicion: si la humedad (en %) es mayor a x, enciende el motor
        if HUM > 11:
            motor_1.on()
        else:
            motor_1.off()

        # que te de el minimo y el maximo de la temp registrada
        value_dht = [sensor.temperature()]


        for valor in value_dht:
            if valor < minim_temp:
                minim_temp = valor
            if valor > maxim_temp:
                maxim_temp = valor
        oled.text("TEMP: "+str(maxim_temp) + "  " + str(minim_temp), 20, 40)

        # que te de el minimo y el maximo de la hum registrada
        value_dht_hum = [sensor.humidity()]


        for valor_1 in value_dht_hum:
            if valor_1 < minim_hum:
                minim_hum = valor_1
            if valor_1 > maxim_hum:
                maxim_hum = valor_1
        oled.text("HUM:   " + str(maxim_hum) + " " + str(minim_hum), 20, 50)
        oled.show()

        time.sleep(0.1)


main()
