# This app is a custom Living Spaces search engine
This is the source code for my living spaces search engine demo and is a major project in Prodegy Development
If you would like to see the demo itself, go here:
https://plumpsey314-livingspacesembedingstest-demoui-60vk50.streamlit.app/

I made this app from publicly available data on Living Space's website.
It uses OpenAI and Pinecone to create vector embedings to perform a semantic search on my sample of their data.

To run this app, you need to set up an openAI account and a pinecone database. 

## All code written in this repository is by Nathan Derhake 
## (nathanderhake@gmail.com) Github: Plumpsey314

Run this following command:

pip install -r requirements.txt

then create a file called secret.py
in this file, put this code:

import os
os.environ["OPENAI_API_KEY"]="...YOUR OPENAI API KEY..."
