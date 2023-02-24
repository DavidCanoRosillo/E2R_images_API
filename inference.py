from PIL import Image

cap_model, cap_processor = None, None
clip_model, clip_text_processor, clip_image_processor = None, None, None
predict_type_model, predict_type_processor = None, None

def infer_generate_caption(img:Image):
    global cap_model, cap_processor
    if cap_model == None:
        cap_model, cap_processor = None, None

def infer_compute_similarity(text:str, img:Image):
    global clip_model, clip_text_processor, clip_image_processor
    if clip_model == None:
        clip_model, clip_text_processor, clip_image_processor = None, None, None

def infer_predict_type(img:Image):
    global predict_type_model, predict_type_processor
    if predict_type_model == None:
        predict_type_model, predict_type_processor = None, None
