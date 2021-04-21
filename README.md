# Panasonic-SN-GCJA5
<br>

### **Introduction**
<br>

Python driver for Panasonic SN-GCJA5 particulate matter (PM) sensor. Tested on Raspberry Pi Zero/Zero W/3B+/4B<br>
<br>


### **Wiring**
<br>

Panasonic SN-GCJA5 uses `JST SM05B-GHS-TB(LF)(SN)` connector and requires 3.3V and 5V for direct wiring. 
Fortunately, Raspberry Pi GPIOs are 3.3V by default and also supports dual power supply voltages, 3.3V and 5V. 
Please refer to sensor specification sheet and table below for wiring guide.
<br>

| Sensor Connector Pin | Symbol | Recommended Voltage | Description | RPi Physical Pin | RPi I/O |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Pin 1 | TX | 3.3V | UART TX *(unused if using I2C protocol)* | *not connected* | |
| Pin 2 | SDA | 3.3V | I2C Data | Pin 3 | GPIO2 (I2C1 SDA) |
| Pin 3 | SCL | 3.3V | I2C Clock | Pin 5 | GPIO3 (I2C1 SCL) |
| Pin 4 | GND | 0V | Ground | Pin 6 | Ground |
| Pin 5 | VDD | 5V | Power supply | Pin 4 | 5v Power |
<br>

More details about Raspberry Pi pinout<br>
<https://pinout.xyz/><br>
<br>


### **Examples**
<br>

```python
from time import sleep
from sngcja5 import SNGCJA5


# If SDA and SCL are connected to I2C bus 1, then i2c_bus_no = 1
pm_sensor = SNGCJA5(i2c_bus_no=1)

while True:

    # The get_measurement method returns a dictionary of all measurement value 
    result = pm_sensor.get_measurement()

    print(result)
    '''
    Structure of result

    {
        "mass_density" : {
            "pm1.0": xx.xx,
            "pm2.5": xx.xx,
            "pm10": xx.xx,
        },
        "particle_count" : {
            "pm0.5": xx.xx, 
            "pm1.0": xx.xx, 
            "pm2.5": xx.xx,
            "pm5.0": xx.xx, 
            "pm7.5": xx.xx, 
            "pm10": xx.xx
        }
    }
    '''

    sleep(1)

```
<br>

### **Dependencies and Installation Instructions**
<br>

* `smbus`<br>
    ```
    pip install smbus
    ```
<br>
<br>

### **Limitation**
<br>

This driver only works using **I2C** protocol
