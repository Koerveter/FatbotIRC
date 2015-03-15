import os, sys
from core.events import TickEvent, RequestPongEvent, ReloadconfigEvent
import ConfigParser, time
from core.weakboundmethod import WeakBoundMethod as Wbm
from core.botinfo import read_config_section

class autopinger():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self.lastPing = time.time()
		self._connections = [
			self.ed.add(TickEvent, Wbm(self.ping)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config)),
			self.ed.add(RequestPongEvent, Wbm(self.reset))
		]

	def reset(self, event):
		self.lastPing = time.time()
		
	def ping(self, event):
		if time.time() - self.lastPing > self.timeout:
			#self.ed.post(PongEvent("trail and error..."))
			RequestPongEvent("trail and error...").post(self.ed)
			
	def reload_config(self, event):
		if event.module == "autopinger" or event.module == "all":
			self.read_config()
	
	def read_config(self):
		config = read_config_section(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'), "autopinger")
		#self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.timeout = config["timeout"] + 2
