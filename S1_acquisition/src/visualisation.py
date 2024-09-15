import numpy as np
import geopandas as gpd
import cartopy as cart
import matplotlib as mpl
import cartopy.crs as ccrs
import cmcrameri.cm as cmc
import matplotlib
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from matplotlib.colors import ListedColormap
from typing import Union
from pathlib import Path

from S1_acquisition.src.file_read import find_open_kml
from S1_acquisition.src.misc.utils import find_number_days_df, find_start_date_df

plt.rcParams.update({'font.size': 10, 'font.weight' : 'bold'})

path_relative_dir = Path(__file__).parents[1]


def visualize_kml(gdf: gpd.geopandas.geodataframe.GeoDataFrame, 
                  date_column: str = "begin",
                  bounds: list[float, float, float, float]=[-180., 180., -90., 90.],
                  fig_title: str = "Sentinel-1 acquisition plan",
                  crs=ccrs.PlateCarree(),
                  kwargs_plot: dict = dict(),
                  kwargs_cbar: dict = dict(),
                  kwargs_title: dict = dict(),
                  ) -> matplotlib.figure.Figure: 


    N_days = find_number_days_df(df=gdf, date_column=date_column)
    df_start = find_start_date_df(df=gdf, date_column=date_column)

    kwargs_cbar_temp = dict(
        orientation='horizontal', 
        label= f"{str(df_start.strftime('%Y-%m-%d'))} + n days", 
        pad=0.1
        )
    
    kwargs_plot_temp = dict(
          subplot_kw = {'projection': crs},
          figsize = (8, 5),
    )

    kwargs_title_temp = dict(
          pad=20,
          fontsize=14,
          fontweight="bold",
    )
    
    _kwargs_plot= {**kwargs_plot_temp, **kwargs_plot}
    _kwargs_cbar= {**kwargs_cbar_temp, **kwargs_cbar}
    _kwargs_title= {**kwargs_cbar_temp, **kwargs_title}

    cmap_steps = N_days + 1
    colormap = cmc.batlow
    discrete_cmap = colormap(np.linspace(0, 1, cmap_steps))
    cmap = ListedColormap(discrete_cmap)
    norm = mpl.colors.Normalize(vmin=0, vmax=N_days)

    fig, ax= plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True, **_kwargs_plot)
    ax.set_extent(bounds)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75)

    for i in range(len(gdf.geometry)):
            
            # select individual 
            acquisition = gdf.iloc[i]
            acq_geom = acquisition.geometry
            acq_day = (acquisition.begin-df_start).days

            ax.add_geometries([acq_geom], crs=crs, edgecolor='black', alpha=0.5, color = cmap.colors[acq_day])

    ax.add_feature(cart.feature.LAND,zorder=0, edgecolor='k')
    ax.gridlines(crs=crs, draw_labels=True,linewidth=2, color='gray', alpha=0.5, linestyle='--')
    ax.set_facecolor('silver')

    cbar = fig.colorbar(mappable=mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
                 ax=ax,
                 **_kwargs_cbar
                 )
    ax.set_title(fig_title, **kwargs_title_temp)
    # cbar.ax.set_yticklabels(cbar_labels)
    # cbar.ax.tick_params(labelsize=labelsize) 

    return fig


def save_figure(fig: matplotlib.figure.Figure,
                fname: Union[str: None] = None,
                **kwargs_saving
                ) -> None: 
    
    if fname == None:
        path_relative_dir = Path(__file__).parents[1]
        directory_figures = Path.joinpath(path_relative_dir, "figures") 
        directory_figures.mkdir(parents=True, exist_ok=True)
        fname = Path.joinpath(directory_figures, "S1_acquisition_plan") 

    fig.savefig(fname=fname, **kwargs_saving)

    return


def plot_save_kml(gdf, **kwargs) -> matplotlib.figure.Figure: 
     
    fig = visualize_kml(gdf, **kwargs)
    save_figure(fig)

    return fig


if __name__ == "__main__":
        
    gdf, _ = find_open_kml()

    fig = visualize_kml(gdf=gdf)

    save_figure(fig=fig)

    
    
    
    