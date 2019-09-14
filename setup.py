#!/usr/bin/python3

from setuptools import setup, find_packages


setup(
    name='capacitive_electrodes',
    version='1.0.0',
    author='Arad Eizen',
    author_email='arad.rgb@gmail.com',
    description='MPR121 based capacitive electrodes driver',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['smbus2'],
)
