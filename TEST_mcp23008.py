import MIXR
from mcp23008 import mcp23008

list_input_pins = (0, 1)
list_output_pins = (2, 3, 4, 5, 6, 7)
i2c_pe = mcp23008(scl=MIXR.I2C2_SCL, sda=MIXR.I2C2_SDA, addr=MIXR.I2C1_PWR_I2C_PE_ADDR, interrupt=MIXR.I2C2_PE_INT)
i2c_pe.set_io_dir(list_input_pins, list_output_pins)
i2c_pe.set_io_state(2, 1)