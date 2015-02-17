# Send Weather by Ferran Fabregas ferri.fc@gmail.com
import random, math
import Image, sys
import time
import re
from twython import Twython
from twython import TwythonStreamer
import subprocess

# Eliza setup
responseStarts = []
responseCurrentIndices = []
responseEnds = []
previousInput = ""
userInput = ""
CONVERSATION_KEYWORDS = ["CAN YOU", "CAN I", "YOU ARE", "YOURE", "I DONT", "I FEEL", "WHY DONT YOU", "WHY CANT I","ARE YOU", "I CANT", "I AM", " IM ", "YOU", "I WANT", "WHAT", "HOW", "WHO", "WHERE","WHEN", "WHY", "NAME", "CAUSE", "SORRY", "DREAM", "HELLO", "HI", "MAYBE", "NO", "YOUR","ALWAYS", "THINK", "ALIKE", "YES", "FRIEND", "COMPUTER", "NOKEYFOUND"]
WORDS_TO_REPLACE = ["ARE","AM","WERE","WAS","YOU","I","YOUR","MY","IVE","YOUVE","IM","YOURE", "YOU", "ME"]
QUESTIONS = [
            "DON'T YOU BELIEVE THAT I CAN.", "PERHAPS YOU WOULD LIKE TO BE ABLE TO.",
            "YOU WANT ME TO BE ABLE TO*", "PERHAPS YOU DON'T WANT TO*",
            "DO YOU WANT TO BE ABLE TO*", "WHAT MAKES YOU THINK I AM*",
            "DOES IT PLEASE YOU TO BELIEVE I AM*", "PERHAPS YOU WOULD LIKE TO BE*",
            "DO YOU SOMETIMES WISH YOU WERE*", "DON'T YOU REALLY*", "WHY DON'T YOU*",
            "DO YOU WISH TO BE ABLE TO*", "DOES THAT TROUBLE YOU?",
            "TELL ME MORE ABOUT SUCH FEELINGS*", "DO YOU OFTEN FEEL*",
            "DO YOU ENJOY FEELING*", "DO YOU REALLY BELIEVE I DON'T*",
            "PERHAPS IN TIME I WILL*", "DO YOU WANT ME TO*",
            "DO YOU THINK YOU SHOULD BE ABLE TO*", "WHY CAN'T YOU*",
            "WHAT MAKES YOU WONDER WHETHER OR NOT I AM*",
            "WOULD YOU PREFER IF I WERE NOT*", "PERHAPS IN YOUR FANTASIES I AM*",
            "HOW DO YOU KNOW YOU CAN'T*", "HAVE YOU TRIED?", "PERHAPS YOU CAN NOW*",
            "DID YOU COME TO ME BECAUSE YOU ARE*", "HOW LONG HAVE YOU BEEN*",
            "DO YOU BELIEVE IT IS NORMAL TO BE*", "DO YOU ENJOY BEING*",
            "I AM MORE INTERESTED IN TALKING ABOUT YOU.", "OH, I*",
            "ARE YOU REALLY SO INTERESTED IN SOMEONE LIKE ME?",
            "WHAT WOULD IT MEAN TO YOU IF YOU GOT*", "WHY DO YOU WANT*",
            "SUPPOSE YOU SOON GOT*", "WHAT IF YOU NEVER GOT*", "I SOMETIMES ALSO WANT*",
            "WHY DO YOU ASK?", "DOES THAT QUESTION INTEREST YOU?",
            "WHAT ANSWER WOULD PLEASE YOU THE MOST?", "WHAT DO YOU THINK?",
            "ARE SUCH QUESTIONS ON YOUR MIND OFTEN?",
            "WHAT IS IT THAT YOU REALLY WANT TO KNOW?", "HAVE YOU ASKED ANYONE ELSE?",
            "HAVE YOU ASKED SUCH QUESTIONS BEFORE?",
            "WHAT ELSE COMES TO MIND WHEN YOU ASK THAT?", "WE CAN KEEP THIS ANONYMOUS.",
            "NO NEED TO SPECIFY ANY NAMES-- PLEASE GO ON.", "IS THAT THE REAL REASON?",
            "DON'T ANY OTHER REASONS COME TO MIND?",
            "DOES THAT REASON EXPLAIN ANYTHING ELSE?", "WHAT OTHER REASONS MIGHT THERE BE?",
            "PLEASE DON'T APOLOGIZE.", "APOLOGIES ARE NOT NECESSARY.",
            "WHAT FEELINGS DO YOU HAVE WHEN YOU APOLOGIZE?", "NO NEED TO BE DEFENSIVE!",
            "WHAT DOES THAT DREAM SUGGEST TO YOU?", "DO YOU DREAM OFTEN?",
            "WHAT PERSONS APPEAR IN YOUR DREAMS?", "DO YOU HAVE PLEASANT DREAMS?",
            "HOW DO YOU DO ... PLEASE STATE YOUR PROBLEM.", "YOU DON'T SEEM QUITE CERTAIN.",
            "WHY THE UNCERTAIN TONE?", "LET'S TRY TO KEEP THIS POSITIVE.", "YOU AREN'T SURE?",
            "DON'T YOU KNOW?", "IS THAT A DEFINITE NO OR MIGHT YOU CHANGE YOUR MIND?",
            "I AM SENSING SOME NEGATIVITY.", "WHY NOT?", "ARE YOU SURE?", "WHY NO?",
            "WHY ARE YOU CONCERNED ABOUT MY*", "WHAT ABOUT YOUR OWN*",
            "CAN'T YOU THINK OF A SPECIFIC EXAMPLE?", "WHEN?", "WHAT ARE YOU THINKING OF?",
            "REALLY. ALWAYS?", "DO YOU REALLY THINK SO?", "BUT YOU ARE NOT SURE YOU.",
            "BELIEVE IN YOURSELF.", "IN WHAT WAY?", "WHAT RESEMBLANCE DO YOU SEE?",
            "WHAT DOES THE SIMILARITY SUGGEST TO YOU?",
            "WHAT OTHER CONNECTIONS DO YOU SEE?", "COULD THERE REALLY BE SOME CONNECTION?",
            "HOW?", "YOU SEEM QUITE POSITIVE.", "ARE YOU SURE?", "I SEE.", "I UNDERSTAND.",
            "TELL ME ABOUT YOUR FRIENDS.", "ARE YOU WORRIED ABOUT YOUR FRIENDS?",
            "DO YOUR FRIENDS EVER GIVE YOU A HARD TIME?", "WHAT DO YOU LIKE ABOUT YOUR FRIENDS?",
            "DO YOU LOVE YOUR FRIENDS?", "PERHAPS YOUR LOVE FOR FRIENDS WORRIES YOU.",
            "DO COMPUTERS EXCITE YOU?", "ARE YOU TALKING ABOUT ME IN PARTICULAR?",
            "HOW DO YOU LIKE YOUR WATCH?", "WHY DO YOU MENTION COMPUTERS?",
            "DO YOU FIND MACHINES AS FASCINATING AS I DO?",
            "DON'T YOU THINK COMPUTERS CAN HELP PEOPLE?",
            "WHAT ABOUT MACHINES EXCITES YOU THE MOST?",
            "HEY THERE, HOW CAN I HELP YOU?",
            "WHAT DOES THAT SUGGEST TO YOU?", "I SEE.",
            "I'M NOT SURE I UNDERSTAND YOU FULLY.", "COME COME ELUCIDATE YOUR THOUGHTS.",
            "CAN YOU ELABORATE ON THAT?", "THAT IS QUITE INTERESTING."]
# pairs of numbers (start of reply string, number of reply strings)
CONVERSATION_TO_RESPONSES_MAP = [
            1,3,4,2,6,4,6,4,10,4,14,3,17,3,20,2,22,3,25,3,
            28,4,28,4,32,3,35,5,40,9,40,9,40,9,40,9,40,9,40,9,
            49,2,51,4,55,4,59,4,63,1,63,1,64,5,69,5,74,2,76,4,
            80,3,83,7,90,3,93,6,99,7,106,6]
# response arrays init
for i in xrange(0,len(CONVERSATION_TO_RESPONSES_MAP)/2):
    responseStarts.append(CONVERSATION_TO_RESPONSES_MAP[2 * i]) # start of reply string
    responseCurrentIndices.append(CONVERSATION_TO_RESPONSES_MAP[2 * i]) # start at first position
    responseEnds.append(responseStarts[i] + CONVERSATION_TO_RESPONSES_MAP[2 * i  + 1]) # number of reply strings

def elizabot(inputText):
    result = ""
    global previousInput
    inputText = " " + inputText.upper().replace("'", "") + " " # reformat inputText, remove the '
    if previousInput != " " and inputText == previousInput: # repeat the last sentence?
        return "DIDN'T YOU JUST SAY THAT?"
    previousInput = inputText
    # search keywords on inputText
    keywordIndex = 0
	while keywordIndex < len(CONVERSATION_KEYWORDS):
        index=inputText.find(CONVERSATION_KEYWORDS[keywordIndex])
        if index != -1:
            break
        keywordIndex=keywordIndex+1
    afterKeyword = ""
	# now, keywordIndex has the first keyword found in inputText, 36 if not any
    if keywordIndex == len(CONVERSATION_KEYWORDS):
        keywordIndex = 35 # 36 -> 35
    else:
		index=inputText.find(CONVERSATION_KEYWORDS[keywordIndex])
        afterKeyword = inputText[index+len(CONVERSATION_KEYWORDS[keywordIndex]):] # get the input text after the keyword
        parts = re.split("\s+", afterKeyword) # afterKeyword is splited by word
        for i in xrange (0,len(WORDS_TO_REPLACE)/2): # go through the list of words to replace
            first = WORDS_TO_REPLACE[i * 2]  # original word
            second = WORDS_TO_REPLACE[i * 2 + 1] # replaced by...
            for j in xrange (0,len(parts)): # replacing all the tenses words found on inputText parts
                if parts[j]==first:
                    parts[j]= second
                else:
                    if parts[j]==second:
                        parts[j]=first
        afterKeyword = str.join(" ",parts) # join string again
	question = QUESTIONS[responseCurrentIndices[keywordIndex] - 1] # map the expresion used by the user with a proper answer/question sequence
    responseCurrentIndices[keywordIndex] = responseCurrentIndices[keywordIndex] + 1; # change the content of responseCurrentIndices, >> right
    if responseCurrentIndices[keywordIndex] > responseEnds[keywordIndex]: # if the sequence ends...
        responseCurrentIndices[keywordIndex] = responseStarts[keywordIndex] # ... start again
    result = result + question
	if result.endswith("*"): # if question ends with a *, uses the inputText as part of the response
            result = result[:-1]
            result = result + " " + afterKeyword;
    return result


# Setup callbacks from Twython Streamer
class TwitterController(TwythonStreamer):
        def on_success(self, data):
		#print data
                if 'text' in data:
                        twitterString=data['text'].encode('utf-8')
						stringParts=twitterString.split(' ')                        
						print twitterString
						userInput=twitterString.replace("@Iamachatterbot","")
						wdata="@"+data['user']['screen_name'].encode('utf-8')+" "+elizabot(userInput).encode('utf-8')
						twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
						twitter.update_status(status=wdata)
						#print wdata

# Your twitter ID
TERMS = '@Iamachatterbot'


# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

print "LISTENING TWITTER....."
# Create streamer

try:
	stream = TwitterController(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	print "Bye Bye! :)"