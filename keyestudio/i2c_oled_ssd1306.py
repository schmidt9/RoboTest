# Copyright (c) 2014-2022 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil

Based on https://github.com/rm-hull/luma.examples/blob/main/examples/sys_info.py
"""

import os
import sys
import time
import signal
from datetime import datetime

if os.name != 'posix':
    sys.exit(f'{os.name} platform is not supported')

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas


try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


def handle_sigterm(signum, frame):
    device.hide() # power off before shudown bacause screen stays on
    os._exit(0) #force exit, avoids further signals


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return f"{n}B"


def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
        % (av1, av2, av3, str(uptime).split('.')[0])


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "Disk:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx %s, Rx %s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


def stats(device):
       with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), fill="white")
        if device.height >= 32:
            draw.text((0, 14), mem_usage(), fill="white")

        if device.height >= 64:
            draw.text((0, 26), disk_usage('/'), fill="white")
            try:
                draw.text((0, 38), network('wlan0'), fill="white")
            except KeyError:
                # no wifi enabled/available
                pass


def get_device():
    serial = i2c(port=2, address=0x3C)
    device = ssd1306(serial)
    return device


def main():
    while True:
        stats(device)
        time.sleep(5)


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGTERM, handle_sigterm)
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
