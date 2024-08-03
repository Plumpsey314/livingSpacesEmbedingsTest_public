"""
Author: Nathan Derhake.
"""


def splitToLowerWords(string, alphabet="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789’\"'"):
    rv = []
    curWord = ''
    for char in string:
        if(char in alphabet):
            curWord+=char
        elif(len(curWord) > 0):
            rv.append(curWord.lower())
            curWord = ''
    if(curWord != ''): rv.append(curWord.lower())
    return rv

wordsAndCounts = []
words = []
file = open('furnitureList.txt', 'r', encoding='utf8') # open file
fileString = file.read() # all of the furnaiture in one string
parsedItems = fileString.split('\n\n')
fileWords = splitToLowerWords(fileString, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789’\"'-")
for word in fileWords:
    # print(word + str(word in words))
    if(word in words):
        index = words.index(word)
        wordsAndCounts[index][1] += 1
        moreWork = index!=0
        curIndex = index
        while(moreWork):
            if(curIndex==0):
                moreWork = False
            if(wordsAndCounts[curIndex][1] > wordsAndCounts[curIndex-1][1]):
                # print(word)
                temp = wordsAndCounts[curIndex]
                tempWord = words[curIndex]
                words[curIndex] = words[curIndex-1]
                words[curIndex-1] = tempWord
                wordsAndCounts[curIndex] = wordsAndCounts[curIndex-1]
                wordsAndCounts[curIndex-1] = temp
                curIndex -= 1
            else: 
                moreWork = False
    else:
        words.append(word)
        wordsAndCounts.append([word, 1])
