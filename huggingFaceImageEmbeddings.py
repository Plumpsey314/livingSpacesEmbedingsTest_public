"""
Author: Nathan Derhake. Influence taken from James Briggs, and Langchain documentation.
"""


from datasets import load_dataset
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
import torch
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

images = load_dataset('frgfm/imagenette', 'full_size', split='train', ignore_verifications=False)

device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
model_id = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(model_id).to(device)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

prompt = "I am looking for something to put in a junk store."
inputs = tokenizer(prompt, return_tensors="pt")

txt_emb = model.get_text_features(**inputs)

sample_num = 128
np.random.seed(4)
sample_img_ids = np.random.randint(0, len(images), sample_num).tolist()
images_subset = [images[i]['image'] for i in sample_img_ids]
batch_size = 16
img_arr = []
for i in tqdm(range(0, len(images_subset), batch_size)):
    raw_images = images_subset[i:i+batch_size]
    batch = processor(
        text=None,
        images=raw_images,
        # images=np.array(raw_images),
        return_tensors="pt",
        padding=True
    )['pixel_values'].to(device)

    img_emb = model.get_image_features(pixel_values=batch).squeeze(0).cpu().detach().numpy()

    if img_arr == []:
        img_arr = img_emb
    else:
        img_arr = np.concatenate((img_arr, img_emb), axis=0)
img_arr = img_arr.T/np.linalg.norm(img_arr, axis=1)

txt_emb = txt_emb.cpu().detach().numpy()

scores = np.dot(txt_emb, img_arr)
k=10
best_indecies = np.argsort(-scores[0])[:k]

for i in best_indecies:
    print(scores[0][i])
    plt.imshow(images_subset[i])
    plt.show()
