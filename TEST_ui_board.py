from mcp23008 import mcp23008
from machine import Timer
from machine import Pin
import MIXR

import time


i2c_pe = mcp23008(
    scl=MIXR.I2C2_SCL,
    sda=MIXR.I2C2_SDA,
    addr=MIXR.I2C1_PWR_I2C_PE_ADDR,
    interrupt=MIXR.I2C2_PE_INT,
)

list_input_pins = (MIXR.RECORD_BUTTON, MIXR.PHANTOM_PWR_BUTTON, MIXR.WIFI_BUTTON)
list_output_pins = (
    MIXR.PHANTOM_PWR_LED,
    MIXR.RECORD_LED,
    MIXR.WIFI_STATUS_LED,
    MIXR.SPARE_LED,
    MIXR.UI_PE_DEBUG_LED,
)

i2c_pe.set_io_dir(list_input_pins, list_output_pins)


def check_buttons(timer):
    # Check if the list is empty first
    if i2c_pe.input_int_reg != 0:
        button = i2c_pe.input_int_reg
        print(button)
        i2c_pe.input_int_reg = 0


def pwr_button_irq():
    print("Power Button Pressed")


# Setup power button interrupt
pwr_int = Pin(MIXR.POWER_BUTTON, Pin.IN, None)
pwr_int.irq(trigger=Pin.IRQ_RISING, handler=pwr_button_irq)

# Setup loop
# Start a software timer to poll the button queue every 100ms
# tim = Timer(-1)
# tim.init(period=250, mode=Timer.PERIODIC, callback=check_buttons)

for pin in list_output_pins:
    i2c_pe.set_io_state(pin, 1)

while True:
    # for pin in list_output_pins:
    #     i2c_pe.set_io_state(pin, 1)
    # time.sleep(2)
    # for pin in list_output_pins:
    #     i2c_pe.set_io_state(pin, 0)
    # time.sleep(2)
    print(i2c_pe.input_int_reg)

    if i2c_pe.input_int_reg != 0:
        print("BUTTON PRESSED!!!")
        i2c_pe.input_int_reg = 0
