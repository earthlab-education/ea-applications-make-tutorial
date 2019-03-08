#!/usr/bin/env python

"""Calculate zonal statistics for an input raster and polygon shapefile"""
import os
import sys
import geopandas as gpd
import rasterio as rio
import rasterstats as rs

def cat_zonal_stats(polygon, raster):
    """Calculate zonal statistics for an input raster with categorical values 
    and polygon shapefile of the same coordinate reference system. 
    
    Parameters
    ----------
    polygon : shapefile
        A shapefile containing the boundaries (i.e. zones) used to calculate
        the summary statistics. 
    
    raster: raster file
        A raster file containing labeled categories to be summarized.     
        
    Returns
    ----------
    summary_df : GeoDataFrame
        A GeoDataFrame containing the attributes of the shapefile and 
        a column with total number of pixels for each category in the raster. 
    """
    with rio.open(raster) as src:
        src_data = src.read()
        src_meta = src.profile

        if src_data.shape[0] == 1:
            src_data = src_data.squeeze()

    # Code example for categorical data
        # https://pythonhosted.org/rasterstats/manual.html#working-with-categorical-rasters
    # Metadata for land cover categories
        # https://www.mrlc.gov/sites/default/files/metadata/nlcd_2011_landcover_2011_edition_2014_10_10.xml
    #cmap = {1.0: 'label_1', 2.0: 'label_2', 3.0: 'label_3'}
    summary = rs.zonal_stats(polygon,
                             src_data,
                             affine=src_meta['transform'],
                             geojson_out=True,
                             copy_properties=True,
                             categorical=True,
                             nodata = -999999)
                                    
                             # Include to use labels from cmap dictionary
                             #category_map=cmap)

    summary_df = gpd.GeoDataFrame.from_features(summary)

    return(summary_df)


# Below is not executed if this file is imported as module
if __name__ == '__main__':
    
    # sys.argv are input variables from command in terminal
    # sys.argv[0] is the script name
    polygon = sys.argv[1]
    raster = sys.argv[2]
    
    df = cat_zonal_stats(polygon, raster)
    
    # Uncomment lines below to exclude geometry column in exported csv
    #out_columns = df.columns.tolist()
    #out_columns.remove("geometry")

    outfile = os.path.join(os.getcwd(), "output", "zonal_stats.csv")
    
    with open(outfile, 'w') as dst:
            df.to_csv(dst, sep=',', encoding='utf-8', header= True, index = False)
            
            #df.to_csv(dst, sep=',', columns = out_columns, encoding='utf-8', header= True, index = False)
            