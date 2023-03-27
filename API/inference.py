import torch
from PIL import Image
from utils import load_model
from lavis.models import load_model_and_preprocess

device = "cpu"
cap_model, cap_processor = None, None
predict_type_model, predict_type_preprocessor = None, None
model, vis_processors, text_processors = None, None, None

def reset(model:int):
    if model != 0:
        cap_model, cap_processor = None, None
    if model != 1:
        predict_type_model, predict_type_preprocessor = None, None
    if model != 2:
        model, vis_processors, text_processors = None, None, None


def infer_generate_caption(img:Image):
    global cap_model, cap_processor, device
    reset(0)
    if cap_model == None:
        print("loading model caption")
        cap_model, cap_processor, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
    img = cap_processor["eval"](img).unsqueeze(0).to(device)
    caption = cap_model.generate({"image": img})
    return caption

def infer_compute_similarity(txt:str, img:Image):
    global model, vis_processors, text_processors
    reset(1)
    if model == None:
        print("loading model similarity")
        model, vis_processors, text_processors = load_model_and_preprocess("blip2_image_text_matching", "pretrain", device=device, is_eval=True)
    img = vis_processors["eval"](img).unsqueeze(0).to(device)
    txt = text_processors["eval"](txt)
    itm_output = model({"image": img, "text_input": txt}, match_head="itm")
    itm_scores = torch.nn.functional.softmax(itm_output, dim=1)
    score = itm_scores[:, 1].item()

    threshold = 8
    response = {'max_score': score * 100,
                'adequate': 'si' if score > threshold else 'no',
                'limit_used':threshold}
    return response

def infer_predict_type(img:Image):
    global predict_type_model, predict_type_preprocessor, device
    reset(2)
    if predict_type_model == None:
        print("loading model predict")
        predict_type_model, predict_type_preprocessor = load_model(device)
    
    img = predict_type_preprocessor(img).unsqueeze(0)
    prediction = predict_type_model(img)
    prediction = torch.softmax(prediction, dim=1) * 100
    keys = ['just_image', 'bar_chart', 'diagram', 'flow_chart', 'graph', 'growth_chart', 'pie_chart', 'table']
    values = prediction.tolist()[0]
    response = dict(zip(keys,values))
    return response
