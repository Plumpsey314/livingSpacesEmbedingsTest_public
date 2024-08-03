"""
Author: Nathan Derhake. Influence taken from James Briggs, and Langchain documentation.
"""

from wordCounter import splitToLowerWords

file = open('furnitureList.txt', 'r', encoding='utf8') # open file
fileString = file.read() # all of the furnaiture in one string
parsedItems = fileString.split('\n\n')
furnitureTypes = ['furniture', 'seat', 'bed', 'chair', 'table', 'bookcase', 'chaise', 'recliner', 'sofa', 'cart', 'battery', 'nightstand', 'dresser', 'bench', 'ottoman', 'umbrella', 'desk', 'settee', 'sectional', 'rug', 'cover', 'lamp', 'stand', 'divider', 'stool', 'island', 'loveseat', 'cabinet', 'cuddler', 'sculpture', 'holder', 'chest', 'curio', 'shelf', 'vanity', 'set', 'rack', 'daybed', 'firepit', 'dining']
singletonTypes = ['cover', 'lamp', 'set']
furnitureSchema = [
    "furniture",
    ["bed", "bedroom set"],
    "cart",
    "divider",
    "firepit",
    "holder",
    "lamp",
    ["non furniture", "battery", "cover"],
    "rug",
    "sculpture",
    ["seat", ["bench", "bench set"], ["chair", "chair set", "chaise", "cuddler", "recliner", "stool"], "ottoman", ["sofa", "daybed", "living room set", ["loveseat", "loveseat set"], "sectional", "settee", "sofa set"]],
    ["shelf", "bookcase", ["cabinet", "curio"], "rack"],
    ["stand", "chest", "drawer", "dresser", ["nightstand", "nightstand set"], "sideboard"],
    ["table", "bar set", ["desk", ["vanity", "vanity set"]], ["dining", "dining set"], "island", "office set"],
    "umbrella"
]
itemTypeList = []
colorAlphabet = 'abcgmnoprtwy'
colorTypes = ['gray', 'black', 'brown', 'green', 'pink', 'blue', 'orange', 'purple', 'red', 'tan', 'white', 'yellow']
materialAlphabet = 'qwertyuiopasdfghjklzxcvbnm01'
materialTypes = ['resin', 'wood', 'concrete laminate', 'reclaimed wood', 'mdf', 'polyurethane', 'faux', 'plastic', 'composite', 'polyester', 'cane', 'polypropylene', 'multi-media', 'fabric', 'glass', 'chenille', 'fiber', 'wicker', 'leather', 'cotton', 'rattan', 'concrete', 'velvet', 'marble', 'veneer', 'metal', 'synthetic', 'wool']
styleAlphabet = 'abcfghimnoprtu'
styleTypes = ['coastal', 'boho', 'classic', 'farmhouse', 'glam', 'cottage', 'industrial', 'modern', 'mid-century modern', 'contemporary', 'french', 'rustic', 'traditional', 'casual']
sizeAlphabet = 'sml'
sizeTypes = ['small', 'medium', 'large']
keywordsAlphabet = 'fot'
keywordsTypes = ['fancy', 'outdoor', 'theater']

synonyms = [ 'synonyms', 
            ['sofa', 'couch'], 
            ['tan', 'cream', 'beige', 'ivory'], 
            ['blue', 'indigo', 'navy'], 
            ['pink', 'magenta'], 
            ['gray', 'grey'], 
            ['mid-century modern', 'mid-century-modern', 'mid century modern', 'mid century-modern'], 
            ['black', 'dark'], 
            ['white', 'light'],
            ['theater', 'theatre', 'movie'],
            ['small', 'tiny', 'cute', 'compact'],
            ['large', 'big', 'sizable', 'hefty', 'heavy'],
            ['bookcase', 'bookshelf'],
            ['shelf', 'shelves'],
            ['chair', 'armchair'],
            ['wood', 'wooden']]
setVersions =  ['set', 'office', 'bedroom', 'bar', ['room', 'living']]
setVersions.extend(furnitureTypes)
multilengthKeywords = [ 
    'multikeywords',
    setVersions,
    ['wood', 'reclaimed'],
    ['media', 'multi'],
    ['modern', ['century', 'mid'], 'mid-century'],
    ['century-modern', 'mid']
]

def appendItemsWithAlphabet(string, alphabet, types):
    rv = []
    for char in string:
        if(char in alphabet): rv.append(types[alphabet.index(char)])
    return rv

def getMetadataDetails():
    csv = open('colors.csv', 'r')
    csv.readline()
    colors = []
    materials = []
    styles = []
    sizes = []
    keywords = []
    curLine = csv.readline().split(',')
    while curLine != ['']:
        colors.append(appendItemsWithAlphabet(curLine[0], colorAlphabet, colorTypes))
        materials.append(appendItemsWithAlphabet(curLine[1], materialAlphabet, materialTypes))
        styles.append(appendItemsWithAlphabet(curLine[2], styleAlphabet, styleTypes))
        sizes.append(appendItemsWithAlphabet(curLine[3], sizeAlphabet, sizeTypes))
        keywords.append(appendItemsWithAlphabet(curLine[4], keywordsAlphabet, keywordsTypes))

        curLine = csv.readline().split(',')
    return {"colors": colors, "materials": materials, "styles": styles, "sizes": sizes, "keywords": keywords}

def getRootWord(word):
    size= len(word)
    if word in furnitureTypes:
        return word
    if word[size-1] == 's':
        if  getRootWord(word[0:size-1]) in furnitureTypes:
            return getRootWord(word[0:size-1])
        if word[size-2]=='e' and getRootWord(word[0:size-2]) in furnitureTypes:
            return getRootWord(word[0:size-2])
    equalWord=findInSchema(word, synonyms, False)
    return equalWord[0][0] if equalWord!=[] else word

def findInSchema(word, schema, includeFirst=True):
    if word==schema[0]: return [word]
    rv = []
    for item in schema[1:]:
        if type(item) == type("string"):
            if item == word: return [[schema[0], word]] if includeFirst else [[word]]
        else:
            if item[0]==word: return [[schema[0], word]] if includeFirst else [[word]]
            res = findInSchema(word, item, True)
            if(res != []):
                if len(res) == 1:
                    if includeFirst:
                        temp = [schema[0]]
                        temp.extend(res[0])
                        rv.append(temp)
                    else:
                        rv.append(res[0])
                else:
                    for instance in res:
                        if includeFirst:
                            temp = [schema[0]]
                            temp.extend(instance)
                            rv.append(temp)
                        else:
                            rv.append(instance)
    return rv

def splitToFurnitureWords(string):
    wordsArr = splitToLowerWords(string, "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789’\"'-/")
    newWordArr = []
    skipCount = 0
    for i in range(len(wordsArr)):
        if skipCount == 0:
            word = getRootWord(wordsArr[i])
            multiwords = findInSchema(word, multilengthKeywords, False)
            continueItterating = True
            if multiwords != []:
                for multiword in multiwords:
                    if continueItterating:
                        canBeKeyword = True
                        if(len(multiword)>1):
                            for j in range(1, len(multiword)):
                                if i+j<len(wordsArr):
                                    jAfterWord = getRootWord(wordsArr[i+j])
                                    if(multiword[len(multiword)-1-j] != jAfterWord):
                                        canBeKeyword = False
                                else:
                                    canBeKeyword= False
                            if canBeKeyword:
                                skipCount = len(multiword)-1
                                multiword.reverse()
                                newWordArr.append(' '.join(multiword))
                                continueItterating = False
                        else:
                            newWordArr.append(word)
                            continueItterating = False
                if continueItterating: # if we didn't find any match for the keyword, add it as normal
                    newWordArr.append(word)
            else:
                newWordArr.append(word)
        else: 
            skipCount-=1
    return newWordArr
                
def typesMetadatasList():
    for item in parsedItems:
        title = item.split(':\n')[0] + ' '
        titleWords = splitToLowerWords(title)
        itemTypes = []
        normalItem = True
        for i in range(len(titleWords)):
            word = getRootWord(titleWords[i])
            if word in furnitureTypes:
                if word in singletonTypes:
                    if word=="set":
                        if i==0:
                            print("I dont think this should happen")
                        else: 
                            beforeWord = getRootWord(titleWords[i-1])
                            sets = ['bar','bedroom', 'office', 'room', 'vanity']
                            if beforeWord in sets:
                                if beforeWord == 'room':
                                    if i==1:
                                        print("This is a problem")
                                        continue
                                    else:
                                        beforeBeforeWord = getRootWord(titleWords[i-2])
                                        if beforeBeforeWord in ['bed', 'living']:
                                            itemTypes.append(beforeBeforeWord + ' ' + beforeWord + ' ' + word)
                                else:
                                    itemTypes.append(beforeWord + ' ' + word)
                            elif beforeWord in furnitureTypes:
                                itemTypes.append(beforeWord + ' ' + word)
                            else:
                                print("this is a problem" + beforeWord)
                    else:
                        normalItem = False
                        itemTypeList.append([word])
                elif not (word=="battery" and itemTypes!=[]):
                    itemTypes.append(word)
        if normalItem:
            itemTypeList.append(itemTypes)
        types = itemTypeList.pop()
        allTypes = []
        for furnitureType in types:
            if furnitureType not in allTypes: allTypes.append(furnitureType)
            furnitureSubtypes = findInSchema(furnitureType, furnitureSchema)[0]
            noNext = False
            for subtype in furnitureSubtypes[0:len(furnitureSubtypes)-1]:
                if subtype in allTypes:
                    noNext = True
                elif noNext:
                    noNext = False
                else:
                    allTypes.append(subtype)
        if("furniture" not in allTypes):
            print(allTypes)
        allTypes.remove("furniture")
        itemTypeList.append(allTypes)
    return itemTypeList
