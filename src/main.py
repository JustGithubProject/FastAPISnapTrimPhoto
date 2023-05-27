from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from PIL import Image
import os

app = FastAPI(title="PhotoService")
templates = Jinja2Templates(directory="src/templates")
output_directory = "src/output"  # Путь к директории для сохранения обрезанных изображений


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/crop_image")
async def crop_image(request: Request, file: UploadFile = File(...)):
    form_data = await request.form()
    width = int(form_data["width"])
    height = int(form_data["height"])

    file_extension = file.filename.split(".")[1]
    file_path = os.path.join(output_directory, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    image = Image.open(file_path)
    cropped_image = image.crop((0, 0, width, height))

    cropped_filename = f"cropped_image.{file_extension}"
    cropped_filepath = os.path.join(output_directory, cropped_filename)
    cropped_image.save(cropped_filepath)

    return templates.TemplateResponse("download.html", {"request": request, "cropped_filename": cropped_filename})


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(output_directory, file_name)
    return FileResponse(file_path, filename=file_name)
