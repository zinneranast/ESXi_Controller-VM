#!/bin/bash

#get a VM name and a service name as a parameters
serviceName=$1
vmName=$2

#connect to 'NAS-server' with SSH
/usr/bin/expect <<EOF
set timeout 10
spawn ssh root@192.168.1.199
expect "Password: "
send "!root01\r"
expect -re "\\$ $"
send "sudo /home/vmB/srv-configs/deleteServices.sh $serviceName $vmName\r"
expect -re "\\$ $"
expect EOF
