import MIXR
from machine import UART
from machine import Pin


class stm_esp_uart:
    def __init__(
        self, esp32_uart_port=MIXR.STM_ESP_UART, esp_uart_baud=MIXR.STM_ESP_UART_BAUD
    ):
        self.uart = UART(esp32_uart_port, esp_uart_baud)
        self.uart.init(esp_uart_baud, bits=8, parity=None, stop=1)

    def send_data(self, mode, data):
        data_to_send = mode << 8 | data
        self.uart.write(data_to_send)

    def receive_data_irq(self):
        debug_led = Pin(2, Pin.Out)
        debug_led.value(1)
