import socket, threading, datetime, re, sys

class Bot:
	def __init__(self, serv, port, nick, username, ircname):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((serv,port))
		self.irc.send('USER ' + ((username + ' ')*3) + ':' + ircname + '\r\n') 
		self.irc.send('NICK ' + nick + '\r\n')
		self.bindings = {}
		self.patterns = [] # store an ordered list of patterns.
		self.conditions = {}
		self.state = {}

	def join(self,chan):
		"Join a channel"
		self.chan = chan
		self.irc.send ('JOIN ' + chan + '\r\n')
		return self

	def bind(self,pattern,response):
		"Bind a matched regex to a response"
		self.patterns.append(pattern)
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
				r = response(*args)
				print('Dynamic response: ' + r)
				self.irc.send('PRIVMSG '+self.chan+' :'+r+'\n') # apply function to regex matches
			except:
				print('Reponse threw exception: ', sys.exc_info()[:2], 'line ' + str(sys.exc_info()[2]))
				return
		else:
			print('Static response: ' + response)
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
				message = None
				for p in self.patterns:
					matches = re.findall(p, data)
					if matches:
						print("\nFound match: " + str(p))
						self.respond(self.bindings[p],matches,None)
						break
			# Check conditions.
			# for condition, response in self.conditions.iteritems():
			#	if condition(): self.respond(response)
