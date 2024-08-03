"""
Author: Nathan Derhake.
"""

from furniture import parsedItems, vectorDoc
from filterQuery import filterQuery
from PIL import Image
import streamlit as st

defaultKValue = 3

st.title("New LIVING SPACES Search Demo")
k = st.number_input("Number of results", step=1, min_value=1, value=defaultKValue)
query = st.text_input("Search for furniture here")

if(query and k>=1):
    defaultKValue = k
    filteredMetadata = filterQuery(query)
    typesMetadata = {}
    colorsMetadata = {}
    materialsMetadata = {}
    stylesMetadata = {}
    sizesMetadata = {}
    keywordsMetadata = {}
    if(filteredMetadata["type"] != []):
        typesMetadata["$in"] = filteredMetadata["type"]
    if(filteredMetadata["excludeType"] != []):
        typesMetadata["$nin"] = filteredMetadata["excludeType"]
    if(filteredMetadata["colors"] != []):
        colorsMetadata["$in"] = filteredMetadata["colors"]
    if(filteredMetadata["materials"] != []):
        materialsMetadata["$in"] = filteredMetadata["materials"]
    if(filteredMetadata["styles"] != []):
        stylesMetadata["$in"] = filteredMetadata["styles"]
    if(filteredMetadata["sizes"] != []):
        sizesMetadata["$in"] = filteredMetadata["sizes"]
    if(filteredMetadata["keywords"] != []):
        keywordsMetadata["$in"] = filteredMetadata["keywords"]
    if(filteredMetadata["excludeKeywords"] != []):
        keywordsMetadata["$nin"] = filteredMetadata["excludeKeywords"]
    rawReleventItems = vectorDoc.similarity_search(query=query, filter={"type": typesMetadata, "color": colorsMetadata, "material": materialsMetadata, "style": stylesMetadata, "size": sizesMetadata, "keyword": keywordsMetadata}, k=int(k)) # k is the number of results
    releventItemsAndDescription = [] # The furniture title and description with no metadata
    for item in rawReleventItems:
        releventItemsAndDescription.append(item.page_content)
    for item in releventItemsAndDescription:
        splitItem = item.split(':\n')
        itemTitle = splitItem[0]
        itemDescription = splitItem[1]
        st.markdown('**' + itemTitle + '**')
        st.image(Image.open('images/myId' + str(parsedItems.index(item)) + '.png'), width=400)
        st.write(itemDescription)
        st.write("__________________________________________________")
