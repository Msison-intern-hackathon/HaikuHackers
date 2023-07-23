from fastapi import FastAPI, 
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel, Field
from typing import Dict, Any
from Hackathon_garbage_detection import classify
from trace_downhill_auto import trace_downhill
import os
import arcgis, arcpy
from typing import List, Optional
from classdefs import Root

app = FastAPI()
#app.mount("/", StaticFiles(directory="mini_site"), name= "static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.post("/hack")
async def run_script(quick_capture: Root):
    apiKey = "AAPKa37c22c6b6c341fcb6ae778e549ce9a7mS25Zx51QFR2KwEaovAIf_Hcv9A73_d-D0464D3E_bFFowZXMK57ksjrzPNh4ofc"
    gis = GIS(apiKey)

    ###------ Classification ------###
    classified = classify(quick_capture[0].AttachmentInfo[0].photo.url)    

    # Add field and value to attribute table of our feature layer
    feature_layer_item = gis.content.get('00d344921b0247ea9ddd9b79821780c5')
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


