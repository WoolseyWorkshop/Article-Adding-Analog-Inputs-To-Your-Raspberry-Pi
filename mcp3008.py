#!/usr/bin/env python3

"""CircuitPython program that reads analog values from an MCP3008 ADC.

Description
-----------

CircuitPython program that reads both single-ended and differential channel
analog values from an MCP3008 analog-to-digital converter integrated circuit.

Circuit
-------

- MCP3008 ADC connected to the SPI0 serial bus with GPIO22 as the chip select.

Libraries/Modules
-----------------

- adafruit_mcp3xxx CircuitPython Library
    - https://circuitpython.readthedocs.io/projects/mcp3xxx/
    - Provides support for MCP3008 analog-to-digital converter.
- board CircuitPython Core Module
    - https://circuitpython.readthedocs.io/en/6.0.x/shared-bindings/board/
    - Access to Raspberry Pi GPIO pins and hardware.
- busio CircuitPython Core Module
    - https://circuitpython.readthedocs.io/en/6.0.x/shared-bindings/busio/
    - Provides SPI serial bus support.
- digitalio CircuitPython Core Module
    - https://circuitpython.readthedocs.io/en/6.0.x/shared-bindings/digitalio/
    - Provides basic digital pin IO support.
- RPi.GPIO Library (https://pypi.org/project/RPi.GPIO/)
    - Control and reset GPIO pins.
- time Standard Library (https://docs.python.org/3/library/time.html)
    - Access to sleep function.

Notes
-----

- Comments are Sphinx (reStructuredText) compatible.

TODO
----

Author(s)
---------

- Created by John Woolsey on 11/09/2020.
- Modified by John Woolsey on 11/17/2020.

Copyright (c) 2020 Woolsey Workshop.  All rights reserved.

Members
-------
"""


# Imports
from time import sleep
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO


# Global Constants/Variables/Instances
SPI = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)  # SPI bus
MCP3008_CS = digitalio.DigitalInOut(board.D22)  # MCP3008 chip select
MCP3008_SPI = MCP3008.MCP3008(SPI, MCP3008_CS)  # MCP3008 instance
ADC_CH0 = AnalogIn(MCP3008_SPI, MCP3008.P0)  # MCP3008 CH0 single channel input
ADC_CH1 = AnalogIn(MCP3008_SPI, MCP3008.P1)  # MCP3008 CH1 single channel input
ADC_DIFF = AnalogIn(
    MCP3008_SPI, MCP3008.P1, MCP3008.P0
)  # MCP3008 CH1-CH0 differential channel input


# Main
def main():
    """Main program entry."""

    print("Press CTRL-C to exit.")
    try:
        while True:
            # Print channel voltages and raw values
            print(f"ADC  CH0: {ADC_CH0.voltage:4.2f} V ({ADC_CH0.value:5d})")
            print(f"ADC  CH1: {ADC_CH1.voltage:4.2f} V ({ADC_CH1.value:5d})")
            print(f"ADC DIFF: {ADC_DIFF.voltage:4.2f} V ({ADC_DIFF.value:5d})")
            print()
            sleep(1)
    except KeyboardInterrupt:
        RPi.GPIO.cleanup()  # release all GPIO resources
        print("\nCleaned up GPIO resources.")


if __name__ == "__main__":  # required for generating Sphinx documentation
    main()
