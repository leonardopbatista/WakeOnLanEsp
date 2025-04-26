# WakeOnLanEsp

WakeOnLanEsp is a Python-based system for waking up computers over the network using an ESP32 or ESP8266 device and MQTT communication. It supports sending Magic Packets via microcontrollers to remotely power on machines.

## Main Features

- Wake computers via Wake-on-LAN (Magic Packets) over MQTT.
- Support for ESP32 and ESP8266 devices.
- Simple graphical interface for sending wake-up commands.
- Modular and easy-to-extend code structure.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/leonardopbatista/WakeOnLanEsp.git
    cd WakeOnLanEsp
    ```

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Flash the corresponding firmware (ESP32 or ESP8266) located in the `/esp32` or `/esp8266` folder to your device.

4. Run the main Python application:

    ```bash
    python main.py
    ```

## Usage

- Configure your ESP device to connect to your MQTT broker.
- Set up the correct topics and payloads as expected by the ESP firmware.
- Use the graphical interface to send a wake-up command to the desired machine.

## Repository Structure

- `/core`: Core application logic.
- `/utils`: Utility functions.
- `/esp32` and `/esp8266`: Firmware for ESP microcontrollers.
- `/graphical_interface`: GUI implementation.
- `/custom_widgets`: Custom components for the GUI.

## Contribution

Feel free to contribute by suggesting improvements, fixing issues, or submitting pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
