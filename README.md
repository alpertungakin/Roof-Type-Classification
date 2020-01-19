# Roof-Type-Classification
A Python implementation to classify 3 main roof types that are hipped, gabled and flat.

The network is trained with [Azure Custom Vision Service](https://www.customvision.ai) then exported as .pb file (model.pb). 
Test and training images are prepared by the script PrepareData.py. It needs shapefile of building footprints and aerial image of study field.
Sample images are obtained from: 
https://figshare.com/articles/Atlanta_Georgia_-_Aerial_imagery_object_identification_dataset_for_building_and_road_detection_and_building_height_estimation/3504308
https://figshare.com/articles/Washington_DC_-_Aerial_imagery_object_identification_dataset_for_building_and_road_detection_and_building_height_estimation/3504320
