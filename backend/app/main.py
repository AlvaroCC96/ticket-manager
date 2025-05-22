import os, shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


from .models import SessionLocal, boletas, engine
from .utils import (
    extract_text_from_pdf,
    extract_text_from_image,
    parse_boleta
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta de uploads
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/upload/")
async def upload_boleta(file: UploadFile = File(...)):
    # Guardar archivo
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
        raise HTTPException(400, "Formato no soportado")
    
    #name file
    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    
    filename = f"{now_str}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extraer texto
    text = ""
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_image(file_path)

    # Parsear boleta
    data = parse_boleta(text)

    # Insertar en DB
    session = SessionLocal()
    try:
        ins = boletas.insert().values(
            servicio=data["servicio"],
            empresa=data["empresa"],
            monto=data["monto"],
            fecha=data["fecha"],
            archivo=filename
        )
        session.execute(ins)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(500, f"DB Error: {e}")
    finally:
        session.close()

    return {"message": "Boleta procesada", **data}

@app.get("/boletas")
def historial_boletas():
    return FileResponse("frontend/public/boletas.html")

@app.get("/api/boletas/")
def list_boletas():
    session = SessionLocal()
    # .mappings() ya devuelve dict-like
    rows = session.execute(boletas.select()).mappings().all()
    session.close()
    return rows

# Calcula la carpeta raíz del proyecto (dos niveles arriba de este archivo)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# Monta StaticFiles apuntando a <root>/frontend/public
app.mount(
    "/",
    StaticFiles(directory=str(PROJECT_ROOT / "frontend" / "public"), html=True),
    name="frontend",
)