#!/bin/bash
sudo apt install -y python3 python3-pip
sudo -H ./setup.py install
sudo gpasswd -a $USER input
