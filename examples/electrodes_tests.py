#!/usr/bin/python3

import sys
import time
import logging
import argparse

from capacitive_electrodes.predefined import electrodes_by_hardware_version


LOGGING_LEVEL = logging.INFO
LOGGING_FORMATS = {
    'format': '%(asctime)s %(name)s %(levelname)s: %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
}


class App(object):
    _logger = logging.getLogger('electrodes_test')

    def __init__(self, hardware_version):
        logging.basicConfig(level=LOGGING_LEVEL, **LOGGING_FORMATS)
        self.electrodes = electrodes_by_hardware_version(hardware_version)
        self.electrodes.init()

    def __loop__(self):
        self._logger.info('loop')
        while True:
            self.electrodes.update()
            # print newly touched electrodes
            for i in self.electrodes.get_newly_touched():
                self._logger.info('elec %s,\t%s', i.index, i.grid_indexes)
            time.sleep(0.01)


def main():
    _parser = argparse.ArgumentParser(
        description='Electrodes Test',
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
