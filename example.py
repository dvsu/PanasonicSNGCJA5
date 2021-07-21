from time import sleep
from sngcja5 import SNGCJA5


pm_sensor = SNGCJA5(i2c_bus_no=3)

while True:
    print(pm_sensor.get_measurement())
    sleep(5)