#! /usr/bin/python

import psycopg2
import sys
from subprocess import call, Popen

sys.path.append("../var")
try:
    from Config import *
    from datetime import timedelta
    from datetime import datetime    
except:
    print "Cannot find local settings file 'Config.py'.  You need to create a Config.py file that contains"
    print "settings appropriate for this copy of the LandsatFACT project.  You can use the file 'Config.tpl.py'"
    print "as a starting point --- make a copy of that file called 'Config.py', and edit appropriately."
    exit(-1)
	
conn_string = (POSTGIS_CONNECTION_STRING)
 
# print the connection string we will use to connect
print "Connecting to database\n	->%s" % (conn_string)
 
# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)
 
print "Connected!\n"

# conn.cursor will return a cursor object, you can use this cursor to perform queries
ndvi_cur = conn.cursor()

#Selects the column that you want
#From Inputs will be replaced with the appropriate view 
ndvi_cur.execute("SELECT * FROM vw_latest_quads_ndvi;")

#Use this view to create an inital mosaic. You may need to change the # of days in teh view.
#ndvi_cur.execute("SELECT * FROM vw_initial_mosaic_ndvi;")


#Create empty string 
ndvi = ' ' 

#loop through data with cursor and attach the data to the empty parameters string
for data in ndvi_cur:
	ndvi += data[0] + ' ' 
	print data
print ndvi

cmd_ndvi = r'gdalwarp -multi -wm 500 --config GDAL_CACHEMAX 1000 -t_srs EPSG:4269 -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=YES -srcnodata -128 -dstnodata -128 /lsfdata/products/mosaics/southeast_mosaic_ndvi.tif' + ndvi + "/lsfdata/products/mosaics/temp/southeast_mosaic_ndvi.tif"

#Use this command to create a new initial mosaic
#cmd_ndvi = r'gdalwarp -wm 2000 --config GDAL_CACHEMAX 2000 -t_srs EPSG:4269 -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=YES -srcnodata -128 -dstnodata -128' + ndvi + "/lsfdata/products/mosaics/temp/southeast_mosaic_ndvi.tif"

# print cmd_ndvi

#call gdal command and insert your string parameter	
#Popen(cmd_ndvi, shell = True)
call(cmd_ndvi, shell = True)



# Make the changes to the database persistent
conn.commit()

# Close communication with the database
ndvi_cur.close()