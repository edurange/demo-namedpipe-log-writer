#!/bin/bash
#
# A turnkey example of running the producer/consumer scripts
#
# Author: Joe Granville
# Date: 20250526
# License: MIT
# Version: 0.1.0
# Email: jwgranville@gmail.com
# Status: Proof-of-concept

fifopath=./fifo_$(date +%s)

mkfifo $fifopath

./toy_log_producer.py $fifopath & ./toy_log_consumer.py $fifopath

wait

rm $fifopath