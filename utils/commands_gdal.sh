#! /bin/bath
## author: xin luo
## create: 2022.3.18; modify: 2022.8.9
## des: some example for fast processing of the remote sensing image.
## main gdal tools: gdal_translate, gdal_merge.py, gdalwarp(for reprojection)...

##### shell style
## -- gdal_translate
### ------ downsampling/resize ------ 
gdal_translate -outsize 20% 20% -r average -co COMPRESS=LZW $path_in $path_out 
## the -tr value georeferenced units, degree or meter
gdal_translate -tr 1000 1000 -r average -co COMPRESS=LZW $path_in $path_out 

### ------ mosaic ------ 
## gdal_merge.py: the latter image overlap the previous image
## '-n -999' means igore value of -999 during image mosaic
gdal_merge.py -init 0 -n -999 -co COMPRESS=LZW -o $path_out $path_in_1 $path_in_2 $path_in_3
## below is a method to keep the nodata values during mosaic.
gdal_merge.py -n -999 -a_nodata -999 -co COMPRESS=LZW -o $path_out $path_in_1 $path_in_2 $path_in_3

### ------ subset by bounds------ 
# extent: str(ulx) str(uly) str(lrx) str(lry), e.g., extent='72 38 84 34'
gdal_translate -projwin $extent -co COMPRESS=LZW $path_in $path_out

### ------ subset by .shp file------ 
gdalwarp -co COMPRESS=LZW -cutline $path_shp -crop_to_cutline $path_input $path_output

### ------ resize to specific width and height (resample) ------ 
gdalwarp -co COMPRESS=LZW -ts $width $height -r bilinear $path_input $path_output

### --------- band math ----------
gdal_calc.py -A $path_img --A_band=1 -B $path_img --B_band=2 \
                --outfile=$path_output --calc="(A*(abs(B-A)<100)-999*(abs(B-A)>100))"  # band math.

### ------ reprojection ------
## 1) wgs84 to utm projection
gdalwarp  -overwrite -s_srs EPSG:4326 -t_srs EPSG:32644 -tr 30 30 -r cubic -co COMPRESS=LZW -co TILED=YES input.tif output.tif 
## 2) wgs84 to wgs84/egm2008
# gdalwarp  -s_srs "+proj=longlat +datum=WGS84 +no_def" -t_srs "+proj=longlat +datum=WGS84 +no_defs +geoidgrids=egm08_25.gtx" input.tif output.tif
# !gdalwarp -overwrite -s_srs EPSG:4326 -t_srs EPSG:4326+3855 input.tif output.tif
## 3) wgs84/egm96 to wgs84/egm2008
# !gdalwarp  -s_srs "+proj=longlat +datum=WGS84 +geoidgrids=egm96_15.gtx" -t_srs "+proj=longlat +datum=WGS84 +no_defs +geoidgrids=egm08_25.gtx" input.tif output.tif
## 4) wgs84/egm96 to wgs84
# !gdalwarp  -s_srs "+proj=longlat +datum=WGS84 +geoidgrids=egm96_15.gtx" -t_srs "+proj=longlat +datum=WGS84 +no_defs" input.tif output.tif

##### python style
```python
import os
## extent = 'str(ulx) str(uly) str(lrx) str(lry)'
command = 'gdal_translate -projwin ' + extent + ' -co COMPRESS=LZW ' + path_input + ' ' + path_output
print(os.popen(command).read())
```