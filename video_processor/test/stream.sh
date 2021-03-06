#!/bin/sh
ffmpeg \
    -re \
    -fflags +genpts \
    -stream_loop -1 \
    -i $1 \
    -preset ultrafast \
    -tune zerolatency \
    -b:v 10M \
    -f mpegts \
    udp://$2