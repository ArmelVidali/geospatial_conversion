import geopandas as gpd
import os

def import_data(path, output_format =False, target_crs = False):
    gdf = gpd.read_file(path)
    if target_crs : 
        gdf = gdf.to_crs(target_crs)
    
    output_path = path[:path.rfind("/")] + "/geoconvert_to_" + str(output_format)  + path[path.rfind("/"):path.rfind(".")] + "." + output_format
    print("input path",path)
    print(output_path)


import_data("C:/M1_GEOMATIQUE/data utile SIG/BDTOPO/75 BDTOPO/BDTOPO/1_DONNEES_LIVRAISON_2022-09-00418/BDT_3-0_SHP_LAMB93_D075-ED2022-09-15/ADMINISTRATIF/REGION.shp", output_format= "shp",target_crs=2154)

