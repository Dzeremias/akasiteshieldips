#!/bin/bash

cd $(pwd)/akasiteshieldips/
/usr/bin/python3 $(pwd)/siteshield.py
sudo bash $(pwd)/create_siteshield.sh
sudo bash #(pwd)/saveiptables.sh
