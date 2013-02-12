from botinator import *
import random, time

# Les Purce chat bot for great good.

def generate_evergreen_class(matches, messenger):
	# todo: add more formats than just 'from adj noun towards adj noun' (adj noun and adj noun, adj noun based on adj noun, adj noun, etc)

	intros = ["Check out our new program: ", "Why don't you enroll in this upcoming program: ", "Your question will be answered in this program: ", "You can explore this further in this program: "]

	adjectives = ['Emergent', 'Dynamic', 'Interdisciplinary', 'Growing', 'Sustainable', 'Engaging','Gothic', 'An Introduction To', 'Non-postmodern', 'Exploring']

	nouns = ['Systems', 'Equality Speech', 'Male Privelege', 'Gender-Power','Freewriting','Media Studies','Afro-Brazilian Dance','Approaches to Healing', 'Ballet', 'Art/Work', 'Foundations of Change', 'Form and Function', 'Dance Creations', 'Power Dynamics', 'Heteronormativity', 'Inverted Sexuality', 'Polyamory', 'Freestyle Deforestation']

	intro = random.choice(intros)
	n1 = random.choice(nouns)
	nouns.remove(n1)
	n2 = random.choice(nouns)
	a1 = random.choice(adjectives)
	adjectives.remove(a1)
	a2 = random.choice(adjectives)
	return intro + 'From ' + a1 + ' ' + n1 + ' Towards ' + a2 + ' ' + n2


def random_response(matches, messenger):
	return random.choice([generate_evergreen_class(matches,messenger), insulted(matches,messenger), generic(matches,messenger)])

def generic(matches, messenger):
	return random.choice(["Let's all hold hands in red square.","You are the future.", "I have my own secret cave in the evergreen woods.", "I am immortal."])

def insulted(matches, messenger):
	return random.choice(["Talk to my mustache.","Let me console you with my guitar.","Check your pie plate. Did you grease it?","Talk to my secretary.","Art Constantino will handle this.", "Better grease yo pie plate", "You need more interdisciplinary education"])

def is_420():
	return time.strftime("%H%M") == "1620"

def wat(matches, messenger):
	return random.choice([insulted(None,None),get_evergreen_class(None,None)])
	

bot = Bot('irc.freenode.net',6667,'DrLesPurce_test','les','Dr Les Purce (bot)')
bot.join('#jayparty')
bot.bind('DrLesPurce_test:.*fuck(ing)?|shit|dammit|damn|stupid|dumb|lame.*', insulted)
bot.bind('DrLesPurce_test: .*\?', generate_evergreen_class) # When asked a question, suggest to join a program
bot.bind('DrLesPurce_test: .*', random_response)
bot.when(is_420, "420")

bot.live()
