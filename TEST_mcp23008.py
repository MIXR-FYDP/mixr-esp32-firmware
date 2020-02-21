import MIXR
from mcp23008 import mcp23008
import time
from machine import Timer


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

list_input_pins = (0, 1)
list_output_pins = (2, 3, 4, 5, 6, 7)
i2c_pe = mcp23008(
    scl=MIXR.I2C2_SCL,
    sda=MIXR.I2C2_SDA,
    addr=MIXR.I2C1_PWR_I2C_PE_ADDR,
    interrupt=MIXR.I2C2_PE_INT,
)
i2c_pe.set_io_dir(list_input_pins, list_output_pins)
i2c_pe.set_io_state(2, 1)

while True:
    # pass
    # print(i2c_pe.input_queue)
    i2c_pe.set_io_state(2, 1)
    time.sleep(0.25)
    i2c_pe.set_io_state(2, 0)
    time.sleep(0.25)
