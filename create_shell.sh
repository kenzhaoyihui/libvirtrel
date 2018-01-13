#!/bin/bash

echo "How many vms do you want to create?"

read number

for((i=2; i<=$number+1; i++)); do
	virsh destroy test$i	
	
	if [ -d "vm$i" ]; then
                rm -rf  vm$i/*
        else
                mkdir vm$i
        fi

	qemu-img create -f qcow2 vm$i/test$i.qcow2 2G && chmod 755 vm$i/test$i.qcow2
	cp /var/lib/libvirt/images/vm1/test1.xml vm$i/test$i.xml
	sed -i "s/test1/test$i/g" vm$i/test$i.xml
	sed -i "s/vm1/vm$i/g" vm$i/test$i.xml

	virsh define vm$i/test$i.xml
	virsh start test$i
done
