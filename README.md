# Raspberry Pi HID Controller

This project enables a Raspberry Pi Zero to act as a Human Interface Device (HID), specifically emulating keystrokes. It can be used for various automation tasks where controlling a device via keyboard inputs is needed.

## Features
- Emulates keyboard keystrokes via HID on a Raspberry Pi Zero.
- Configurable to send specific keystrokes based on pre-programmed instructions.
- Can be extended for use in automation and testing environments.

## Prerequisites

### Hardware
- **Raspberry Pi Zero (or compatible models)**
- **USB cable** to connect the RPI to a target device as a HID.
- **MicroSD card** with Raspberry Pi OS installed.

### Software
- **Raspberry Pi OS** (Lite version recommended for minimal setup)
- Python 3.x installed on the RPI.

## Setup

### Configure RPI as HID

For detailed instructions on how to enable HID on Raspberry Pi, refer to this [tutorial on Random Nerd Tutorials](https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/).



## How to Start & Run

### On Windows
1. **Get the suffix from the local IP address**:
   Use the `ipconfig` command to find your local IP address (e.g., `192.168.0.12`). The suffix you need is `12`.
   
2. **Start the Server**:
```bash
cd /ScreenController
python main.py
```
   
### On Raspberry Pi

1. **Prepare the Device:** Plug in the USB cable to connect the Raspberry Pi to the target device.

2. **Run the HID Script:**

```bash
cd /home/pi/rpi-hid-gadget/HIDController
python main.py 12
```
