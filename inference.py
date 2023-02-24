import torch
from PIL import Image
from lavis.models import load_model_and_preprocess

device=torch.device("cpu")
cap_model, cap_processor = None, None
clip_model, clip_text_processor, clip_image_processor = None, None, None
predict_type_model, predict_type_processor = None, None

def infer_generate_caption(img:Image):
    global cap_model, cap_processor, device
    if cap_model == None:
        cap_model, cap_processor, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
    img = cap_processor["eval"](img).unsqueeze(0).to(device)
    caption = cap_model.generate({"image": img})
    return caption

def infer_compute_similarity(text:str, img:Image):
    global clip_model, clip_image_processor, clip_text_processor, device
    if clip_model == None:
        clip_model, clip_image_processor, clip_text_processor = load_model_and_preprocess(name="blip_feature_extractor", model_type="base", is_eval=True, device=device)
    image = clip_image_processor["eval"](img).unsqueeze(0).to(device)
    text_input = clip_text_processor["eval"](text)
    sample = {"image": image, "text_input": [text_input]}
    features_image = clip_model.extract_features(sample, mode="image")
    features_text = clip_model.extract_features(sample, mode="text")
    similarity = features_image.image_embeds_proj[:, 0, :] @ features_text.text_embeds_proj[:, 0, :].t()
    return similarity.item()


def infer_predict_type(img:Image):
    global predict_type_model, predict_type_processor, device
    if predict_type_model == None:
        predict_type_model, predict_type_processor = None, None
