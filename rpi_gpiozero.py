"""
Support for controlling GPIO pins of a Raspberry Pi with gpiozero
"""
# pylint: disable=import-error
import logging

from homeassistant.const import (
    EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)

REQUIREMENTS = ['gpiozero==1.4.0', 'pigpio==1.38']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'rpi_gpiozero'

_DEVICES = set()
_REMOTE_FACTORY = {}

# pylint: disable=no-member
def setup(hass, config):
    """Set up the Raspberry PI GPIO component."""
    import os
    # Make the default pin factory 'mock' so that
    # it other pin factories can be loaded after import
    os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'
    import gpiozero

    def cleanup_gpiozero(event):
        """Stuff to do before stopping."""
        for dev in _DEVICES:
            try: 
                _LOGGER.info("closing device %s", dev)
                dev.close()
            except:
                _LOGGER.exception("unexpected error closing device %s", dev)
        _DEVICES.clear()

    def prepare_gpiozero(event):
        """Stuff to do when home assistant starts."""
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup_gpiozero)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare_gpiozero)
    return True

def get_pinfactory(hostport=None):
    """
    Get the pinfactory for the configured hostport.

    :param hostport: the host/port tuple, when None local GPIO is used
    """

    # TODO do we need any thread safety here?
    if hostport:
        from gpiozero.pins.pigpio import PiGPIOFactory
        if hostport not in _REMOTE_FACTORY:
            _LOGGER.info(
                "Creating pigpiod connection to %s:%s",
                hostport[0],
                hostport[1]
            )
            _REMOTE_FACTORY[hostport] = PiGPIOFactory(
                host=hostport[0],
                port=hostport[1]
            )
        pin_factory = _REMOTE_FACTORY[hostport]
    else:
        from gpiozero.pins.rpigpio import RPiGPIOFactory
        if _LOCAL_FACTORY == None:
            _LOCAL_FACTORY = RPiGPIOFactory()
        pin_factory = _LOCAL_FACTORY
    return pin_factory

def setup_button(port, pull_mode, bouncetime, hostport):
    """
    Set up a GPIO as input (a.k.a Button in Gpiozero.

    :param port: the GPIO port using BCM numbering.
    :param pull_mode: 'UP' or 'DOWN' to pull the GPIO pin high or low.
    :param bouncetime: the software bounce compensation in msec.
    :param hostport: the remote host/port, None for local.
    """
    from gpiozero import Button
 
    if pull_mode.upper() not in ('UP', 'DOWN'):
        raise ValueError("invalid pull_mode %s", pull_mode)
   
    if bouncetime < 0:
        raise ValueError("invalid bouncetime %s", bouncetime)

    btn = Button(
        port,
        pull_up=(pull_mode.upper() == 'UP'),
        bounce_time=float(bouncetime) / 1e3, 
        pin_factory=get_pinfactory(hostport)
    )

    # add the button to the _DEVICES list so we can cleanup on shutdown
    _DEVICES.add(btn)

    return btn
