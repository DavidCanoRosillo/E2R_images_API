from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
# from inference import infer_generate_caption, infer_compute_similarity, infer_predict_type
from inference import infer_compute_similarity, infer_predict_type
import uvicorn
from utils import translate

app = FastAPI(title='Pautas E2R imagenes')

@app.post('/generate_caption')
async def generate_caption(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    caption = infer_generate_caption(image)
    return caption

@app.post('/compute_similarity')
async def compute_similarity(text:str, file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    en_text = translate(text, 'es', 'en')
    
    similarity = infer_compute_similarity(en_text, image)
    print(similarity)
    return similarity

@app.post('/predict_type')
async def predict_type(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    predictions = infer_predict_type(image)
    return predictions

if __name__ == "__main__":
    uvicorn.run(app, port='8888', host='0.0.0.0')