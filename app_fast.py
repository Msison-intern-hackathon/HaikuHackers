from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Dict, Any
from datetime import datetime
import os



app = FastAPI()
#app.mount("/", StaticFiles(directory="mini_site"), name= "static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)


class QuickCapture(BaseModel):
    pass

@app.post("/hack")
async def run_script(quick_capture: Dict):
    print(quick_capture)
    #os.popen("")