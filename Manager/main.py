import sys
import manager
import paramiko, getpass, re, time
import configparser
import time
from tkinter import *
import os

mgr = manager.manager()
mgr.updateall()

config = configparser.ConfigParser()
config.sections()
config.read('manager.conf')

from paramiko import SSHClient

host = config['host.info']['hostname']
print('Logging into:', host)
local_hostname = config['host.info']['local_host']
print('Local hostmame:', local_hostname)
username = config['host.info']['username']
print('As user:', username)
password = config['host.info']['passwd']
sudo_pswd = config['host.info']['sudo_pswd']

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=str(password))

compWindow = 0

root = Tk()

def serviceOptions():
	def sRestart():
		servce = input('\nservice name: ')
		stdin, stdout, stderr = client.exec_command('service restart' + ' ' + servce)
		print('Restarted', servce)
	def sStart():
		servce = input('\nservice name: ')
		stdin, stdout, stderr = client.exec_command('service restart' + ' ' + servce)
		print('Started', servce)
	def sStop():
		print('Stoped', servce)
		servce = input('\nservice name: ')
		stdin, stdout, stderr = client.exec_command('service restart' + ' ' + servce)
		print('Started', servce)

	window = Tk()
	restart = Button(window, text="restart", command=sRestart)
	restart.grid(row=1, column=0)

	start = Button(window, text="start", command=sStart)
	start.grid(row=1, column=1)

	stop = Button(window, text="stop", command=sStop)
	stop.grid(row=1, column=2)

	window.mainloop()

serviceOpt = Button(root, text="Service", command=serviceOptions)
serviceOpt.grid(row=1, column=0)

def vncServer():
	vncs = Tk()
	def start():
		stdin, stdout, stderr = client.exec_command('vncserver')
	def stop():
		vnc1 = Tk()
		def shut():
			server = local_hostname + ':' + str(serverNum.get())
			stdin, stdout, stderr = client.exec_command('vncserver -kill ' + server)

		serverNum = Entry(vnc1, width=10)
		serverNum.grid(row=0, column=0)
		sendCmd = Button(vnc1, text='Stop', command=shut)
		sendCmd.grid(row=1, column=1)

	startVNC = Button(vncs, text='Start', command=start)
	startVNC.grid(row=1, column=0)
	stopVNC = Button(vncs, text='Stop', command=stop)
	stopVNC.grid(row=1, column=1)

vServer = Button(root, text='VNC Server', command=vncServer)
vServer.grid(row=3, column=0)

def power():
	pwr = Tk()
	def off():
		if int(tts.get()) == 0:
			stdin, stdout, stderr = client.exec_command('sudo shutdown now')
			stdin.write(sudo_pswd + "\n")
		else:
			stdin, stdout, stderr = client.exec_command('sudo shutdown +' + int(tts.get()))
			stdin.write(sudo_pswd + "\n")
	def restart():
		if int(tts.get()) == 0:
			stdin, stdout, stderr = client.exec_command('sudo shutdown -r now')
			stdin.write(sudo_pswd + "\n")
		else:
			stdin, stdout, stderr = client.exec_command('sudo shutdown +' + int(tts.get()))
			stdin.write(sudo_pswd + "\n")

	tts = Entry(pwr, width=25)
	tts.grid(row=0, column=0)
	off = Button(pwr, text='Off', command=off)
	off.grid(row=1, column=9)
	rest = Button(pwr, text='Restart', command=restart)
	rest.grid(row=1, column=10)

powerCmd = Button(root, text='Power', command=power)
powerCmd.grid(row=4, column=0)

def runCommand():
	ecomd = Tk()
	cmd = Entry(ecomd, width=50)
	cmd.grid(row=1, column=1)
	def excmd(event):
		stdin, stdout, stderr = client.exec_command(str(cmd.get()))
		ecomd.destroy()

	sCmdButton = Button(ecomd, text="Send Command", command=excmd)
	sCmdButton.grid(row=2, column=10)
	ecomd.bind('<Return>', excmd)

	ecomd.mainloop()

runCmd = Button(root, text='Command', command=runCommand)
runCmd.grid(row=20, column=0)

def rootCmd():
	rcmd = Tk()
	rootcommand = Entry(rcmd, width=50)
	rootcommand.grid(row=1, column=1)
	def sendCommand(event):
		stdin, stdout, stderr = client.exec_command('sudo' + ' ' + str(rootcommand.get()))
		stdin.write(sudo_pswd + "\n")
		rcmd.destroy()

	sCmdButton = Button(rcmd, text="Send Command", command=sendCommand)
	sCmdButton.grid(row=2, column=10)
	rcmd.bind('<Return>', sendCommand)

	rcmd.mainloop()

close_button = Button(root, text='Sudo', command=rootCmd)
close_button.grid(row=21, column=0)

root.mainloop()

