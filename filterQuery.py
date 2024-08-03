"""
Author: Nathan Derhake. Influence taken from James Briggs, and Langchain documentation.
"""


from addMetadatas import getRootWord, furnitureTypes, splitToFurnitureWords, colorTypes, materialTypes, styleTypes, sizeTypes, keywordsTypes

def filterQuery(query):
    prepositions = ['above', 'across', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'by', 'down', 'from', 'in', 'into', 'near', 'of', 'off', 'on', 'to', 'toward', 'under', 'upon', 'within']
    queryArr = splitToFurnitureWords(query)
    print(queryArr)
    typesMD = []
    excludeTypesMD = []
    colors = []
    materials = []
    styles = []
    sizes = []
    keywords = []
    excludeKeywords = []
    prepositionTimer = 0
    for word in queryArr:
        rootWord = getRootWord(word)
        if rootWord in colorTypes and rootWord not in colors:
            colors.append(rootWord)
        if rootWord in materialTypes and rootWord not in materials:
            materials.append(rootWord)
        if rootWord in styleTypes and rootWord not in styles:
            styles.append(rootWord)
        if rootWord in sizeTypes and rootWord not in sizes:
            sizes.append(rootWord)
        if rootWord in keywordsTypes and rootWord not in keywords:
            if "outdoor" in excludeKeywords and rootWord == "indoor":
                excludeKeywords = []
            else:
                keywords.append(rootWord)
        if rootWord=="indoor" and rootWord not in excludeKeywords:
            if "outdoor" in keywords:
                keywords.remove("outdoor")
            else: 
                excludeKeywords.append("outdoor")
        elif (rootWord in furnitureTypes or (len(rootWord)>4 and rootWord[len(rootWord)-4:] == ' set')) and rootWord not in typesMD:
            if prepositionTimer!=0:
                if rootWord not in typesMD and rootWord != "furniture":
                    excludeTypesMD.append(rootWord)
            elif rootWord != 'set':
                if rootWord in excludeTypesMD:
                    excludeTypesMD.remove(rootWord)
                typesMD.append(rootWord)
        prepositionTimer = max(prepositionTimer-1, 0)
        if word in prepositions:
            prepositionTimer = 2
    if "furniture" in typesMD and "cover" not in typesMD:
        typesMD.remove("furniture")
        excludeTypesMD.append("non furniture")
    return {"type": typesMD, "excludeType": excludeTypesMD, "colors": colors, "materials": materials, "styles": styles, "sizes": sizes, "keywords": keywords, "excludeKeywords": excludeKeywords}
# print(filterQuery('rugs tha dining set'))
