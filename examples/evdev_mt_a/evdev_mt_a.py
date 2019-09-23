#!/usr/bin/python3

import sys
import time
import logging
import argparse
from evdev import UInput, ecodes


from capacitive_electrodes.predefined import electrodes_by_hardware_version


LOGGING_LEVEL = logging.INFO
LOGGING_FORMATS = {
    'format': '%(asctime)s %(name)s %(levelname)s: %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
}


class App(object):
    _logger = logging.getLogger('evdev_mt_a')

    def __init__(self, hardware_version):
        logging.basicConfig(level=LOGGING_LEVEL, **LOGGING_FORMATS)
        self.electrodes = electrodes_by_hardware_version(hardware_version)
        self.electrodes.init()

        ev_multitouch = {
            ecodes.EV_ABS: [
                (ecodes.ABS_MT_POSITION_X, (0, 0, self.electrodes.grid_sizes[0])),
                (ecodes.ABS_MT_POSITION_Y, (0, 0, self.electrodes.grid_sizes[1])),
            ]
        }
        self.ui_multitouch = UInput(ev_multitouch, name='capacitive_electrodes', version=0x3)

    def __loop__(self):
        self._logger.info('loop')
        while True:
            self.electrodes.update()

            if self.electrodes.get_newly_touched() or self.electrodes.get_newly_released():
                touched = self.electrodes.get_touched()
                for i in touched:
                    self.ui_multitouch.write(ecodes.EV_ABS, ecodes.ABS_MT_POSITION_X, i.grid_indexes[0])
                    self.ui_multitouch.write(ecodes.EV_ABS, ecodes.ABS_MT_POSITION_Y, i.grid_indexes[1])
                    self.ui_multitouch.write(ecodes.EV_SYN, ecodes.SYN_MT_REPORT, 0)
                if not touched:
                    self.ui_multitouch.write(ecodes.EV_SYN, ecodes.SYN_MT_REPORT, 0)
                self._logger.info('send multitouch_a[%d] report', len(touched))
                self.ui_multitouch.syn()

            time.sleep(0.01)

    def __exit__(self):
        self.ui_multitouch.close()


def main():
    _parser = argparse.ArgumentParser(
        description='Test Electrodes',
        add_help=False)
    _parser.add_argument(
        '--hardware_version',
        metavar='<hardware version number>',
        dest='hardware_version',
        type=int,
        default=0,
        help='the hardware version')
    _args, _ = _parser.parse_known_args()
    app = App(**dict(_args._get_kwargs()))
    app.__loop__()


if __name__ == '__main__':
    main()
