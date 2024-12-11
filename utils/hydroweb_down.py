help_message = """
Download products from your hydroweb.next projects (https://hydroweb.next.theia-land.fr) using the py-hydroweb lib (https://pypi.org/project/py-hydroweb/)
This script is an example tuned for your last hydroweb.next project but feel free to adapt it for future requests.
Follow these steps:
1. If not already done, install py-hydroweb latest version using `pip install -U py-hydroweb` or `conda install py-hydroweb` (WARNING: python >= 3.8 is required)
2a. Generate an API-Key from hydroweb.next portal in your user settings
2b. Carefully store your API-Key (2 options):
- either in an environment variable `export HYDROWEB_API_KEY="<your_key_here>"`
- or in below script by replacing <your_key_here>
3. You can change download directory by adding an `output_folder` parameter when calling `submit_and_download_zip` (see below). By default, current path is used.
4. You are all set, run this script `python download_script.py`

For more documentation about how to use the py-hydroweb lib, please refer to https://pypi.org/project/py-hydroweb/.
"""

try:
    import logging
    import sys
    import py_hydroweb
except ImportError:
    print(help_message)
    exit(1)

# Set log config
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Create a client
#  - either using the API-Key environment variable
client: py_hydroweb.Client = py_hydroweb.Client("https://hydroweb.next.theia-land.fr/api")
#  - or explicitly giving API-Key (comment line above and uncomment line below)
# client: py_hydroweb.Client = py_hydroweb.Client("https://hydroweb.next.theia-land.fr/api", api_key="<your_key_here>")

# Initiate a new download basket (input the name you want here)
basket: py_hydroweb.DownloadBasket = py_hydroweb.DownloadBasket("my_download_basket")

# Add collections in our basket
basket.add_collection("HYDROWEB_LAKES_RESEARCH", bbox=[-340.3125, -87.8374, 344.17969, 87.8374])

# Do download (input the archive name you want here, and optionally an output folder)
downloaded_zip_path: str = client.submit_and_download_zip(
    basket, zip_filename="test_template_example_short.zip" #, output_folder = "<change_me>"
)


