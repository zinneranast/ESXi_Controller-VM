#!/bin/bash

serviceName=$1

#connect to 'NAS-server' with SSH
/usr/bin/expect <<EOF
set timeout 10
spawn ssh root@192.168.1.199
expect "Password: "
send "!root01\r"
expect -re "\\$ $"
send "sudo grep $serviceName /home/vmB/srv-configs/services.list\r"
expect -re "\\$ $"
expect EOF
