#!/bin/bash

ipAddress1=$1
ipAddress2=$2

/usr/bin/expect <<EOF
set timeout 10
spawn ssh root@$ipAddress1
expect "Password: "
send "!root01\r"
expect -re "\\$ $"
send "ping $ipAddress2 -c 2\r"
expect EOF
