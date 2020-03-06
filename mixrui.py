from mcp23008 import mcp23008
from machine import Timer
from machine import Pin
import MIXR
import mixrpower

import time

RECORD_INT = 1
PHANTOM_INT = 2
WIFI_INT = 4

class MixrUI:
    def __init__(self):
        self.i2c_pe = mcp23008(
            scl=MIXR.I2C2_SCL,
            sda=MIXR.I2C2_SDA,
            addr=MIXR.I2C1_PWR_I2C_PE_ADDR,
            interrupt=MIXR.I2C2_PE_INT,
        )

        self.list_input_pins = (MIXR.RECORD_BUTTON, MIXR.PHANTOM_PWR_BUTTON, MIXR.WIFI_BUTTON)
        self.list_output_pins = (
            MIXR.PHANTOM_PWR_LED,
            MIXR.RECORD_LED,
            MIXR.WIFI_STATUS_LED,
            MIXR.POWER_LED,
            MIXR.UI_PE_DEBUG_LED,
        )

        self.i2c_pe.set_io_dir(self.list_input_pins, self.list_output_pins)
        self.mixrPower = mixrpower.MixrPower()

    def initialize(self):
        for pin in self.list_output_pins:
            self.i2c_pe.set_io_state(pin, 0)
        self.i2c_pe.set_io_state(MIXR.UI_PE_DEBUG_LED, 1)
        self.i2c_pe.set_io_state(MIXR.POWER_LED, 1)
        self.init_power_button()

        # Start a software timer to poll the button queue every 100ms
        tim = Timer(-1)
        tim.init(period=100, mode=Timer.PERIODIC, callback=self.irq_mixr_input)

        self.mixrPower.initialize()

    # Setup power button interrupt
    def init_power_button(self):
        # self.i2c_pe.set_io_state(MIXR.SPARE_LED, 1)
        self.pwr_int = Pin(MIXR.POWER_BUTTON, Pin.IN, None)
        self.pwr_int.irq(trigger=Pin.IRQ_RISING, handler=self.pwr_button_irq)


    def pwr_button_irq(self, arg):
        pin = MIXR.POWER_LED
        current = self.i2c_pe.get_input_state(pin)
        print("current: {}".format(current))
        if current == True:
            self.i2c_pe.set_io_state(pin, 0)
        else:
            self.i2c_pe.set_io_state(pin, 1)
        print("Power Button Pressed!")

    def irq_mixr_input(self, timer):
        # # Check if the list is empty first
        # print("int reg: {}".format(self.i2c_pe.input_int_reg))
        if self.i2c_pe.input_int_reg != 0:
            button = self.i2c_pe.input_int_reg
            print("button: {}".format(button))
            self.i2c_pe.input_int_reg = 0
            if button == RECORD_INT:
                self.handle_record()
            elif button == WIFI_INT:
                self.handle_wifi()
            elif button == PHANTOM_INT:
                self.handle_phantom_pwr()
            else:
                print("Unrecognized Button pressed!")
        # self.i2c_pe.input_int_reg = 0

    def handle_record(self):
        print("recoooord")
        self.toggle_led(MIXR.RECORD_LED)
        #send signal to STM to start recording

    def handle_wifi(self):
        print("wiiifi")
        self.toggle_led(MIXR.WIFI_STATUS_LED)

    def handle_phantom_pwr(self):
        print("phantom" )
        self.toggle_led(MIXR.PHANTOM_PWR_LED)
        self.mixrPower.toggle_power()
        self.mixrPower.print_power()

    def toggle_led(self, pin):
        current = self.i2c_pe.get_input_state(pin)
        if current == True:
            self.i2c_pe.set_io_state(pin, 0)
        else:
            self.i2c_pe.set_io_state(pin, 1)


ui = MixrUI()
ui.initialize()
while True:
    time.sleep(2)
    ui.toggle_led(MIXR.UI_PE_DEBUG_LED)