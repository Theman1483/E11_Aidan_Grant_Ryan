# CapeMCA Usage Guide

## Device Behavior

The MCA begins acquiring data as soon as it is powered on. The spectrum
histogram accumulates counts continuously, independent of whether a USB host
is connected. Reading the spectrum is non-destructive — it returns a snapshot
of the current accumulated data without clearing it.

The two known commands are:

| Command      | Response         | Description                          |
|--------------|------------------|--------------------------------------|
| `{0, 0}`     | 64 bytes         | Status packet (count rate, timing, device info) |
| `{0, 16}`    | 16,384 bytes     | Full 4096-channel energy spectrum    |

There may be additional firmware commands (clear, start/stop, configuration)
not documented in the provided example code.

## Basic Usage

Read the current device status and accumulated spectrum:

```python
from capemca import CapeMCA

with CapeMCA() as mca:
    status = mca.read_status()
    print(f"Count rate: {status.cps} cps")
    print(f"Total counts: {status.total_count}")

    spectrum = mca.read_spectrum()
```

## Interval-Based Acquisition

Because the spectrum accumulates from power-on and a read does not clear it,
interval-based measurements should be computed by differencing successive reads.
Take a baseline spectrum at the start of acquisition, then subtract the previous
read from each new read to isolate the counts collected during that interval.

This differencing logic belongs in your DAQ/application layer rather than in
the driver module, since `capemca.py` is a hardware interface that returns raw
device data. Other tools in a multi-sensor ecosystem may not need differencing.

```python
import time
from capemca import CapeMCA

INTERVAL_S = 5

with CapeMCA() as mca:
    previous = mca.read_spectrum()

    while True:
        time.sleep(INTERVAL_S)
        current = mca.read_spectrum()
        interval = [c - p for c, p in zip(current, previous)]
        previous = current

        # interval now holds only the counts from the last INTERVAL_S seconds
        total = sum(interval)
        print(f"Counts in last {INTERVAL_S}s: {total}")
```

## Multiple Devices

To work with more than one MCA connected simultaneously:

```python
from capemca import CapeMCA, find_all_mcas

devices = find_all_mcas()
print(f"Found {len(devices)} MCA(s)")

for dev in devices:
    mca = CapeMCA(device=dev)
    mca.connect()
    status = mca.read_status()
    print(f"Device {status.capemca_id}: {status.cps} cps")
    mca.close()
```
