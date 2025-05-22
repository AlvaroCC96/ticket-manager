# Boletas Tracker App

**Boletas Tracker App** es una aplicación web **100% local** que corre en tu Raspberry Pi (o en tu PC) y te permite:

- **Subir boletas** (PDF o imagen) de servicios del hogar (agua, luz, internet, teléfono).  
- **Extraer automáticamente** los datos clave de cada boleta:  
  - **Servicio** (empresa)  
  - **Monto** (en CLP)  
  - **Fecha** (de emisión o vencimiento)  
- **Almacenarlos** en una base de datos SQLite.  
- Mostrar un **historial** y un pequeño **dashboard** para consultar todas tus boletas.

---

## 📂 Estructura del proyecto

```text
boletas_tracker_app/
├── backend/
│   ├── app/
│   │   ├── main.py        ← FastAPI + rutas API + Jinja2
│   │   ├── models.py      ← Definición de la tabla SQLite
│   │   ├── utils.py       ← Lógica de extracción y parseo OCR/PDF
│   │   └── templates/     ← Plantillas Jinja2 (boletas.html)
│   └── uploads/           ← Archivos subidos (PDFs/imagenes)
├── frontend/
│   └── public/
│       ├── index.html     ← Formulario de subida de boletas
│       ├── boletas.html   ← Vista de historial (tabla Bootstrap)
│       ├── main.js        ← Lógica de envío y notificaciones
│       └── boletas.js     ← Lógica de carga de la tabla
└── requirements.txt       ← Dependencias Python
```

---

## ⚙️ Tecnologías

- **Backend**  
  - [FastAPI](https://fastapi.tiangolo.com/)  
  - [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite)  
  - [pdfplumber](https://github.com/jsvine/pdfplumber) (extraer texto de PDFs)  
  - [Pillow](https://python-pillow.org/) + [pytesseract](https://github.com/madmaze/pytesseract) (OCR para imágenes)  
- **Frontend**  
  - HTML5 + [Bootstrap 5](https://getbootstrap.com/)  
  - JavaScript nativo  

---

## 📝 Requisitos

1. **Python 3.8+**  
2. **Tesseract OCR** (solo para extracción de texto en imágenes)  
   ```bash
   sudo apt update
   sudo apt install -y tesseract-ocr libtesseract-dev
   ```
3. Clonar este repositorio y crear un entorno virtual:
   ```bash
   git clone https://github.com/tuusuario/boletas_tracker_app.git
   cd boletas_tracker_app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 🚀 Arrancar la aplicación

Dentro de tu entorno virtual:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 5000 --reload
```

- El frontend quedará disponible en  
  `http://<IP_Raspberry>:5000/`

---

## 📋 Uso

1. **Subir boleta**  
   - Abre `http://localhost:5000/`  
   - Selecciona tu archivo PDF o imagen de la boleta.  
   - Haz clic en **"Subir y procesar"**.  
   - Verás un mensaje con el **servicio**, **monto** y **fecha** extraídos.  

2. **Ver historial**  
   - Haz clic en **"Ver Historial de Boletas"** o visita  
     `http://localhost:5000/boletas.html`  
   - Se listarán todas las boletas cargadas con:  
     - ID  
     - Servicio  
     - Monto  
     - Fecha  
     - Enlace al archivo original  

---

## 🔧 Personalización y extensiones

- **Notificaciones**: Integrar Telegram o WhatsApp para avisos de boletas por vencer.  
- **Gráficos**: Añadir Chart.js o un motor de gráficas para estadísticas mensuales.  
- **Autenticación**: Si lo compartes en tu LAN, añade un login sencillo.  
- **Multiusuario**: Escala la DB para varios hogares o cuentas.  
- **Importación masiva**: Carpeta watchers para subir varios archivos de golpe.  

---

¡Y listo! Con esto tienes un *centro de control doméstico* para mantener tus gastos de servicios siempre organizados y a la vista. 🏠📊🎉  
