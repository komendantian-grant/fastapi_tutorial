from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, Response

from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/reverse_image/")
async def create_upload_files(files: List[UploadFile]):
    jpeg_bytes = await files[0].read()
    jpeg_bytes_io = BytesIO(jpeg_bytes)
    jpeg_object = Image.open(jpeg_bytes_io)
    jpeg_object_return = jpeg_object.rotate(180)
    jpeg_bytes_io_return = BytesIO()
    jpeg_object_return.save(jpeg_bytes_io_return, format="JPEG")
    jpeg_bytes_io_return.seek(0)
    jpeg_bytes_return = jpeg_bytes_io_return.read()
    return Response(jpeg_bytes_return, media_type="image/jpg")

@app.get("/")
async def main():
    content = """
<body>
<form action="/reverse_image/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
