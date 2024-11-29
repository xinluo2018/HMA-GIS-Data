import numpy as np
import cartopy.crs as ccrs

def add_scale_bar(ax, length=None, tmc = ccrs.Mercator(), location=(0.5, 0.05), linewidth=3):
    """
    params:
        ax: the axes to draw the scalebar on.
        length: the length of the scalebar in km.
        tmc: the coordinate system that the scalebar is in.
        location: center of the scalebar in axis coordinates. 
                    (e.g. 0.5 is the middle of the plot)
        linewidth: the thickness of the scalebar.
    """    
    #Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(tmc)
    #Turn the specified scalebar location into coordinates in metres
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]
    text_space = (y1 - y0) * 0.02
    #Calculate a scale bar length if none has been given
    #(Theres probably a more pythonic way of rounding the number but this works)
    if not length: 
        length = (x1 - x0) / 5000 # in km
        ndim = int(np.floor(np.log10(length))) #number of digits in number
        length = round(length, -ndim) #round to 1sf
        #Returns numbers starting with the list
        def scale_number(x):
            if str(x)[0] in ['1', '2', '5']: return int(x)        
            else: return scale_number(x - 10 ** ndim)
        length = scale_number(length) 

    #Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbx - length * 500, sbx + length * 500]
    #Plot the scalebar
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='k', linewidth=linewidth)
    #Plot the scalebar label
    ax.text(sbx, sby+text_space, str(length) + ' km', transform=tmc,
            horizontalalignment='center', verticalalignment='bottom')
