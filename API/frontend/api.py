from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title='Pautas E2R imagenes')

@app.get("/", response_class=HTMLResponse)
async def read_items():
    f = open("index.html")
    html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/js/test.js", response_class=HTMLResponse)
async def read_items():
    f = open("js/test.js")
    html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post('/generate_caption')
async def generate_caption(file: UploadFile = File(...)):
    return 'This is an example caption'

@app.post('/compute_similarity')
async def compute_similarity(text:str, file: UploadFile = File(...)):
    return "similarit'"

@app.post('/predict_type')
async def predict_type(file: UploadFile = File(...)):
    return "prediction"

if __name__ == "__main__":
    uvicorn.run(app, port='1234', host='0.0.0.0')
