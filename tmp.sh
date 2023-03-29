  
cd /Users/luo/Library/CloudStorage/OneDrive-Personal/GitHub/High-Moutain-Asia-GIS-Data

### download srtm dem data
for left in {65..107}
do
  for bottom in {24..46}
  do
  path_save=srtm_${left}_${battom}
  right=$(expr $left + 1)
  up=$(expr $bottom + 1)
  path_save=SRTM_GL3_${left}_${bottom}.tif
  echo $path_save
  python utils/get_dem.py SRTMGL1_E --bounds $left $right $bottom $up --out dem/tiles/$path_save
  done
done

