#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
from os import system; system('clear')
from collections import Counter
from random import choice
from math import ceil
import re

#Read in all the allowed words
with open("wordList.txt") as wordFile:
    possibleWords = [word.strip().lower() for word in wordFile]

#Generate the board
opponent = input("Opponent name: ")
wordLen = int(input("How long is the word: "))
word = ["?" for _ in range(wordLen)]

#Remove all possibleWords which are longer than the word
possibleWords = [i for i in possibleWords if len(i)<=wordLen]

#You can only have 5 blanks, so the word must be longer than (no. cards - 5)
possibleWords = [i for i in possibleWords if len(i)>=wordLen-5]

totalPossibleWords = len(possibleWords)
correctLetters, incorrectLetters = [], []
guessedLetters, suggestedLetter = [], "e"

count = 0

#While it is not totally guessed
while "?" in word and len(possibleWords) != 1:
    #Print the HUD
    system('clear')
    print("Opponent name: ", opponent)
    percentageLeft = str(round((100/totalPossibleWords)*len(possibleWords), 2))+"%"
    print("{} | ? | ? | {}".format(" ".join([str(x)[-1] for x in range(1,wordLen+1)]), percentageLeft))
    print("{} | {} | {}".format(" ".join(word), suggestedLetter, len(possibleWords)))
    if len(possibleWords) < 25:
        print(" ".join(possibleWords))
    else:
        print(" ".join(list(map(lambda _: choice(possibleWords), range(10)))))

    #Read in the guess, where it is/if it's right and validate it
    letter = str(input("Enter a letter to guess: "))
    while letter not in list("etaoinsrhdlucmfywgpbvkxqjz_"):
        letter = str(input("Invalid letter; please try again: "))
    guessedLetters.append(letter)

    #Enter and validate the position of the guessed letter
    position = input("Enter its position [1-n]: ")
    while True:
        try:
            position = int(position)
        except:
            position = None
            break
        if not 1 <= position <= wordLen:
            position = None
        if word[position-1] == "?":
            break
        print(position)
        position = input("You've already guessed that position; please try again: ")

    #Logic for possibleWords and suggestedLetter
    if position != None: #If it's right
        #If the letter isn't a blank
        if letter != "_":
            #Update the word HUD, and add the letter to correctLetters
            word[position-1] = letter
            correctLetters.append(letter)

            #Regex pattern between 1st and last known letter, with wildcards as necessary, to match words
            startCrib = [i for i, x in enumerate(word) if x != "?"][0]
            endCrib = [i for i, x in enumerate(word) if x != "?"][-1]+1
            knownCrib = [x if x!="?" else "[a-z_]" for x in word[startCrib:endCrib]]
            pattern = re.compile("^[a-z_]{0,"+str(startCrib)+"}"+"".join(knownCrib)+"[a-z_]{0,"+str((len(word)-endCrib))+"}$")
            possibleWords = [x for x in possibleWords if bool(pattern.match(x))]

        #If the letter is a blank
        else:
            #Remove all words longer than the longest possible given the blank
            maxPosLength = max([position-1, wordLen-position])
            possibleWords = [x for x in possibleWords if len(x)<=maxPosLength]

    else: #If it's wrong
        incorrectLetters.append(letter)

        #Filter the words, so they don't contain the incorrect letter, but it must still be able to contain already correct letters
        newPossibleWords = []
        for iWord in possibleWords:
            valid = True
            for iLetter in incorrectLetters:
                if iWord.count(iLetter) > correctLetters.count(iLetter):
                    valid = False
            if valid:
                newPossibleWords.append(iWord)

        possibleWords = newPossibleWords[:]

    #Remove correctLetters from the filteredPossibleWords to stop reguessing letters
    filteredPossibleWords = []
    for nWord in possibleWords:
        for nLetter in correctLetters:
            #nWord = nWord.replace(nLetter, "", 1)
            nWord = nWord.replace(nLetter, "", correctLetters.count(nLetter))
        filteredPossibleWords.append(nWord)

    #Suggest the best next letter to guess
    d = dict(Counter("".join(filteredPossibleWords)))
    print(d, max(d, key=lambda i: d[i]))
    if len(filteredPossibleWords) <= 1:
        break
    #The optimum value is the value closest to half of the percentage left (binary search)
    optimumValue = round(len(possibleWords)/2)
    suggestedLetter = min(d, key=lambda i: abs(d[i]-optimumValue))
    #suggestedLetter2 = max(d, key=lambda i: d[i])

    #Print all the letters that have been guessed
    print(guessedLetters)
    count += 1

system('clear')
if len(possibleWords) == 1:
    print("Done in {} moves! The word was \"{}\"".format(count, possibleWords[0]))
else:
    print("Invalid word! Check for a spelling mistake or an undisclosed letter")
