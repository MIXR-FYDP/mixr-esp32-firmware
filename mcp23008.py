from machine import I2C
import MIXR

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


class mcp23008():
    def __init__(self, scl, sda, addr, interrupt, speed=SPEED_NORMAL):
        self.interrupt = interrupt
        self.addr = addr
        self.i2c = I2C(id=-1, scl=scl, sda=sda, freq=speed)
        self.i2c.init()

        # MCP23008 Configuration
        # SEQOP: Disable - 1
        # DISSLW: Enable - 0
        # HAEN: Enable  - 1
        # ODR: Open Drain - 1
        # INTPOL: Active low - 0

        # Get config reg
        print(self.i2c.readfrom_mem(addr=self.addr, REG_IOCON, nbytes=1))
        config = bytearray(1)
        config[0] = 0x2C
        self.i2c.writeto_mem(addr=self.addr, REG_IOCON, buf=config)
        print(self.i2c.readfrom_mem(addr=self.addr, REG_IOCON, nbytes=1))

        # Create a read buffer (1 byte)
        self.read_buffer = bytearray(1)
        self.write_buf = bytearray(1)

    def validate_channel(self, channel):
        if channel < 0 or channel > NUM_GPIO:
            return False
        return True

    def set_io_dir(self, list_input_pins, list_output_pins):
        for pin in list_input_pins, list_output_pins:
            if not validate_channel(pin):
                return -1

        io_dir = 0x00
        for input_pin in list_input_pins:
            io_dir = io_dir | (1 << input_pin)

        for output_pin in list_output_pins:
            io_dir = io_dir & ~(1 << output_pin)

        direction = bytearray[1]
        direction[0] = io_dir
        self.i2c.writeto_mem(addr=self.addr, REG_IODIR, buf=io_dir)

    def set_io_state(self, channel, state):
        if not validate_channel(self, channel):
            return -1
        self.write_buf[0] = self.i2c.readfrom_mem(addr=self.addr, REG_GPIO, nbytes=1)
        print(self.write_buf[0])
        if state:
            self.write_buf[0] = self.write_buf[0] | (1 << channel)
        else:
            self.write_buf[0] = self.write_buf[0] & ~(1 << channel)
        self.i2c.writeto_mem(addr=self.addr, REG_GPIO, buf=self.write_buf)

