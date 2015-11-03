#!/bin/bash

serviceName=$1
username=$2

#connect to 'NAS-server' with SSH
/usr/bin/expect <<EOF
set timeout 10
spawn ssh root@192.168.1.199
expect "Password: "
send "!root01\r"
expect -re "\\$ $"
send "sudo /home/vmB/srv-configs/findService.sh $serviceName $username\r"
expect EOF
