from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI(title='Pautas E2R imagenes')

@app.post('/generate_caption')
async def generate_caption(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = Image.open(BytesIO(await file.read()))
    return 'hi'

@app.post('/compute_similarity')
async def compute_similarity(text:str, file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = Image.open(BytesIO(await file.read()))
    return 'hi'

@app.post('/predict_type')
async def predict_type(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = Image.open(BytesIO(await file.read()))
    return 'hi'

if __name__ == "__main__":
    uvicorn.run(app, port='8888', host='0.0.0.0')