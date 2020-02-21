from machine import I2C
from machine import Pin

# I2C Speeds
SPEED_NORMAL = 100000
SPEED_FAST = 400000

# Registers
REG_IODIR = 0x00
REG_IPOL = 0x01
REG_GPINT_EN = 0x02
REG_DEFVAL = 0x03
REG_INTCON = 0x04
REG_IOCON = 0x05
REG_GPPU = 0x06
REG_INTF = 0x07
REG_INTCAP = 0x08
REG_GPIO = 0x09
REG_OLAT = 0x0A

# Number of GPIOS
NUM_GPIO = 8


class mcp23008:
    def __init__(self, scl, sda, addr, interrupt=None, speed=SPEED_NORMAL):
        self.interrupt = Pin(interrupt, Pin.IN, None)
        self.interrupt.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler)
        self.addr = addr
        self.i2c = I2C(1, scl=Pin(scl), sda=Pin(sda), freq=speed)

        # Create a read and write buffer (1 byte each)
        self.read_buffer = bytearray(1)
        self.write_buffer = bytearray(1)
        # MCP23008 Configuration
        # SEQOP: Disable - 1
        # DISSLW: Enable - 0
        # HAEN: Enable  - 1
        # ODR: Open Drain - 1
        # INTPOL: Active low - 0

        # Set config reg
        self.write_buffer[0] = 0x2C
        self.i2c.writeto_mem(self.addr, REG_IOCON, self.write_buffer)

        # Set default values to 0 (active high inputs)
        self.write_buffer[0] = 0x00
        self.i2c.writeto_mem(self.addr, REG_DEFVAL, self.write_buffer)

        # Disable pull-up resistors
        self.i2c.writeto_mem(self.addr, REG_GPPU, self.write_buffer)
        print("MCP23008 Initialized...")

        self.input_int_reg = 0

    def validate_channel(self, channel):
        if channel < 0 or channel > NUM_GPIO:
            return False
        return True

    def set_io_dir(self, list_input_pins, list_output_pins):
        for pin in list_input_pins:
            if not self.validate_channel(pin):
                return -1

        for pin in list_output_pins:
            if not self.validate_channel(pin):
                return -1

        self.write_buffer[0] = 0x00

        for input_pin in list_input_pins:
            self.write_buffer[0] = self.write_buffer[0] | (1 << input_pin)

        # Enable interrupt on all input pins
        self.i2c.writeto_mem(self.addr, REG_GPINT_EN, self.write_buffer)

        # Compare all input pins to the default values
        self.i2c.writeto_mem(self.addr, REG_INTCON, self.write_buffer)

        # Set output pins
        for output_pin in list_output_pins:
            self.write_buffer[0] = self.write_buffer[0] & ~(1 << output_pin)
        self.i2c.writeto_mem(self.addr, REG_IODIR, self.write_buffer)

    def set_io_state(self, channel, state):
        if not self.validate_channel(channel):
            return -1
        self.read_buffer = self.i2c.readfrom_mem(self.addr, REG_GPIO, 1)
        self.write_buffer[0] = self.read_buffer[0]
        if state:
            self.write_buffer[0] = self.write_buffer[0] | (1 << channel)
        else:
            self.write_buffer[0] = self.write_buffer[0] & ~(1 << channel)
        self.i2c.writeto_mem(self.addr, REG_GPIO, self.write_buffer)

    def get_input_state(self, channel):
        if not self.validate_channel(channel):
            return -1

        self.read_buffer = self.i2c.readfrom_mem(self.addr, REG_GPIO, 1)
        return bool(self.read_buffer[0] | (1 << channel))

    def irq_handler(self, pin):
        # Get the pins that set the interrupt
        self.read_buffer = self.i2c.readfrom_mem(self.addr, REG_INTF, 1)
        self.input_int_reg = self.read_buffer[0]
