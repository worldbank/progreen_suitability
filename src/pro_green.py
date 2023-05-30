import sys, os, io, math, importlib
import rasterio, richdem
import boto3

import numpy as np
import pandas as pd
import geopandas as gpd

from botocore import UNSIGNED
from botocore.config import Config

from osgeo import gdal 
from dem_stitcher import stitch_dem

from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension
from pystac_client.client import Client

sys.path.insert(0, "/home/wb411133/Code/gostrocks/src")

import GOSTRocks.rasterMisc as rMisc
import GOSTRocks.mapMisc as mapMisc

def re_classify(array, defs, no_data):
    ''' re-classify array based on categories in defs
    
    :param array: numpy array of desired data
    :param defs: dictionary defining re-classification
    :param no_data: value to set no_data
    '''
    mask = np.zeros(array.shape) + 1
    if defs['max_val']: max_val = defs['max_val']
    else: max_val = array.max()
    if defs['min_val']: min_val = defs['min_val']
    else: min_val = array.min()
    
    if defs['min_val']: # set everything below this value to no_data
        mask[array < defs['min_val']] = 0
    if defs['max_val']:
        mask[array > defs['max_val']] = 0        
    
    if defs['classifier'] == 'binary': # only return the mask, not additional value
        return(mask.astype(int))    
    if defs['classifier'] == 'linear-ascending': # scale ascending
        array = (array - min_val)/(max_val - min_val) * 100
        array = array.astype(int)
    if defs['classifier'] == 'linear-descending': # scale descending
        array = (array - min_val)/(max_val - min_val) * 100
        array = abs(array - 100)        
    if defs['classifier'] == 'ranges': # map good and bad ranges
        array = np.digitize(array, defs['ranges'])
        for i in list(range(len(defs['range_definition']))):
            array[array == i] = defs['range_definition'][i]
    if defs['classifier'] == 'convert': #Map good and bad vals
        map_array = array.copy()
        for key, value in defs['map_vals'].items():
            array[map_array == key] = value
    
    array = array.astype(int)
    mask = mask.astype(int)
    return(array * mask)

def clip_and_classify(global_file, bounds, defs):
    inR = rasterio.open(global_file)
    local_d, profile = rMisc.clipRaster(inR, bounds, crop=False)
    local_d = re_classify(local_d, defs, profile['nodata'])
    return([local_d, profile])

def write_file(d,p,f):
    with rasterio.open(f, 'w', **p) as out:
        out.write(d)

        
def scale_write(data, profile, template_r, out_file=''):
    ''' Scale the data to a template raster, optionally write output
    
    :param data: numpy array of input data to scale
    :param profile: rasterio metadata describing data
    :param template_r: rasterio object for raster to match to
    :param out_file: optional output file to create
    :return: updated data and profile
    :rtype: list of [data, profile]
    '''
    with rMisc.create_rasterio_inmemory(profile, data) as in_raster:
        if out_file != '':
            data, profile = rMisc.standardizeInputRasters(in_raster, template_r, out_file)
        else:
            data, profile = rMisc.standardizeInputRasters(in_raster, template_r)
    return([data, profile])