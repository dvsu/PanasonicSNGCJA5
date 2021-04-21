import smbus
from time import sleep


MASS_DENSITY_PM_TYPES = ["pm1.0", "pm2.5", "pm10"]
MASS_DENSITY_BLOCK_SIZE = 4
ADDRESS_MASS_DENSITY_HEAD = 0
ADDRESS_MASS_DENSITY_TAIL = 11
ADDRESS_MASS_DENSITY_LENGTH = (ADDRESS_MASS_DENSITY_TAIL - ADDRESS_MASS_DENSITY_HEAD) + 1
'''
Address register of mass density values is started from 0 (0x00) to 11 (0x0B).
Size of each value block is 4 bytes (32 bits) 
Total data length is 12 bytes

Value allocation
------------------------
PM1.0: byte 0 - byte 3 
PM2.5: byte 4 - byte 7
PM10: byte 8 - byte 11
'''

PARTICLE_COUNT_PM_TYPES = ["pm0.5", "pm1.0", "pm2.5", "N/A", "pm5.0", "pm7.5", "pm10"]
PARTICLE_COUNT_BLOCK_SIZE = 2
ADDRESS_PARTICLE_COUNT_HEAD = 12
ADDRESS_PARTICLE_COUNT_TAIL = 25
ADDRESS_PARTICLE_COUNT_LENGTH = (ADDRESS_PARTICLE_COUNT_TAIL - ADDRESS_PARTICLE_COUNT_HEAD) + 1
'''
Address register of particle count values is started from 12 (0x0C) to 25 (0x19)
Size of each value block is 2 bytes (16 bits)
Total data length is 14 bytes (or 12 bytes excluding byte 18 and 19)

Value allocation
------------------------
PM0.5: byte 12 - byte 13
PM1.0: byte 14 - byte 15
PM2.5: byte 16 - byte 17
N/A: byte 18 - byte 19
PM5.0: byte 20 - byte 21
PM7.5: byte 22 - byte 23
PM10: byte 24 - byte 25
'''

# Total raw data length stored in sensor register, i.e. 26 bytes
DATA_LENGTH_HEAD = ADDRESS_MASS_DENSITY_HEAD
DATA_LENGTH_TAIL = ADDRESS_PARTICLE_COUNT_TAIL
TOTAL_DATA_LENGTH = ADDRESS_MASS_DENSITY_LENGTH + ADDRESS_PARTICLE_COUNT_LENGTH


class SNGCJA5:

    def __init__(self, i2c_bus_no:int):
        self.i2c_address = 0x33
        self.i2c_bus = smbus.SMBus(i2c_bus_no)
        self.__mass_density_addresses = {pm_type: MASS_DENSITY_BLOCK_SIZE*order 
                                            for order, pm_type in enumerate(MASS_DENSITY_PM_TYPES)}

        self.__particle_count_addresses = {pm_type: PARTICLE_COUNT_BLOCK_SIZE*order
                                            for order, pm_type in enumerate(PARTICLE_COUNT_PM_TYPES)}

        self.__measurement_data = {
            "mass_density" : {},
            "particle_count" : {}
        }


    def get_mass_density_data(self, data:list) -> dict:

        return {pm_type: 
            float((data[address+3] << 24 | 
                data[address+2] << 16 | 
                data[address+1] << 8 | 
                data[address]) / 1000) 
                for pm_type, address in self.__mass_density_addresses.items()}


    def get_particle_count_data(self, data:list) -> dict:

        return {pm_type: 
            float((data[address+1] << 8 | data[address])) 
                for pm_type, address in self.__particle_count_addresses.items()
                if pm_type != "N/A"}


    def get_measurement(self) -> dict:

        # Data is updated by sensor every 1 second as per specification. Thus, 1-second delay is added
        # to prevent data duplication
        sleep(1) 

        try:
            data = self.i2c_bus.read_i2c_block_data(self.i2c_address, DATA_LENGTH_HEAD, TOTAL_DATA_LENGTH)

            mass_density_data = self.get_mass_density_data(data[ADDRESS_MASS_DENSITY_HEAD:ADDRESS_MASS_DENSITY_TAIL+1])
            particle_count_data = self.get_particle_count_data(data[ADDRESS_PARTICLE_COUNT_HEAD:ADDRESS_PARTICLE_COUNT_TAIL+1])

            self.__measurement_data = {
                "mass_density": mass_density_data,
                "particle_count": particle_count_data
            }

            return self.__measurement_data
        
        except:
            #TODO
            print("Failed to get measurement")
            pass
