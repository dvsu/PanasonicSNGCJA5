# Panasonic-SN-GCJA5

## **Introduction**

Python driver for Panasonic SN-GCJA5 particulate matter (PM) sensor. Tested on Raspberry Pi Zero/Zero W/3B+/4B<br>

## **Wiring**

Panasonic SN-GCJA5 uses `JST SM05B-GHS-TB(LF)(SN)` connector and requires 3.3V and 5V for direct wiring. 
Fortunately, Raspberry Pi GPIOs are 3.3V by default and also supports dual power supply voltages, 3.3V and 5V. 
Please refer to sensor specification sheet and table below for wiring guide.  

| Sensor Connector Pin | Symbol | Recommended Voltage | Description | RPi Physical Pin | RPi I/O |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Pin 1 | TX | 3.3V | UART TX *(unused if using I2C protocol)* | *not connected* | |
| Pin 2 | SDA | 3.3V | I2C Data | Pin 3 | GPIO2 (I2C1 SDA) |
| Pin 3 | SCL | 3.3V | I2C Clock | Pin 5 | GPIO3 (I2C1 SCL) |
| Pin 4 | GND | 0V | Ground | Pin 6 | Ground |
| Pin 5 | VDD | 5V | Power supply | Pin 4 | 5v Power |

More details about Raspberry Pi pinout  
<https://pinout.xyz/>  

## **Examples**

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
        "sensor_data": {
            "mass_density": {
                "pm1.0": <float>,
                "pm2.5": <float>,
                "pm10": <float>
            },
            "particle_count": {
                "pm0.5": <float>, 
                "pm1.0": <float>, 
                "pm2.5": <float>,
                "pm5.0": <float>, 
                "pm7.5": <float>, 
                "pm10": <float>
            },
            "mass_density_unit": "ug/m3",
            "particle_count_unit": "none" 
        },
        "timestamp": <int> # seconds since the Unix epoch
    }
    '''
    sleep(5)
```

## **Dependencies and Installation Instructions**

`smbus`

```none
pip install smbus
```

## **Limitation**

Currently, this driver only supports **I2C** protocol
