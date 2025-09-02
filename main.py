from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms
from PIL import Image
import io

from model import CarPartsCNN

app = FastAPI()

# simpan status terakhir supaya bisa diakses frontend
latest_status = {}

# CORS supaya frontend bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CarPartsCNN()
model.load_state_dict(torch.load("car_parts_model.pth", map_location=device))
print(device)
model.to(device)
model.eval()
print("Model siap digunakan")

# transformasi gambar
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
])

# mapping komponen mobil
classes = ["Front Right", "Front Left", "Rear Right", "Rear Left", "Hood"]

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global latest_status

    # baca gambar
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = transform(img).unsqueeze(0).to(device)

    # prediksi
    with torch.no_grad():
        outputs = model(img)
        probs = torch.sigmoid(outputs).cpu().numpy()[0]

    status = {}
    for cls, p in zip(classes, probs):
        status[cls] = "Open" if p > 0.5 else "Closed"

    latest_status = status
    return {"status": status}

@app.get("/status")
async def get_status():
    return {"status": latest_status}