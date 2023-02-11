import time
import board
import digitalio
from hx711_gpio import *
from GETLogger import *
from massSensor import *
#this is the "LOGTOSEVER" code


# set up data structure
data = {}
data["picoID"] = "HayHay"
data["sensor"] = "Mass"
data["reading"] = ""
data["units"] = "g"

# setup pins
pin_OUT = digitalio.DigitalInOut(board.GP5)
pin_SCK = digitalio.DigitalInOut(board.GP6)
pin_SCK.direction = digitalio.Direction.OUTPUT



hx = HX711(pin_SCK, pin_OUT)
hx.OFFSET = 0 # -150000
hx.set_gain(128)
time.sleep(0.050)
#scale = 25000.0



logger = GETLogger("TFS Students", "Fultoneagles", "http://popu.local/logger/logger.php")

#calabrate the sensor using reading (x) and the mass (y) of the scale for two different masses.
sensor = massSensor(2,2,3,3)

while True:
    try:
        #scale equation
        x = hx.read()
        real_mass = sensor.ymass(x)

        # real_mass = sensor.getMB()*x+63.5
#EACH SCALE HAST TO BE CALIBRATED I.E A 20Kg SCALE WILL HAVE A DIFFERENT EQUATION TO A 5Kg SCALE.
        data["reading"] = real_mass
        if old_mass != real_mass:
            logger.log(data)
        old_mass = real_mass
        time.sleep(5)
    except Exception as e:
        print("Error:\n", str(e))
