"""
Author: Nathan Derhake. Image embeddings. Influence taken from James Briggs, and Langchain documentation.
"""


import torch
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizer
from tqdm.auto import tqdm
from PIL import Image
import numpy as np

def getImageEmbeddings(prompt, emb_obj=None, k=10):
    if emb_obj==None: emb_obj = imagesToVectors()
    model = emb_obj['model']
    tokenizer = CLIPTokenizer.from_pretrained(emb_obj['model_id'])
    inputs = tokenizer(prompt, return_tensors="pt")
    text_emb = model.get_text_features(**inputs).cpu().detach().numpy()
    scores = np.dot(text_emb, emb_obj['embedded_images'])
    best_indecies = np.argsort(-scores[0])[:k]

    best_images = []
    for index in best_indecies:
        image = emb_obj['image_list'][index]
        import matplotlib.pyplot as plt
        plt.imshow(image)
        plt.show()
        print(index)
        best_images.append({"image": image, "score": scores[0][index]})
    return best_images

def imagesToVectors(image_list = None):
    modelID = "openai/clip-vit-base-patch32"
    device = "cpu" 
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps" 
    model = CLIPModel.from_pretrained(modelID).to(device)
    processor = CLIPProcessor.from_pretrained(modelID)
    
    # creates image embeddings object
    imgs_len = 286
    images = [] if not image_list else image_list
    batch_size = 16
    embedded_images = []
    for i in tqdm(range(0, imgs_len, batch_size)):
        # Get the list of images
        raw_batch = []
        for j in range(batch_size):
            if i+j<imgs_len:
                image = Image.open('images/myId' + str(i+j) + '.png')
                if not image_list: images.append(image) 
                raw_batch.append(image)
        # Uses CLIP to see what is most similar to the prompt
        batch = processor(
            text=None,
            images = raw_batch,
            return_tensors="pt",
            padding=True
        )['pixel_values'].to(device)
        img_emb = model.get_image_features(pixel_values=batch).squeeze(0).cpu().detach().numpy()
        if embedded_images==[]:
            embedded_images = img_emb
        else:
            embedded_images = np.concatenate((embedded_images, img_emb), axis=0)
    embedded_images = embedded_images.T/np.linalg.norm(embedded_images, axis=1)
    return {
        "model": model,
        "model_id": modelID,
        "embedded_images": embedded_images,
        "image_list": images
    }
    
getImageEmbeddings(prompt="movie theater furniture")
