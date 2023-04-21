import pandas as pd
import random
import json
import torch
from tqdm import tqdm

def create_pd(pairs=1000):
    """
        Returns dataframe of 200 same index pairs and 200 different index pairs
        Same index pairs are on even rows and different index pairs on odd rows
        Odd rows will generally have different index, but if 2 random numbers 
        roll same numbers it is possible to have same index.
    """
    s1 = pd.DataFrame(columns=['id_imagen', 'id_description', 'CLIP'])

    shuffled_descriptions = list(range(pairs))
    shuffled_images = list(range(pairs))
    random.shuffle(shuffled_descriptions)
    random.shuffle(shuffled_images)

    for i in range(pairs):
        #if i % 2 == 0: # same index pair
        new_row = pd.Series({'id_imagen': i, 'id_description': i})
        s1 = pd.concat([s1, new_row.to_frame().T], ignore_index=True)
        # else: # different index pair
        #    new_row = pd.Series({'id_imagen': shuffled_images.pop(), 'id_description': shuffled_descriptions.pop()})
        #    s1 = pd.concat([s1, new_row.to_frame().T], ignore_index=True)
    for i in range(pairs):
        new_row = pd.Series({'id_imagen': shuffled_images.pop(), 'id_description': shuffled_descriptions.pop()})
        s1 = pd.concat([s1, new_row.to_frame().T], ignore_index=True)
    return s1

class PairsDataset(torch.utils.data.Dataset):
    """
        Reads json file with descriptions, reads images and returns path
    """
    def __init__(self, json_path, images_path, dataframe):
        f = open(json_path)
        self.data = json.load(f)
        self.path = images_path
        self.df = dataframe
    
    def update_df(self, idx, CLIP_score, CLIP_LARGE_score):
        self.df.at[idx,'CLIP'] = CLIP_score
        #self.df.at[idx,'CLIP_LARGE'] = CLIP_LARGE_score
    
    def save_df(self, path):
        self.df.to_csv(path)
        return None
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        id_description = self.df.at[idx,'id_description']
        id_imagen = self.df.at[idx,'id_imagen']
        
        text = self.data[id_description]['description']
        img_path = self.path + '/' + str(id_imagen) + '.png'
        return idx, text, img_path

# df = create_pd(2000)
df = create_pd(2200)
#df = pd.read_csv('/Users/dcr/uni/beca/demo/out_clip_small.csv')
json_path = '/Users/dcr/dataset/images/cleaned.json'
img_path = '/Users/dcr/dataset/images'
ds = PairsDataset(json_path, img_path, df)

print("Cargando modelo ClipCap")
from image_captioning import generate_caption
from utils import translate
print("Cargando modelo MPNET")
from semantic_similarity import mean_similarity, clip_similarity
from semantic_similarity import clip_large

"""
for i, (idx, text, img_path) in enumerate(tqdm(ds)):
    # en_caption = generate_caption(img_path)
    if not pd.isna(ds.df.at[idx,'CLIP']):
        print("Already done")
        pass      
    en_text = translate(text, 'es', 'en')
    
    CLIP_max_score = clip_similarity(img_path, en_text)
    
    #CLIP_large = clip_large(img_path, en_text)
    # print(idx, idx % 2 == 0 , MPNET_mean_score, CLIP_max_score)
    # es_caption = translate(en_caption, 'en', 'es')
    ds.update_df(idx, CLIP_max_score, 0)
    #if i % 100 == 0:
    #    ds.save_df('out_clip_small.csv')
"""
#ds.save_df('out_clip_small.csv')

print(len(ds))
print(len(ds.df))

for i in tqdm(range(0, len(ds.df))):
    idx, text, img_path = ds.__getitem__(i)    

    en_text = translate(text, 'es', 'en')
    
    CLIP_max_score = clip_similarity(img_path, en_text)
    
    ds.update_df(idx, CLIP_max_score, 0)
    if i % 100 == 0:
        print(i)
        ds.save_df('final_results.csv')

ds.save_df('final_results.csv')
