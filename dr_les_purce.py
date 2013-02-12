from botinator import *
import random, time

# Les Purce chat bot for great good.

# here is newjam's TESC class creation grammar, combined with new elements from this program
JAMES = "<title>:=<zzz> : <zzz>|<zzz>\n" + \
"<c>:=<adj> <noun>|<noun>\n" + \
"<xxx>:=<adj> <noun>|<c> and <c>|<c> <prep> <c>|<c> and <c>  <prep> <c>\n" + \
"<yyy>:=<vbing> <c>|<adj> <noun>\n" + \
"<zzz>:=<xxx>|<yyy>\n" + \
"<prep>:=to|from|of|in|toward\n" + \
"<noun>:=Alternatives|Foundations|Representations|Narratives|Crafts|Biodiversity|Knowledge|Abjection|Art|Time|Argentina|Plants|People|Ecoliteracy|Change|Mausoleum|Systems|Equality Speech|Male Privelege|Gender-Power|Freewriting|Media Studies|Studies|Afro-Brazilian Dance|Approaches to Healing|Ballet|Art/Work|Foundations of Change|Form|Function|Dance Creations|Power Dynamics|Heteronormativity|Inverted Sexuality|Sexuality|Polyamory|Freestyle Deforestation\n" + \
"<vbing>:=Drawing|Defending|Writing|Rewriting|Interogating|Looking|Re-Interpretting|Engaging|Exploring\n" + \
"<adj>:=Real|Literary|Imagined|Cultural|Evolutionary|Social|Forbidden|Sustainable|Emergent|Dynamic|Interdisciplinary|Growing|Sustainable|Gothic|An Introduction To|Non-postmodern\n"

# here are two functions I added to do class title generation --boomzilla
def parse_grammar(grammar):
    #this function converts the grammar string
    #into a dictionary, with the rules as keys,
    #returns the dictionary
    lines = grammar.splitlines()
    grammar_dict = {}
    for line in lines:
        line_split = line.split(":=")
        grammar_dict[line_split[0]] = line_split[1].split("|")
    return grammar_dict

def generate_sentence(grammar_dict, rule):
    #this function returns a randomly generated
    #string based on the passed grammar
    g_list = grammar_dict.get(rule)
    g_string = random.choice(g_list)
    to_return = ""
    sub_list = g_string.split()
    for rule in sub_list:
            if (rule[0] == "<"):
                to_return += generate_sentence(grammar_dict, rule)
            else:
                to_return += rule + " "
    return to_return

def generate_evergreen_class(matches, messenger):
	# todo: add more formats than just 'from adj noun towards adj noun' (adj noun and adj noun, adj noun based on adj noun, adj noun, etc)

	intros = ["Check out our new program: ", "Why don't you enroll in this upcoming program: ", "Your question will be answered in this program: ", "You can explore this further in this program: "]

	intro = random.choice(intros)
	grammar_dict = parse_grammar(JAMES)
	rule = "<title>"
	title = (generate_sentence(grammar_dict, rule))
	return intro + title


def random_response(matches, messenger):
	return random.choice([generate_evergreen_class(matches,messenger), insulted(matches,messenger), generic(matches,messenger)])

def generic(matches, messenger):
	return random.choice(["Let's all hold hands in red square.","You are the future.", "I have my own secret cave in the evergreen woods.", "I am immortal."])

def insulted(matches, messenger):
	return random.choice(["Talk to my mustache.","Let me console you with my guitar.","Check your pie plate. Did you grease it?","Talk to my secretary.","Art Constantino will handle this.", "Better grease yo pie plate", "You need more interdisciplinary education"])

def is_420():
	return time.strftime("%H%M") == "1620"

bot = Bot('irc.freenode.net',6667,'DrLesPurce_test','les','Dr Les Purce (bot)')
bot.join('#jayparty')
bot.bind('DrLesPurce_test:.*fuck(ing)?|shit|dammit|damn|stupid|dumb|lame.*', insulted)
bot.bind('DrLesPurce_test: .*\?', generate_evergreen_class) # When asked a question, suggest to join a program
bot.bind('DrLesPurce_test: .*', random_response)
bot.when(is_420, "420")

bot.live()
