import socket, threading, datetime, re, sys

class Bot:
	def __init__(self, serv, port, nick, username, ircname):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((serv,port))
		self.irc.send('USER ' + ((username + ' ')*3) + ':' + ircname + '\r\n') 
		self.irc.send('NICK ' + nick + '\r\n')
		self.bindings = {}
		self.conditions = {}
		self.state = {}

	def join(self,chan):
		"Join a channel"
		self.chan = chan
		self.irc.send ('JOIN ' + chan + '\r\n')
		return self

	def bind(self,pattern,response):
		"Bind a matched regex to a response"
		self.bindings[pattern] = response
		return self

	def when(self,condition,response):
		"Bind a predicate function to a response"
		self.conditions[condition] = response
		return self

	def __repr__(self): return "botbotbotbotbot"

	def pong(self): self.irc.send("PONG :pings\n")

	def respond(self,response,*args):
		"""
		Send a response, which may be a function returning a string or just a string
		Response function must have two parameters: list of regex matches and the
		messenger nick.
		"""
		if hasattr(response, '__call__'): # is function object?
			try:
				print('Responding: ' + response(*args))
				self.irc.send('PRIVMSG '+self.chan+' :'+response(*args)+'\n') # apply function to regex matches
			except:
				print('Reponse threw exception: ', sys.exc_info()[:2], 'line ' + str(sys.exc_info()[2].tb_lineno))
				return
		else:
			print('Responding: ' + response)
			self.irc.send('PRIVMSG '+self.chan+' :'+response+'\n') # just send string

	def live(self):
		"Main event loop. Run after everything else is configured. Ctrl-C to end."
		# How could someone modify the bot while it is looping this method to
		# dynamically play with its behavior?
		while True:
			data = self.irc.recv(4096)
			print(data)
			if data.find("PING :") != -1: self.irc.send("PONG :pings\n")
			# Respond to messages.
			elif data.find(' PRIVMSG ' + self.chan) != -1:
				for pattern, response in self.bindings.iteritems():
					matches = re.findall(pattern, data)
					if matches:
						print("Found match: " + str(pattern))
						self.respond(response,matches,'john')
			# Check conditions.
			for condition, response in self.conditions.iteritems():
				if condition(): self.respond(response)
