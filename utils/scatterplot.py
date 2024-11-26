import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap

# Scatterplot
def scatterplot(x, y, size, color, color_range=[-1.5, -1, -0.5],
                cmap_dhdt=plt.cm.get_cmap('Reds').reversed(), color_min=-1.5, color_max=0):
  cmap_dem = LinearSegmentedColormap.from_list('linear color', ["DimGray", "white"])
  fig = plt.figure(figsize=(10,6))
  ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator(central_longitude=88.5))
  ax.set_extent([91, 99, 27.3, 32])

  ## 1. Tibeteau southeast boundary
  shp_fea = cfeature.ShapelyFeature(Reader(path_setp_vec).geometries(), \
                        crs=ccrs.PlateCarree(), edgecolor='lightgreen', linewidth=1, facecolor='none')

  ax.add_feature(shp_fea, zorder=0)
  scatter = ax.scatter(
      x = x,
      y = y,
      s = size,
      c = color,
      cmap=cmap_dhdt,
      alpha=1, 
      linewidth=2,
      vmin=color_min,
      vmax=color_max,
      transform=ccrs.PlateCarree(),
      )
  ax.gridlines(draw_labels=True, linewidth=1, alpha=1, zorder=1, color='grey', linestyle='--')

  # produce a legend with the unique colors from the scatter
  handles, labels = scatter.legend_elements(prop="colors", num=color_range)
  legend_color = ax.legend(handles, labels, loc="lower left", title="dh/dt \n($m/yr$)",\
                              facecolor='white', edgecolor='black', borderpad=0.8, labelspacing=1.25, markerscale=2)

  # produce a legend with a cross-section of sizes from the scatter
  handles, labels = scatter.legend_elements(prop="sizes", num=[100, 300, 500], alpha=0.2)
  print(labels)
  legend_glacier_area = ax.legend(handles, [100, 300, 500], loc="lower left", title="Glacier area\n     (${km^2}$)", \
                                      edgecolor='black', borderpad = 0.8, labelspacing=1.2, bbox_to_anchor=(0.15, 0.))

  ax.add_artist(legend_color)
  ax.add_artist(legend_glacier_area)
  return ax
