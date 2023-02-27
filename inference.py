import torch
import clip
from sentence_transformers import util
from PIL import Image
from utils import load_model
#from lavis.models import load_model_and_preprocess

device = torch.device("cpu")
cap_model, cap_processor = None, None
clip_model, preprocess = None, None
predict_type_model, predict_type_preprocessor = None, None

"""
def infer_generate_caption(img:Image):
    global cap_model, cap_processor, device
    if cap_model == None:
        cap_model, cap_processor, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
    img = cap_processor["eval"](img).unsqueeze(0).to(device)
    caption = cap_model.generate({"image": img})
    return caption
"""
    
def infer_compute_similarity(text:str, img:Image):
    global clip_model, preprocess, device
    # 0.2434956976771353 optimal limit
    if clip_model == None:
        clip_model, preprocess = clip.load("ViT-B/32", device=device)
    
    sentences = text.split('.')
    if (len(sentences) > 1):
        del sentences[-1]
    
    sentences = clip.tokenize(sentences, truncate = True)
    img = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        img_embedding = clip_model.encode_image(img)
        txt_embedding = clip_model.encode_text(sentences)
    
    cosine_scores = util.cos_sim(img_embedding, txt_embedding)
    cosine_scores = cosine_scores.squeeze()
    
    if len(sentences) == 1:
        return cosine_scores.item()
    list_scores = cosine_scores.tolist()
    max_score = max(list_scores)
    response = {'max score':max_score,
                'adequate': 'yes' if max_score > 0.2434956976771353 else 'no',
                'limit used':0.2434956976771353}
    return response

def infer_predict_type(img:Image):
    global predict_type_model, predict_type_preprocessor, device
    if predict_type_model == None:
        predict_type_model, predict_type_preprocessor = load_model(device)
    
    img = predict_type_preprocessor(img).unsqueeze(0)
    prediction = predict_type_model(img)
    prediction = torch.softmax(prediction, dim=1)
    keys = ['just_image', 'bar_chart', 'diagram', 'flow_chart', 'graph', 'growth_chart', 'pie_chart', 'table']
    values = prediction.tolist()[0]
    print(values)
    response = dict(zip(keys,values))
    return response
