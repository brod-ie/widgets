import logging
import time
import socket

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

def setup(hass, config):
    # Get the host from the configuration. Use DEFAULT_TEXT if no name is provided
    host = config[DOMAIN].get('host', '127.0.0.1')

    ikettle = iKettle(host)

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', host)

    hass.states.set('ikettle.OnButton', 'on')

    def press_button_on(call):
        ikettle.press_button_on()

    def press_button_off(call):
        ikettle.press_button_off()

    def press_button_100(call):
        ikettle.press_button_100()

    def press_button_95(call):
        ikettle.press_button_95()

    def press_button_80(call):
        ikettle.press_button_80()

    def press_button_65(call):
        ikettle.press_button_65()

    hass.services.register(DOMAIN, 'press_button_on', press_button_on)
    hass.services.register(DOMAIN, 'press_button_off', press_button_off)
    hass.services.register(DOMAIN, 'press_button_100', press_button_100)
    hass.services.register(DOMAIN, 'press_button_95', press_button_95)
    hass.services.register(DOMAIN, 'press_button_80', press_button_80)
    hass.services.register(DOMAIN, 'press_button_65', press_button_65)

    return True

class iKettle():

    BUFFER_SIZE = 10

    BUTTON_WARM = '8' # Select Warm button
    BUTTON_WARM_5 = '8005' # Warm option is 5 mins

    def __init__(self, host):
        self.host = host

    def _initiate(self):
        import time
        import socket

        # Open a connection to the kettle
        TCP_PORT = 2000
        INITIATE = b"HELLOKETTLE\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, TCP_PORT))
        s.send(INITIATE)
        return s

    def _button_code(button):
        SET_STRING = 'set sys output 0x'
        return (SET_STRING + button + '\n').encode()

    def _send_message(self, message):
        s = self._initiate()
        s.send(message)
        s.close()

    def press_button_on(self):
        BUTTON_ON = '4' # Select On button
        self._send_message(iKettle._button_code(BUTTON_ON))

    def press_button_off(self):
        BUTTON_OFF = '0' # Turn off
        self._send_message(iKettle._button_code(BUTTON_OFF))

    def press_button_100(self):
        BUTTON_100 = '80' # Select 100C button
        self._send_message(iKettle._button_code(BUTTON_100))

    def press_button_95(self):
        BUTTON_95 = '2' # Select 95C button
        self._send_message(iKettle._button_code(BUTTON_95))

    def press_button_80(self):
        BUTTON_80 = '4000' # Select 80C button
        self._send_message(iKettle._button_code(BUTTON_80))

    def press_button_65(self):
        BUTTON_65 = '200' # Select 65C button
        self._send_message(iKettle._button_code(BUTTON_65))
