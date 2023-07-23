from arcgis.gis import GIS
import arcpy
from arcgis.geometry import Point
from arcgis.features import FeatureSet, Feature


def trace_downhill():
    apiKey = "AAPKa37c22c6b6c341fcb6ae778e549ce9a7mS25Zx51QFR2KwEaovAIf_Hcv9A73_d-D0464D3E_bFFowZXMK57ksjrzPNh4ofc"
    gis = GIS(apiKey)
    feature_layer_item = gis.content.get('92e5e33078b9459f898741cc94c057fc') # ID of feature layer

    feature_layer = feature_layer_item.layers[0]
    print(feature_layer)

    #Get most recently added feature
    query_result = feature_layer.query(where='1=1', order_by_fields='Date and time of sighting', out_fields='*', return_geometry=True, return_all_records=False, result_record_count=1)
    most_recent_feature = query_result.sdf
    feature = most_recent_feature.SHAPE[0]
    input_points = [
        {
            "geometry": {
                "x": feature.x,
                "y": feature.y,
                "spatialReference": {
                    "wkid": 32618,
                    "latestWkid": 32618
                }
            },
            "attributes": {
                "Name": "Most Recent Point",
                "Type": "Start"
            }
        }]

    input_feature_set = FeatureSet(input_points)

    polyline = arcpy.agolservices.TraceDownstream(
        InputPoints=input_feature_set,
        PointIDField="",
        DataSourceResolution="FINEST",
        Generalize=False
    )

    add_result = feature_layer.edit_features(adds=FeatureSet(features=Feature(polyline)))
