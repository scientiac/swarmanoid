# swarmanoid
Avengers, Assemble!!!

# Installation

Use nix package manager with `flakes` enabled to utilize the power of declerative configuration `flake.nix`

If you are not using `nixOS`:

1. First install the nix package manager from the link below:
(It should be as easy as pasting the command and following the script.)

https://nixos.org/download

2. Run the given script `enable-flakes-non-nixos.sh` with superuser permissions:

```
# With great power comes great responsibilities.
sudo ./etc/enable-flakes-non-nixos.sh
```

3. Run `nix develop`. For the first time it will take some time to install `opencv`, because it should be compiled manually with the `enableGTK2` flag to displaying windows using the `opencv` library itself. The environment will be loaded instantly upon running `nix develop` the next time.

4. `help` to see the help text.

> Note: Since, the development is done in the nix environment you should enter the environment each time running `nix develop` if you exit or closed the terminal.

> using `flake.nix` to add the dependencies and environment variable is highly recommended.

>To set up micropython and use it refer to [MICROPY.md][MICROPY.md]
![Pin Diagram](etc/ESP8266-Node-MCU.png)

| Label | GPIO   | Input         | Output                | Notes                                                           |
|-------|--------|---------------|-----------------------|-----------------------------------------------------------------|
| D0    | GPIO16 | no interrupt  | no PWM or I2C support | HIGH at bootused to wake up from deep sleep                     |
| D1    | GPIO5  | OK            | OK                    | often used as SCL (I2C)                                         |
| D2    | GPIO4  | OK            | OK                    | often used as SDA (I2C)                                         |
| D3    | GPIO0  | pulled up     | OK                    | connected to FLASH button, boot fails if pulled LOW             |
| D4    | GPIO2  | pulled up     | OK                    | HIGH at bootconnected to on-board LED, boot fails if pulled LOW |
| D5    | GPIO14 | OK            | OK                    | SPI (SCLK)                                                      |
| D6    | GPIO12 | OK            | OK                    | SPI (MISO)                                                      |
| D7    | GPIO13 | OK            | OK                    | SPI (MOSI)                                                      |
| D8    | GPIO15 | pulled to GND | OK                    | SPI (CS)Boot fails if pulled HIGH                               |
| RX    | GPIO3  | OK            | RX pin                | HIGH at boot                                                    |
| TX    | GPIO1  | TX pin        | OK                    | HIGH at bootdebug output at boot, boot fails if pulled LOW      |
| A0    | ADC0   | Analog Input  | X                     |


