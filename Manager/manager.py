import subprocess
import sys

class manager(object):
	def updateall(self):
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])
