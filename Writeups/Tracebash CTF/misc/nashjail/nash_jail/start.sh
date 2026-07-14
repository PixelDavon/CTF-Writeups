#!/bin/bash

exec socat \
TCP-LISTEN:1337,reuseaddr,fork \
EXEC:"timeout 600 /home/Shinobi/jail.sh",pty,stderr