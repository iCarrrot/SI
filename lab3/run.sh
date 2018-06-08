#!/bin/bash

# Katalog w ktorym jest plik run.sh
export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Uwaga na:
# 1. polecenie exec - zastepujepy pythonem basha
# 2. opcje -u - wylaczamy buforowanie we/wy - pomoze nam przy zapomnianych stdout.flush
exec /usr/bin/python2 -u $DIR/read.py $DIR && $DIR/z1i2 && /usr/bin/python2 -u $DIR/write.py