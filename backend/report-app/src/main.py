import os
import re

from typing import Any
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

INVALID_PATH_REGEX = re.compile(r"\.|/|\\")

def valid_filename(filename: str) -> bool:
    return INVALID_PATH_REGEX.match(filename) is None

@app.get("/")
async def root():
    return {"Server says It's All Good"}

@app.post("/report")
def create_report(
    *,
    filename: str = 'report.json',
    http_request: Request
) -> Any:
    if not valid_filename(filename):
        return JSONResponse(content=f"Invalid filename",status_code=404)

    try:
        with open("../shared/" + filename, 'x') as _:
            pass
    except FileExistsError:
        return JSONResponse(content=f"Report named {filename} already exists",status_code=409)

    return JSONResponse(content=f"Report named {filename} created",status_code=200)


@app.get("/report")
def get_report(
    *,
    filename: str = 'report.json',
    http_request: Request
) -> Any:
    if not valid_filename(filename):
        return JSONResponse(content=f"Invalid filename",status_code=404)

    report_path = os.path.abspath("../shared/" + filename)
    if not os.path.exists(report_path):
        return JSONResponse(content="File not Found",status_code=404)

    return FileResponse(report_path, filename=filename, media_type="application/json-seq")

@app.delete("/report")
def delete_report(
    *,
    filename: str = 'report.json',
    http_request: Request
) -> Any:
    if not valid_filename(filename):
        return JSONResponse(content=f"Invalid filename",status_code=404)

    try:
        os.remove("../shared/" + filename)
    except FileNotFoundError:
        return JSONResponse(content="File not Found",status_code=404)

    return JSONResponse(content="Report deleted",status_code=200)
