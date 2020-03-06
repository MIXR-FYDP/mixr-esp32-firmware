from mcp23008 import mcp23008
from machine import Timer
from machine import Pin
from machine import ADC
import MIXR

class MixrPower:
    def __init__(self):
        self.i2c_pe = mcp23008(
            scl=MIXR.I2C1_SCL,
            sda=MIXR.I2C1_SDA,
            addr=MIXR.I2C1_PWR_I2C_PE_ADDR,
            interrupt=MIXR.I2C1_PE_INT,
        )
        self.list_input_pins = (MIXR.BAT_GAUGE_ALRT, MIXR.BAT_CHG_nPG, MIXR.BAT_CHG_STATUS)
        self.list_output_pins = (
            MIXR.nSW_EN,
            MIXR.PHANTOM_PWR_EN, #*
            MIXR.REG_49V2_EN, #*
            MIXR.nBAT_CHG_EN,
            MIXR.PWR_PE_DEBUG_LED,
        )

        self.i2c_pe.set_io_dir(self.list_input_pins, self.list_output_pins)

    def initialize(self):
        self.i2c_pe.set_io_state(MIXR.nSW_EN, 1)
        self.i2c_pe.set_io_state(MIXR.PHANTOM_PWR_EN, 0)
        self.i2c_pe.set_io_state(MIXR.REG_49V2_EN, 0)
        self.i2c_pe.set_io_state(MIXR.nBAT_CHG_EN, 1)
        self.i2c_pe.set_io_state(MIXR.PWR_PE_DEBUG_LED, 1)
                

    def toggle_power(self):
        current = self.i2c_pe.get_input_state(MIXR.PHANTOM_PWR_EN)
        if current == True:
            self.i2c_pe.set_io_state(MIXR.PHANTOM_PWR_EN, 0)
            self.i2c_pe.set_io_state(MIXR.REG_49V2_EN, 0)
        else:
            self.i2c_pe.set_io_state(MIXR.PHANTOM_PWR_EN, 1)
            self.i2c_pe.set_io_state(MIXR.REG_49V2_EN, 1)

    def print_power(self):
        adc = ADC(Pin(MIXR.MONITOR_48V))
        adc.atten(ADC.ATTN_11DB)
        x = adc.read()
        print("ADC READ: {}".format(x))
        print("Voltage: {}".format(x*3.3/4095))
        print("Voltage by ratio: {}".format(x*3.3/4095*MIXR.MONITOR_48V_RATIO))
        # adc.read()/3.3*4095
