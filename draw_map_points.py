import matplotlib.pyplot as plt
import geopandas as gpd

# Create a plot
fig, ax = plt.subplots(figsize=(10, 10))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot(ax=ax, color='white', edgecolor='black')

# Plot each set of data
gdf1.plot(ax=ax, color='red', marker='o', label='Set 1')
gdf2.plot(ax=ax, color='blue', marker='^', label='Set 2')

# Add legend and title
plt.legend()
plt.title('Map of Coordinate Points')

# Show the plot
plt.show()
