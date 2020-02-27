import MIXR
from mcp23008 import mcp23008
import time
from machine import Timer

i2c_pe = mcp23008(
    scl=MIXR.I2C2_SCL,
    sda=MIXR.I2C2_SDA,
    addr=MIXR.I2C1_PWR_I2C_PE_ADDR,
    interrupt=MIXR.I2C2_PE_INT,
)


def check_buttons(timer):
    # Check if the list is empty first
    if i2c_pe.input_int_reg != 0:
        button = i2c_pe.input_int_reg
        print(button)
        i2c_pe.input_int_reg = 0


# Setup loop
# Start a software timer to poll the button queue every 100ms
tim = Timer(-1)
tim.init(period=250, mode=Timer.PERIODIC, callback=check_buttons)

list_input_pins = (MIXR.BAT_GAUGE_ALRT, MIXR.BAT_CHG_nPG, MIXR.BAT_CHG_STATUS)
list_output_pins = (
    MIXR.nSW_EN,
    MIXR.PHANTOM_PWR_EN,
    MIXR.REG_49V2_EN,
    MIXR.nBAT_CHG_EN,
    MIXR.PWR_PE_DEBUG_LED,
)

i2c_pe.set_io_dir(list_input_pins, list_output_pins)

while True:
    i2c_pe.set_io_state(MIXR.PWR_PE_DEBUG_LED, 1)
    time.sleep(0.25)
    i2c_pe.set_io_state(MIXR.PWR_PE_DEBUG_LED, 0)
    time.sleep(0.25)
