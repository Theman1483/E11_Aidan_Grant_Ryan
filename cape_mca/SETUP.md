# CapeMCA Raspberry Pi Setup

## Dependencies

1. Install the libusb system library:

   ```bash
   sudo apt install libusb-1.0-0-dev
   ```

2. Install the Python USB package:

   ```bash
   pip install pyusb
   ```

## USB Permissions

By default, USB devices require root access. To allow your user account to
communicate with the MCA without `sudo`, create a udev rule:

```bash
sudo nano /etc/udev/rules.d/50-capemca.rules
```

Add this line:

```
SUBSYSTEMS=="usb",ATTRS{idVendor}=="4701",ATTRS{idProduct}=="0290",GROUP="users",MODE="0666",ATTR{power/autosuspend}="-1",ATTR{power/autosuspend_delay_ms}="-1"
```

This sets permissions and also disables USB autosuspend for the MCA device,
which can cause timeout errors if the device sits idle between reads.

Then reload the rules:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Unplug and replug the MCA for the rule to take effect, or reboot.

You can verify autosuspend is disabled by finding the device's sysfs path:

```bash
# List USB device paths
ls /sys/bus/usb/devices/

# Find the one with vendor ID 4701
cat /sys/bus/usb/devices/1-1/idVendor    # try different paths like 1-1, 1-1.1, etc.

# Check autosuspend is disabled (-1)
cat /sys/bus/usb/devices/<your-path>/power/autosuspend_delay_ms
```

## Verify the Device

After plugging in the MCA, confirm it appears on the USB bus:

```bash
lsusb | grep 4701
```

You should see a device with `ID 4701:0290`.

## Usage

Run directly to get a status readout and spectrum dump:

```bash
python capemca.py
```

Or import into another script:

```python
from capemca import CapeMCA

with CapeMCA() as mca:
    status = mca.read_status()
    print(f"Count rate: {status.cps} cps")

    spectrum = mca.read_spectrum()
```
