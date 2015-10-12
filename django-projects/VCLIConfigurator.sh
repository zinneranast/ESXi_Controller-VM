#!/bin/bash

vsCommand='vicfg-vswitch --config sessionConfig.cfg'

#set default value for a physical NIC
vmknic=vmnic0

#get a tenant name, a VM name and IP as a parameters
portGroup=$1
vmName=$2
serviceName=$3
ipAddr=$4

#get a virtual switch name
tenantSwitch=`esxcli -c sessionConfig.cfg network vswitch standard portgroup list | grep -w "$portGroup" | awk '{print $2}'`
if [ "$tenantSwitch" == "" ]; then
  echo "Error: The specified port group does not exist."
  exit 0
fi

#add an uplink adapter to a virtual switch
uplink=`vicfg-vswitch --config sessionConfig.cfg -l | grep "$tenantSwitch" | awk '{print $NF}'`
if [ `echo $uplink | grep -w "[0-9]\+"` ]; then
  $vsCommand -L $vmknic $tenantSwitch
fi

#check a free VLAN ID
esxcli -c sessionConfig.cfg network vswitch standard portgroup list | awk '{print $NF}' | sort -u -n | sed '1d' > vlanIds.list
i=1
while read line; do
  if [[ $line -ne $i && $line -ne 4095 ]]; then
    break
  else
    i=$(($i + 1))
  fi
done < vlanIds.list
rm vlanIds.list
if [ $i -eq 4096 ]; then
  echo "There are not available VLAN ID"
  exit 0
fi
vlanId=$i

#set a VLAN ID for a virtual switch
ifVlanIdSet=`$vsCommand -l | grep "$portGroup[[:blank:]]\+[0-9]\+" | awk '{print $2}'`
if [ $ifVlanIdSet -eq 0 ]; then
  echo "The VLAN ID $vlanId will be set for your port group. Continue? (y/n)"
  read answer
  while [ "$answer" != "n" ]; do
    if [ "$answer" == "y" ]; then
      $vsCommand -v $vlanId --pg $portGroup $tenantSwitch
      break
    else
      read answer
    fi
  done
  if [ "$answer" == "n" ]; then
    echo "Enter the VLAN ID:"
    read vlanId
    ifVlanIdExists = `esxcli -c sessionConfig.cfg network vswitch standard portgroup list | awk '{print $NF}' | sort -u -n | grep -o -w "$vlanId"`
    while [[ "$ifVlanIdExists" == "$vlanId" || $vlanId -gt 4094 ]]; do
      echo "You cannot use this VLAN ID. Please enter another:"
      read vlanId
      ifVlanIdExists=`esxcli -c sessionConfig.cfg network vswitch standard portgroup list | awk '{print $NF}' | sort -u -n | grep -o -w "$vlanId"`
    done
    $vsCommand -v $vlanId --pg $portGroup $tenantSwitch
  fi
else
  vlanId=$ifVlanIdSet
fi

#connect to 'Converter' with SSH
/usr/bin/expect <<EOF
set timeout 10
spawn ssh root@192.168.1.198
expect "Password: "
send "!root01\r"
expect -re "\\$ $"
send "sudo /home/client1/converterConfigurator.sh $vlanId\r"
expect -re "\\$ $"
send "exit\r"

#connect to 'NAS-server' with SSH
spawn ssh root@192.168.1.199
expect "Password: "
send "!root01\r"
expect -re "\\$ $"
send "sudo /home/vmB/serverConfigurator.sh $ipAddr $vlanId $vmName$serviceName\r"
expect EOF
