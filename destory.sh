#!/bin/bash

echo "How manny VMs do you want to destroy?"

read number

for((i=2; i<=$number+1; i++)); do
        #virsh destroy test$i
        #virsh undefine test$i
	rm -rf vm$i
done
