# Picoc.py - For Raspberry Pi Pico WH
from machine import UART, Pin
import time

class UARTHandler:
    def __init__(self, uart_id=0, baud_rate=115200, tx_pin=0, rx_pin=1):
        try:
            self.uart = UART(uart_id, 
                           baud_rate,
                           tx=Pin(tx_pin),
                           rx=Pin(rx_pin),
                           bits=8,
                           parity=None,
                           stop=1)
            print(f"UART initialized on ID {uart_id}")
            self.uart.init(baud_rate, bits=8, parity=None, stop=1)
        except Exception as e:
            print(f"Failed to initialize UART: {e}")
            raise e

    def send_message(self, message):
        try:
            self.uart.write(f"{message}\n".encode('utf-8'))
            #print(f"Sent: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def receive_message(self):
        try:
            if self.uart.any():
                ReceivedString = self.uart.readline().decode('utf-8').rstrip()
                if ReceivedString == "LEDOn":
                    led=Pin('LED', Pin.OUT)
                    led.value(True) #turn board LED on
                    return "LED turned on"
                elif ReceivedString == "LEDOff":
                    led=Pin('LED', Pin.OUT)
                    led.value(False) #turn board LED off
                    return "LED turned off"
                elif ReceivedString == "LED15On":
                    led=Pin(15, Pin.OUT)
                    led.value(True) #Turn 15 LED on
                    return "LED 15 turned on"
                elif ReceivedString == "LED15Off":
                    led=Pin(15, Pin.OUT)
                    led.value(False) #Turn 15 LED on
                    return "LED 15 turned off"
                else:
                    #Return what text was sent
                    return ReceivedString
            return None
        except Exception as e:
            print(f"Failed to receive message: {e}")
            return None

def main():
    uart_handler = UARTHandler()
    
    while True:       
        # Check for incoming messages
        received = uart_handler.receive_message()
        if received:
            print(f"Received: {received}")
            # Echo back the received message
            uart_handler.send_message(f"Pico W received: {received}")
        time.sleep(1)

if __name__ == "__main__":
    main()