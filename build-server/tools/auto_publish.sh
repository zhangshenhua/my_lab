#/usr/bini/sh
export PATH=./tools:$PATH;
ssh_tunnel.py 10.239.131.220 root 123456 &
ssh_command.py 10.239.131.220 root 123456 "./vgt-get install all >> /tmp/vgt.log"


