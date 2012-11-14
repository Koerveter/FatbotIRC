import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import ConfigParser
import random

class GuessnumberManager():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.read_config()
		self.games = {}
		
	def prase_privmsg(self, event):
		source = event.source
		nick = source.split("!")[0]
		channel = event.channel
		message = event.message
		
		if self.games.has_key(source):
			self.games[source].process(event.message.split(":")[1], channel, nick)
			return
		
		if message.find(" ") == -1:  # If no parameters, discard
			return
		command = message.split(" ")
		parameters = command[1:]
		command = command[0].split(":")[1].lower()  # Get rid of the : at start and no caps
		
		if command == "guessnumber" and parameters[0] == "start":
			if len(parameters) < 3:  # not enough parameters, output help
				self.evManager.post(SendPrivmsgEvent(nick, nick + ": Syntax error. Syntax for starting a game of guessnumber is \"guessnumber start min max\" where min is the minimum value and max is the maximum value."))
				return
			try:
				min = int(parameters[1])
				max = int(parameters[2])
			except ValueError:
				self.evManager.post(SendPrivmsgEvent(nick, nick + ": Syntax error. Syntax for starting a game of guessnumber is \"guessnumber start min max\" where min is the minimum value and max is the maximum value."))
				
			self.games[source] = Guessnumber(min, max, self.evManager)
			self.evManager.post(SendPrivmsgEvent(nick, "Starting game of guessnumber with " + nick + " between values " + parameters[1] + " and " + parameters[2]))
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.prase_privmsg(event)
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "guessnumber" or event.module == "all":
				self.read_config()
		elif isinstance(event, TickEvent):
			self.check_instances()
			
			
	def check_instances(self):
		items = []
		for source, game in self.games.iteritems():
			if game.state == Guessnumber.STATE_STOPPED:
				items.append(source)
				
		for item in items:
			del self.games[item]
			
	def read_config(self):
		pass
		
		
class Guessnumber():
	STATE_STOPPED = 'stopped'
	STATE_RUNNING = 'running'
	def __init__(self, min, max, evManager):
		self.evManager = evManager
		self.state = Guessnumber.STATE_RUNNING
		self.number = random.randint(min, max)
		print self.number
		
	def process(self, message, channel, nick):
		try:
			print message
			value = int(message)
		except ValueError:
			self.evManager.post(SendPrivmsgEvent(nick, "Please enter a number."))
			return
		if value == self.number:  # game won
			self.evManager.post(SendPrivmsgEvent(nick, "Congratulations " + nick + " you have guessed the right number and therefore won the game!"))
			self.state = Guessnumber.STATE_STOPPED
		elif value > self.number:  # need to guess lower
			self.evManager.post(SendPrivmsgEvent(nick, nick + ": The number I'm looking for is lower."))
		elif value < self.number:  # need to guess higher
			self.evManager.post(SendPrivmsgEvent(nick, nick + ": The number I'm looking for is higher."))
			
			
			