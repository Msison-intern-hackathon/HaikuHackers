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
import arcgis, arcpy
from io import BytesIO
from PIL import Image
from Hackathon_garbage_detection import classify
from trace_downhill_auto import trace_downhill

app = FastAPI()
#app.mount("/", StaticFiles(directory="mini_site"), name= "static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

apiKey = "AAPKa37c22c6b6c341fcb6ae778e549ce9a7mS25Zx51QFR2KwEaovAIf_Hcv9A73_d-D0464D3E_bFFowZXMK57ksjrzPNh4ofc"
gis = GIS(apiKey)

class QuickCapture(BaseModel):
    pass

@app.post("/hack")
async def run_script(quick_capture: Dict):
    
    ###------ Classification ------###
    classified = classify(quick_capture["URL"])    

    # Add field and value to attribute table 
    feature_layer_item = gis.content.get('92e5e33078b9459f898741cc94c057fc')
    feature_layer = FeatureLayer.fromitem(feature_layer_item)
    field = {
        'name': 'Recyclable',
        'type': 'esriFieldTypeString',
        'length': 100
    }
    feature_layer.manager.add_to_definition({'fields': [field]})
    features = feature_layer.query(where='1=1', order_by_fields='Date and time of sighting', out_fields='*', return_geometry=True, return_all_records=False, result_record_count=1)
    
    features[0].attributes['Recyclable'] = classified    
    feature_layer.edit_features(updates=features)

    ###------ TraceDownhill Automation ------###
    trace_downhill()


