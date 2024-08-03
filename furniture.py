"""
Author: Nathan Derhake. Influence taken from James Briggs, and Langchain documentation.
"""


# imports
import math
import random
from pinecone import Pinecone
import openai
import os
import streamlit as st
from addMetadatas import typesMetadatasList, getMetadataDetails
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore

# import secret

# pinecone stuff
# initialize pinecone
pc_api = os.environ["PC_API_KEY"]
pc = Pinecone(
    api_key=pc_api
)
indexName = "furniture-index" # the name of the pinecone database

# initialize openai
os.environ["OPENAI_API_KEY"]=st.secrets["OPENAI_API_KEY"] # storing openai key in streamlit
# import secret # stroring openai secret in ignored file
embeddings = OpenAIEmbeddings(openai_api_version="text-embedding-ada-002")

# Some useful methods for testing/creating custom vectors
# returns the nunmber of vectors in the pinecone database
def pineconeSize(index_name):
    index = pc.Index(index_name)
    namespaces = index.describe_index_stats()['namespaces'] 
    if(namespaces == {}):
        return 0
    if(len(namespaces) == 1):
        return index.describe_index_stats()['namespaces']['']['vector_count']
    return len(namespaces)

def strArrToVect(strArr): # turns a string representation of an array to a vector
    vect = []
    for strNum in strArr[strArr.index('[')+1:strArr.index(']')].split(','):
        vect.append(float(strNum))
    return vect

def insertData(vect, width, depth, height, lbs): # adds data to embedings in such a way that it is relevent and keeps variance 1
    # 15% lbs 5%  the others lbs^2+counter^2=0.15 500 = max wieght 200 max W 100 max D 100 max H
    if(width>200):
        vect.append(0.2)
        vect.append(0.1)
    else:
        widthVect = 0.22360679774997896*width/200 
        vect.append(widthVect)
        vect.append( -math.sqrt(0.05-widthVect*widthVect))
    if(depth>100):
        vect.append(0.2)
        vect.append(0.1)
    else:
        depthVect = 0.22360679774997896*depth/100 
        vect.append(depthVect)
        vect.append( -math.sqrt(0.05-depthVect*depthVect))
    if(height>100):
        vect.append(0.2)
        vect.append(0.1)
    else:
        heightVect = 0.22360679774997896*height/100 
        vect.append(heightVect)
        vect.append( -math.sqrt(0.05-heightVect*heightVect))
    if(lbs>500):
        vect.append(0.3742)
        vect.append(0.1)
    else:
        lbsVect = 0.3872983346207417*lbs/500 
        vect.append(lbsVect)
        vect.append( -math.sqrt(0.15-lbsVect*lbsVect))
    return vect

def calculateVariance(vector):
    sum = 0
    for num in vector:
        sum += num*num
    return sum

def calculateDistance(vectA, vectB):
    sum = 0
    for i in range(len(vectA)):
        diff = vectA[i]-vectB[i]
        sum += diff*diff
    return sum

def queryDistance(queryA, queryB, pineconeVectors):
    return calculateDistance(pineconeVectors._embedding_function(queryA), pineconeVectors._embedding_function(queryB))

def randVect(length):
    size = 2*math.sqrt(3/length) # This is the size needed for the variance of the vector to be 1.
    vector = []
    for i in range(length):
        vector.append(random.random()*size - size/2)
    return vector

def scaleVect(vect, scale):
    rv = []
    for dimention in vect:
        rv.append(dimention*scale)
    return rv

def addVectorsInBatches(toAdd, customAddition): # adds vectors to indexName
    itemTypeList = typesMetadatasList()
    itemColorList = getMetadataDetails()["colors"]
    itemMaterialList = getMetadataDetails()["materials"]
    itemStyleList = getMetadataDetails()["styles"]
    itemSizeList = getMetadataDetails()["sizes"]
    itemKeywordList = getMetadataDetails()["keywords"]


    arrCount = len(toAdd)
    startingId = pineconeSize(indexName)
    batches = 1 + arrCount//32
    for i in range(batches):
        firstItemIndex = 32*i
        itemsToInsert = [] # will be a subsection of the strings we are going to embed
        if(firstItemIndex == arrCount):
            continue
        numItemsToInsert = arrCount-firstItemIndex if firstItemIndex+31 >= arrCount else 32
        itemsToInsert = toAdd[firstItemIndex:firstItemIndex+numItemsToInsert]
        if (customAddition):
            ids = []
            for j in range(numItemsToInsert):
                item = parsedItems[firstItemIndex + j]
                splitItem = item.split(':\n')
                vectorIndex.upsert([(splitItem[0], toAdd[j], {"namespace": splitItem[0], "title": splitItem[0], "description": splitItem[1], "text": splitItem[0], "page_content": item})], namespace=splitItem[0])
        else:
            ids = []
            metadatas = []
            for j in range(numItemsToInsert):
                ids.append("myId" + str(startingId+firstItemIndex+j))
                metadatas.append({"type":itemTypeList[firstItemIndex+j], "color": itemColorList[firstItemIndex+j], "material": itemMaterialList[firstItemIndex+j], "style": itemStyleList[firstItemIndex+j], "size": itemSizeList[firstItemIndex+j], "keyword": itemKeywordList[firstItemIndex+j]})
            vectorDoc.add_texts(iter(itemsToInsert), metadatas=metadatas, ids=ids) # adds new data to Pinecone

def removeUselessWords(sentence):
    uselessWords = ['i', 'me', 'my', 'am', 'looking', 'there\'s', 'plenty', 'going', 'you\'ll', 'has', 'you\'re', 'I\'m', 'and', 'a', 'to', 'the', 'with', 'of', 'have', 'for', 'our', 'in', 'you', 'your', 'is', 'that', 'this', 'can', 'it', 'space', 'are', 'features', 'from', 'but', 'all', 'on', 'which', 'any', 'will', 'collection', 'be', 'thanks', 'an', 'or', 'power', 'as', 'perfect', 'at', 'even', 'look', 'so', 'by', 'its', 'quality', 'best', 'while', 'up', 'easy', 'top', 'offers', 'extra', 'value', 'sophisticated', 'get', 'inviting', 'create', 'through', 'experience', 'program', 'also', 'choose', 'like', 'details', 'into', 'addition', 'provide', 'featuring', 'comes', 'not', 'made', 'style', 'when', 'more']
    itemsWords = []
    legalChars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789’\"'-"
    curWord = ''
    for char in sentence:
        if(char in legalChars):
            curWord += char.lower()
        else:
            if(len(curWord) > 0 and not(curWord in uselessWords)):
                itemsWords.append(curWord.lower())
            curWord = ''
    if(len(curWord) > 0 and not(curWord in uselessWords)):
        itemsWords.append(curWord.lower())
    return ' '.join(itemsWords)


parsedItems = [] # This is the array of furniture data

# # Once we have our embeddings, we do not need this. 
# # You do not need to comment this code back in, but you can.
furnitureFile = open('furnitureList.txt', 'r', encoding='utf8') # open file
fileString = furnitureFile.read() # all of the furnaiture in one string
# file parsing; Making sure that everything is in the perfect format before I start embedding
rawItems = fileString.split('\n\n')
# Each item should be in this exaft format: title:\ndescription
for item in rawItems:
    splitItem = item.split(':\n')
    if(len(splitItem)!=2):
        print("something is wrong with this item. I think two items are glued toghether. This is what the item looks like: " + item)
        continue
    # remove unnesesary new line characters
    title = splitItem[0].replace('\n', '')
    description = splitItem[1].replace('\n', '')
    parsedItems.append(title + ':\n' + description)

# # adds furniture dimentions to parsedItems
# with open('furnitureSizeMass.csv', 'r') as file:
#     file.readline() # first line does not matter
#     for i in range(len(parsedItems)):
#         curLine = file.readline()
#         splitItem = parsedItems[i].split(':\n')
#         title = splitItem[0].replace('\n', '')
#         description = splitItem[1].replace('\n', '')
#         dimentionData = strArrToVect('[' + curLine + ']') # array with sizes and weight
#         strToAdd = ''
#         strToAdd += "This item's width is " + str(dimentionData[0]) + " inches."
#         strToAdd += " This item's depth is " + str(dimentionData[1]) + " inches."
#         strToAdd += " This item's height is " + str(dimentionData[2]) + " inches."
#         strToAdd += " This item's weight is " + str(dimentionData[3]) + " pounds."
#         parsedItems[i] = title + ':\n' + strToAdd + ' ' + description
# # Structures files such that it filters out unhelpful words
# rawItems = fileString.split('\n\n')
# parsedItems = list(map(removeUselessWords, rawItems))

# CODE TO CREATE THE EMBEDINGS NOT TO SEARCH. Should only be run once (by me) then never again unless we are reformating our database.
# Do not comment this code back in
# pinecone vector index creation
# pc.create_index(indexName, dimension=1536,metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1")) # create pinecone index
##### leave this uncommented. These are 2 different objects describing the same vector doc. they have different uses
vectorDoc = PineconeVectorStore(index_name=indexName, embedding=embeddings, pinecone_api_key=pc_api) # the pinecone object
vectorIndex = pc.Index(indexName)
#####
# vector deletion
# vectorIndex.delete(delete_all=True)
# # custom vector deletion
# for item in parsedItems:
#     toDelete = item.split(':\n')[0]
#     vectorIndex.delete(ids=[toDelete], namespace=toDelete)
# normal vector Creation
# addVectorsInBatches(parsedItems, False) # adds vectors to Pinecone
# Custom vector creation
# # generating the vector array from the file
# vectors = []
# with open('embedings.txt', 'r') as file:
#     curLine = file.readline()
#     count = 0
#     while (curLine != '' and count<169):
#         count += 1
#         vectors.append(strArrToVect(curLine)) # adds the current line to vectors
#         curLine = file.readline() # reads the next line of the file
# # opening the furniture dimentions and weight csv
# with open('furnitureSizeMass.csv', 'r') as sheet:
#     sheet.readline() # this is the title line. We do not care about this
#     curLine = sheet.readline().strip('\n')
#     count = 0
#     while (curLine != ''):
#         csvData = curLine.split(',') # array with sizes and weight
#         dimentionData = strArrToVect('[' + ','.join(csvData[0:len(csvData)-1]) + ']')
#         curVect = vectors[count]
#         vectors[count] = insertData(curVect[0:len(curVect)-8], dimentionData[0], dimentionData[1], dimentionData[2], dimentionData[3])
#         count += 1
#         curLine = sheet.readline().strip('\n')
# addVectorsInBatches(vectors, True) # adds vectors to Pinecone

# # searching for furniture
# query = "I am looking for couches/sofas/chairs to decorate my private movie theatre"
# queryA = "I am looking for waterproof furniture"
# queryB = "I am looking for grey pieces of furniture"
# queryC = "Furniture for an office"
# queryD = "I want chairs that will look good in my bed room"
# queryE = "bench"
# queryF = "Introducing our sleek wooden chairs, perfect for small apartments. Crafted with precision and functionality in mind, these chairs effortlessly complement any decor. Made from high-quality solid wood, they offer a timeless appeal. With their slender profile, they add an elegant touch and optimize space. Despite their petite design, the curved backrest provides excellent support for comfortable seating. Versatile and durable, these chairs are ideal for dining, working, or relaxing. Upgrade your small apartment with these exquisite wooden chairs and create a cozy and stylish environment."
# queryG = "I have a friend coming home from a backbadking trip, and I want to get a really comfortable couch for him once he gets home. I don't really care about the colour, but I deffinitely need the couch to have good leg support, and maybe even recline because I think my friend's legs would be extremely tired."
# queryH = "Set the mood and turn up the heat with our Linette fireplace console – a design that allows you to enjoy all the perks of having a fireplace without the stress, expense or inconvenience. A 42-inch fireplace insert produces ambient flame-like lighting that you can use with the included clear fire glass crystals or traditional logs to create your desired look. The fan-forced heater even offers multiple settings for providing the perfect temperature. The focal point of your space, this piece also fits a TV up to 96 inches and includes cord management cutouts to minimize wire clutter."
# queryI = "I am looking for deviders for me and my roomate"

# # Embeding queries
# queries = [query, queryA, queryB, queryC, queryD, queryE, queryF, queryG, queryH, queryI]
# # embeddedQueries = list(map(vectorDoc._embedding_function, list(map(removeUselessWords, queries)))) #caveman
# # embeddedQueries = list(map(vectorDoc._embedding_function, queries)) # not caveman

# rawReleventItems = vectorDoc.similarity_search(query="poolside chairs", k=10) # k is the number of results
# releventItemsAndDescription = [] # The furniture title and description with no metadata
# for item in rawReleventItems:
#     releventItemsAndDescription.append(item.page_content)
# releventTitles = [] # A list of all the furniture titles
# for item in releventItemsAndDescription:
#     releventTitles.append(item.split(':\n')[0])
# print(releventItemsAndDescription)
# print(releventTitles)
# print(parsedItems.index(rawReleventItems[0].page_content))



# print(vectorIndex)

# ids = [] # a list of all the ids in pinecone
# size = pineconeSize(indexName)
# for i in range(size):
#     # ids.append(parsedItems[i].split(':\n')[0])
#     ids.append("myId"+str(i))
# vectors = [] # a list of all the vectors in pinecone
# for id in ids:
#     # print(id)
#     # print(vectorIndex.fetch([id]))
#     vectors.append(vectorIndex.fetch([id])['vectors'][id]['values'])

# vectors.extend(embeddedQueries)

# # seeing what happens if we remove the last 8 dimentions.
# for vector in vectors:
#     vectorLen = len(vector)
#     for i in range(8):
#         vector[vectorLen-1-i] = 0

# scaledVectors = [] # the same embeding vector, but the variance is 0.7 instead of 1
# for vector in vectors:
#      # 1536n^2 = 1 we want 1528m^2 = 0.7, so multiply by |m|/|n| which is about sqrt(0.7)
#      scaledVectors.append(scaleVect(vector, 0.838847376741424)) # scale such that the variance of the 1528 nonzero items is 0.7

# # clears the file
# with open('embedings.txt', 'r+') as file:
#     file.truncate()
#     file.close()
# # adding vectors to embedings file
# with open('embedings.txt', 'a') as file:
#     # for vector in scaledVectors:
#     for vector in vectors:
#         file.write(str(vector)+'\n')
