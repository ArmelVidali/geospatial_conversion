import geopandas as gpd
import os

def import_data(path, output_format =False, target_crs = False):
    try : 
        gdf = gpd.read_file(path)
    
        if target_crs : 
            gdf = gdf.to_crs(target_crs)
        path = path.replace("\\", "/")
        file_name = path[path.rfind("/")+1:path.rfind(".")]
            
        output_path = path[:path.rfind("/")] + "/geoconvert_to_" + str(output_format) + "/"

    
        
        if os.path.isdir(output_path):
            if output_format == "csv" : 
                gdf.to_csv(output_path + "/" + file_name + "." + output_format)
            else : 
                gdf.to_file(output_path + "/" + file_name + "." + output_format)
        else:
            os.mkdir(output_path) 
            if output_format == "csv" : 
                gdf.to_csv(output_path + "/" + file_name + "." + output_format)
            else : 
                gdf.to_file(output_path + "/" + file_name + "." + output_format)
        return [1, output_path]
    except :
        return[0, ""]

    
            

