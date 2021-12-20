import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random
import mistune
from dotenv import load_dotenv
from services import mapit
from typing import Optional
import sys

class Map(BaseModel):
    x: float
    y: float
    name: Optional[str] = None
    dilate: Optional[int] = 100
    figx: Optional[int] = 10
    figy: Optional[int] = 10
    radius: Optional[int] = 500
    backgroundFc: Optional[str] = '#E4FBFF'
    backgroundEc: Optional[str] = '#E4FBFF'
    greenFc: Optional[str] = '#CCFFBD'
    greenEc: Optional[str] = '#7ECA9C'
    waterFc: Optional[str] = '#a8e1e6' 
    waterEc: Optional[str] = '#2F3737'
    streetsFc: Optional[str] = '#C400FF'
    streetsEc: Optional[str] = '#FF67E7'
    buildingA: Optional[str] = '#7C83FD'
    buildingB: Optional[str] = '#78DEC7'
    buildingEc: Optional[str] = '#480032'
    textColor: Optional[str] = '#2F3737'


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/favicon.ico")
async def favicon(): return FileResponse('./static/favicon.ico')

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.get("/advanced")
async def advanced(request: Request):
  return templates.TemplateResponse("advanced.html", {"request": request})

@app.get("/examples")
async def examples(request: Request):
  return templates.TemplateResponse("examples.html", {"request": request})

@app.get("/documentation")
async def documentation(request: Request):
    with open('README.md', 'r') as readme:
        readme_content = readme.read()
        return templates.TemplateResponse("documentation.html", {
            "request": request,
            "readme": mistune.html(readme_content)
        })

@app.get('/api/')
async def api(x: Optional[float] = None, y: Optional[float] = None, name: Optional[str] = None, theme_num: Optional[int] = 0):
    report = mapit.get_image(x, y, name, theme_num)

    return report

@app.post('/advanced_api/')
async def advanced_api(map: Map):
    map_dict = map.dict()
    report = mapit.get_advanced_image(
      map.x,
      map.y,
      map.name,
      map.dilate,
      map.figx,
      map.figy,
      map.radius,
      map.backgroundFc,
      map.backgroundEc,
      map.greenFc,
      map.greenEc,
      map.waterFc,
      map.waterEc,
      map.streetsFc,
      map.streetsEc,
      map.buildingA,
      map.buildingB,
      map.buildingEc,
      map.textColor)
    return report

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', "8000")))
