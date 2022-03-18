# image.py

from fastapi import FastAPI
from fastapi.responses import FileResponse

image_path = "my_image.png"
app = FastAPI()

@app.get("/")
async def main():
    return FileResponse(image_path)
