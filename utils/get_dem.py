## author: xin luo
## creat: 2023.12.20  # modify: xxxx
## des: download dem data from OpenTopography World DEM


import os
import requests

def get_dem(demtype, bounds, path_out=None):
    """
    download a DEM of choice from OpenTopography World DEM
    !!note: API have maximum rate limit (500 API calls/24hrs).
    Parameters
        demtype: str, type of DEM to fetch (e.g., COP30, SRTMGL1 (Vertical Coordinates: EGM96), SRTMGL1_E(SRTMGL1 Ellipsoidal (Vertical Coordinates: WGS84)), SRTMGL3 etc)
        bounds: list, geographic aoi extent in format (minlon, maxlon, minlat, maxlat)
        apikey: str, opentopography api key(obtain from: https://opentopography.org/)        
        path_out: str, path to output filename        
    """
    url="https://portal.opentopography.org/API/globaldem?demtype={}&west={}&east={}&south={}&north={}&outputFormat=GTiff&API_Key={}"
    apikey='7f97d1b49489d7c0e346b085772aef3c'

    while path_out is None:
        path_out = '{}.tif'.format(demtype)
    while os.path.exists(path_out):
        print('!!Output file has been existed.')
        return
    #Prepare API request url
    url = url.format(demtype, *bounds, apikey)
    #  ----- download -----  ##
    response = requests.get(url)
    open(path_out, 'wb').write(response.content)

