from sentence_transformers import SentenceTransformer, util
from image_captioning import clip_model, preprocess
import torchvision
import torch
import clip
from sentence_transformers import SentenceTransformer, util
from PIL import Image

model = SentenceTransformer('all-mpnet-base-v2')

def mean_similarity(caption, text):
    sentences = text.split('.')
    if (len(sentences) > 1):
        del sentences[-1]
    caption_embedding = model.encode(caption)
    text_embeddings = model.encode(sentences)

    cosine_scores = util.cos_sim(caption_embedding, text_embeddings)
    cosine_scores = cosine_scores.squeeze()
    if len(sentences) == 1:
        return cosine_scores.item()

    list_scores = cosine_scores.tolist()
    #return sum(list_scores) / len(sentences)
    return max(list_scores)

def clip_similarity(img_path, text):
    sentences = text.split('.')
    if (len(sentences) > 1):
        del sentences[-1]

    image = torchvision.io.read_image(img_path)
    transform = torchvision.transforms.ToPILImage()
    resize = torchvision.transforms.Resize((224, 224))
    pil_image = transform(resize(image))

    sentences = clip.tokenize(sentences, truncate = True)

    image = preprocess(pil_image).unsqueeze(0)
    with torch.no_grad():
        img_embedding = clip_model.encode_image(image)
        txt_embedding = clip_model.encode_text(sentences)

    cosine_scores = util.cos_sim(img_embedding, txt_embedding)
    cosine_scores = cosine_scores.squeeze()
    if len(sentences) == 1:
        return cosine_scores.item()

    list_scores = cosine_scores.tolist()
    return max(list_scores)

from sentence_transformers import SentenceTransformer, util
from PIL import Image

#model_large = SentenceTransformer('clip-ViT-L-14')
model_large = SentenceTransformer('clip-ViT-B-32')

def clip_large(img_path, text):
    sentences = text.split('.')
    if (len(sentences) > 1):
        del sentences[-1]
    sentences = clip.tokenize(sentences, truncate = True)
    
    image = torchvision.io.read_image(img_path)
    transform = torchvision.transforms.ToPILImage()
    resize = torchvision.transforms.Resize((224, 224))
    pil_image = transform(resize(image))

    #Encode an image:
    image = preprocess(pil_image).unsqueeze(0)
    
    img_emb = model.encode(image)

    #Encode text descriptions
    text_emb = model.encode(sentences)

    #Compute cosine similarities 
    cosine_scores = util.cos_sim(img_emb, text_emb)
    cosine_scores = cosine_scores.squeeze()
    #print(cosine_scores.shape)
    if len(sentences) == 1:
        return cosine_scores.item()

    list_scores = cosine_scores.tolist()
    return max(list_scores)