## reference: https://github.com/uw-cryo/asp-binder-demo/blob/master/asp_binder_utils.py
## author: xin luo
## creat: 2022.3.18 # modify: xxxx
## des: download dem data from OpenTopography World DEM
## !!! The user should login OpenTopography firstly, because the dem download is requried.

import os
import sys
import requests
import argparse

def get_dem(demtype, bounds, apikey='7f97d1b49489d7c0e346b085772aef3c', path_out=None):
    """
    download a DEM of choice from OpenTopography World DEM
    Parameters
        demtype: str, type of DEM to fetch (e.g., COP30, SRTMGL1 (Vertical Coordinates: EGM96), SRTMGL1_E(SRTMGL1 Ellipsoidal (Vertical Coordinates: WGS84)), SRTMGL3 etc)
        bounds: list, geographic aoi extent in format (minlon, maxlon, minlat, maxlat)
        apikey: str, opentopography api key(obtain from: https://opentopography.org/)        
        path_out: str, path to output filename        
    """

    base_url="https://portal.opentopography.org/API/globaldem?demtype={}&west={}&east={}&south={}&north={}&outputFormat=GTiff&API_Key={}"
    if path_out is None:
        path_out = '{}.tif'.format(demtype)
    if not os.path.exists(path_out):
        #Prepare API request url
        url = base_url.format(demtype, *bounds, apikey)
        print(url)
        #Get
        response = requests.get(url)
        #Check for 200
        if response.ok:
            print ('DEM data have been downloaded!')
        else:
            print ('Query failed')
            sys.exit()
        #Write to disk
        open(path_out, 'wb').write(response.content)
    else:
        print('!!Output file has been existed.')


def get_args():

    """ Get command-line arguments. """
    parser = argparse.ArgumentParser(
            description='download dem with the given extent')
    parser.add_argument(
            'demtype', metavar='demtype', type=str, nargs='+',
            help='type of DEM to fetch (e.g., COP30, SRTMGL1, SRTMGL1_E')
    parser.add_argument(
            '--bounds', metavar=('w','e','s','n'), type=float, nargs=4,
            help=('region for data download'))
    parser.add_argument(
            '--apikey', metavar='apikey', type=str, nargs='+',
            help=('opentopography api key(obtain from: https://opentopography.org/)'),
            default=['7f97d1b49489d7c0e346b085772aef3c'])
    parser.add_argument(
            '--out', metavar='out', type=str, nargs='+',
            help=('path to output filename'),
            default=[None])

    return parser.parse_args()


if __name__ == '__main__':

    # extract arguments 
    args = get_args()
    demtype = args.demtype[0]
    bounds = args.bounds
    apikey = args.apikey[0]
    out = args.out[0]
    get_dem(demtype, bounds, apikey, out)


