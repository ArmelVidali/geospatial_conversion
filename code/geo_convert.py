import geopandas as gpd
import concurrent.futures
import os


# Import data, convert and optionnaly reproject & divide dataset by unique values for a given field
def import_data(gdf, path, output_format, target_crs=False, divide_dataset=False, field=None, extract_invalid_geometry=False):

    print("... Extracting values ... ")
    if target_crs:
        gdf = gdf.to_crs(target_crs)
    path = path.replace("\\", "/")
    file_name = path[path.rfind("/")+1:path.rfind(".")]

    output_path = path[:path.rfind(
        "/")] + "/geoconvert_to_" + str(output_format) + "/"

    if divide_dataset == False:
        output_file_path = f"{output_path}/{file_name}.{output_format}"

        if os.path.isdir(output_path):
            if output_format == "csv":
                gdf.to_csv(output_file_path)
            else:
                gdf.to_file(output_file_path)
        else:
            os.mkdir(output_path)
            if output_format == "csv":
                gdf.to_csv(output_file_path)
            else:
                gdf.to_file(output_file_path)
    else:
        for value in gdf[field].unique():
            output_file_path = f"{output_path}/{file_name}_{field}_{str(value)}.{output_format}"

            # export one file per unique value for the selected field
            output_gdf = gdf[gdf[field] == value]

            if not output_gdf.empty:
                if os.path.isdir(output_path):
                    if output_format == "csv":
                        output_gdf.to_csv(output_file_path)
                    else:
                        output_gdf.to_file(output_file_path)
                else:
                    os.mkdir(output_path)
                    if output_format == "csv":
                        output_gdf.to_csv(output_file_path)
                    else:
                        output_gdf.to_file(output_file_path)

    print("-- File converted --")
    return [1, output_path]
