word="test" # set-up the word
wordarray=[]
resolvedwordarray=[]
remainingattempts=5
usedletters=[]
theend=False
for letter in word:
    wordarray.append('0')
    resolvedwordarray.append(letter)
inputletter='0'
while (inputletter<>'1' and theend==False):
    print "WORD:",
    for letter in wordarray:
        print letter,
    print
    print ("Remaining attempts: %i" % remainingattempts)
    inputletter=raw_input('Enter your letter (1 to exit):')
    if len(inputletter)!=1:
        print "Only one character!"
    else:
        if inputletter not in usedletters:
            usedletters.append(inputletter)
            if inputletter not in resolvedwordarray:
                remainingattempts=remainingattempts-1
            else:
                for i,letter in enumerate(resolvedwordarray):
                    if letter==inputletter:
                       wordarray[i]=inputletter
        else:
            print "Letter used yet!"
    # Check game status
    if remainingattempts==0:
        print "You lose!"
        theend=True
    if '0' not in wordarray:
        print "You win!"
        theend=True
print "Bye Bye!"


                

