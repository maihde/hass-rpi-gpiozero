---
layout: page
title: "Raspberry PI Gpiozero Binary Sensor"
description: "Instructions on how to integrate Gpiozero sensor capabilities into Home Assistant."
date: 2018-01-29 00:00
sidebar: true
comments: false
sharing: true
footer: true
logo: raspberry-pi.png
ha_category: Binary Sensor
ha_release: pre 0.7
ha_iot_class: "Local Push"
---

IMPORTANT: THIS COMPONENT IS NO LONGER NECESSARY.  THE BUILT-IN [remote_rpi_gpio](https://www.home-assistant.io/components/remote_rpi_gpio/) COMPONENT provides the same functionality.

The `rpi_gpiozero` binary sensor platform allows you to read sensor values of
the GPIOs of both local and remote GPIOs of your
[Raspberry Pis](https://www.raspberrypi.org/).

<p class='note'>
You need the `gpiozero` and `pigpio` modules installed on your system for this component to work.
</p>

### {% linkable_title Installation %}

<p class='note'>
The installation instructions assume you are running Hassbian
</p>

```bash
sudo su -s /bin/bash homeassistant
cd /srv/homeassistant
source bin/activate
pip install gpiozero pigpio
cd ~/.homeassistant
git clone https://github.com/maihde/hass-rpi-gpiozero.git
mkdir -p ~/.homeassistant/custom_components/binary_sensor
ln -s ~/.homeassistant/hass-rpi-gpiozero/rpi_gpiozero.py ~/.homeassistant/custom_components/rpi_gpiozero.py
ln -s ~/.homeassistant/hass-rpi-gpiozero/binary_sensor/rpi_gpiozero.py ~/.homeassistant/custom_components/binary_sensor/rpi_gpiozero.py
```

### {% linkable_title Configuration %}
To use a your Raspberry Pi's GPIO in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry for local GPIO
binary_sensor:
  - platform: rpi_gpiozero
    ports:
      11: PIR Office
      12: PIR Bedroom
```

To use a remote Raspberry Pi's GPIO in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry for local GPIO
binary_sensor:
  - platform: rpi_gpiozero
    host: '192.168.1.1'
    ports:
      11: PIR Office
      12: PIR Bedroom
```

Configuration variables:

- **ports** array (*Required*): Array of used ports.
  - **port: name** (*Required*): Port numbers (BCM mode pin numbers) and corresponding names.
- **pull_mode** (*Optional*): The internal pull to use (UP or DOWN). Default is UP.
- **bouncetime** (*Optional*): The time in milliseconds for port debouncing. Default is 50ms.
- **invert_logic** (*Optional*): If true, inverts the output logic to ACTIVE LOW. Default is false (ACTIVE HIGH).
- **host** (*Optional*): The hostname or IP address of a Raspberry Pi running `pigpiod`.
- **port** (*Optional*): The port number for connection to `pigpiod`.  Default is 8888.
For more details about the GPIO layout, visit the Wikipedia [article](https://en.wikipedia.org/wiki/Raspberry_Pi#GPIO_connector) about the Raspberry Pi.
