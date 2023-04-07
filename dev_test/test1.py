import numpy as np
import matplotlib.pyplot as plt

# Generate some random data
num_points = 100
x_data = np.random.randn(num_points, 10)
y_data = np.random.randn(num_points, 10)

# Define the colors for each data set using the 'viridis' color map
colors = plt.cm.viridis(np.linspace(0, 1, 10))

# Plot each data set in a scatter plot with a different color
for i in range(10):
    plt.scatter(x_data[:, i], y_data[:, i], c=colors[i], label='Data Set {}'.format(i+1))

# Add a legend to the plot
plt.legend()

# Show the plot
plt.show()

