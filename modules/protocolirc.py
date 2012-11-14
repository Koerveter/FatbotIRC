import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser

class protocolIRC():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.read_config()
		
	def prase_privmsg(self, event):
		source = event.source
		channel = event.channel
		message = event.message
		
		# :Kek!Keke@somekind.ofspecial.mask PRIVMSG Fatbot :Hey
		if message.find(" ") == -1 or source != self.master:  # If no parameters, discard
			return
		command = message.split(" ", 1)
		parameters = command[1]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "join":  # channel
			self.evManager.post(JoinEvent(parameters))
		elif command == "part":  # channel
			self.evManager.post(PartEvent(parameters))
		elif command == "send":  # destination, message
			parameters = parameters.split(" ", 1)
			self.evManager.post(SendPrivmsgEvent(parameters[0], parameters[1]))
		
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.prase_privmsg(event)
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.master = 		self.config.get("protocolirc", "master")
			