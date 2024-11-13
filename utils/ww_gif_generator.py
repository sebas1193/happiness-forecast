import geopandas as gpd
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

def create_happiness_gif():
    # Load geospatial data from zip file
    world = gpd.read_file('../utils/ne_110m_admin_0_countries.zip')
    
    # Load the happiness dataset
    df = pd.read_csv('../data/happiness_dataset_merged.csv')
    
    # Create a list of unique years in the happiness DataFrame
    years = sorted(df['year'].unique())
    
    # Calculate the full range of 'happiness_score' for all years with a small margin
    vmin = df['happiness_score'].min() * 0.95  # Add a margin to smooth the range
    vmax = df['happiness_score'].max() * 1.05
    
    # List to store paths of temporary images
    image_files = []
    
    # Create interpolated images between years
    num_interpolations = 10  # Increase the number of intermediate frames to smooth the transition
    
    for i in range(len(years) - 1):
        year_start = years[i]
        year_end = years[i + 1]
        
        # Data for start and end year
        df_start = df[df['year'] == year_start]
        df_end = df[df['year'] == year_end]
        
        # Join data from both years with the shapefile
        world_start = world.merge(df_start, left_on='ISO_A2', right_on='ISO2', how='left')
        world_end = world.merge(df_end, left_on='ISO_A2', right_on='ISO2', how='left')
        
        for j in range(num_interpolations + 1):
            # Interpolate 'happiness_score' for each country smoothly
            interpolation_factor = j / num_interpolations
            world_interpolated = world_start.copy()
            world_interpolated['happiness_score'] = (1 - interpolation_factor) * world_start['happiness_score'] + \
                                                    interpolation_factor * world_end['happiness_score']
            
            # Create heat map for the interpolated frame
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            world.boundary.plot(ax=ax, linewidth=1)
            plot = world_interpolated.plot(column='happiness_score', cmap='coolwarm', ax=ax, legend=True,
                                           vmin=vmin, vmax=vmax)
            
            # Adjust the legend to have only integer values and a constant range
            cbar = plot.get_figure().get_axes()[-1]
            cbar.set_yticks(np.linspace(vmin, vmax, 5))
            cbar.set_yticklabels([int(tick) for tick in np.linspace(vmin, vmax, 5)])
            
            # Add title and remove axes
            interpolated_year = year_start + interpolation_factor * (year_end - year_start)
            ax.set_title(f'Happiness Score by Country - {int(interpolated_year)}')
            ax.set_axis_off()
            
            # Save the image to a temporary file
            filename = f"happiness_{year_start}_{j}.png"
            plt.savefig(filename, format="png")
            image_files.append(filename)
            plt.close(fig)
    
    # Create the GIF using imageio with shorter duration for smooth transitions
    with imageio.get_writer("../data/happiness_score_smooth.gif", mode="I", duration=5, loop=0) as writer:
        for filename in image_files:
            image = imageio.imread(filename)
            writer.append_data(image)
    
    # Remove temporary files
    for filename in image_files:
        os.remove(filename)
