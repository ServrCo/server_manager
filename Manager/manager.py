import subprocess
import sys

class update(object):
	def all(self):
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])