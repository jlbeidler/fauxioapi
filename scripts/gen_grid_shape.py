#!/usr/bin/env python
# Example script for fauxioapi to create a shapefile of the grid cells in a domain

import ogr
import osr
import fauxioapi as io

# Path to grid description file
griddesc = '../data/griddesc.txt'
# List of gridding domains to run
grids = ['9AK2',]

def draw_grid(grid_name, grid):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.CreateDataSource('%s.shp' %grid_name)
    srs = osr.SpatialReference()
    srs.ImportFromProj4(grid.proj4())
    with open('%s.pj4' %grid_name, 'w') as pj4:
        pj4.write('%s\n' %grid.proj4())
    layer = data_source.CreateLayer('cells', srs, ogr.wkbPolygon)
    field_name = ogr.FieldDefn('cellid', ogr.OFTString)
    col_len = len(str(grid.NCOLS))
    row_len = len(str(grid.NROWS))
    field_name.SetWidth(col_len+row_len+1)
    layer.CreateField(field_name)
    for col in range(grid.NCOLS):
        for row in range(grid.NROWS):
            feature = ogr.Feature(layer.GetLayerDefn())
            cellid = str(col+1).rjust(col_len,'0') + '!' + str(row+1).rjust(row_len,'0')
            feature.SetField('cellid', cellid)
            poly = []
            x = (col * grid.XCELL) + grid.XORIG
            y = (row * grid.YCELL) + grid.YORIG
            poly.append('%s %s' %(x,y))
            x += grid.XCELL
            poly.append('%s %s' %(x,y))
            y += grid.YCELL
            poly.append('%s %s' %(x,y))
            x -= grid.XCELL
            poly.append('%s %s' %(x,y))
            y -= grid.YCELL
            poly.append('%s %s' %(x,y))
            poly = ogr.CreateGeometryFromWkt('POLYGON((%s))' %','.join(poly))
            feature.SetGeometry(poly)
            layer.CreateFeature(feature)
            feature = None
    data_source = None

for grid_name in grids:
   grid = io.Grid(grid_name, griddesc)
   draw_grid(grid_name, grid) 

