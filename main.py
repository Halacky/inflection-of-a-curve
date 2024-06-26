import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define the data matrix xy
xy = np.array([[5, 20], [3, 18], [2, 19], [1.5, 16], [5.5, 9], [4.5, 8], 
               [3.5, 12], [2.5, 11], [3.5, 3], [2, 3], [2, 6], [0, 6], 
               [2.5, -4], [4, -5], [6.5, -2], [7.5, -2.5], [7.7, -3.5], [6.5, -8]])

n = xy.shape[0]
t = np.arange(n)
fx = interp1d(t, xy[:,0], kind='cubic', bounds_error=False)  # Set bounds_error=False to allow extrapolation
fy = interp1d(t, xy[:,1], kind='cubic', bounds_error=False)

time = np.linspace(0, n-1, 511)
uv = np.column_stack((fx(time), fy(time)))

def curvature(t, fx, fy):
    dt = 1e-6  # Small step for numerical differentiation
    t = np.clip(t, 0, n-1)  # Clip t within the range of the original data
    
    xp = (fx(t + dt) - fx(t - dt)) / (2 * dt)
    yp = (fy(t + dt) - fy(t - dt)) / (2 * dt)
    
    d2x = (fx(t + dt) - 2 * fx(t) + fx(t - dt)) / dt**2
    d2y = (fy(t + dt) - 2 * fy(t) + fy(t - dt)) / dt**2
    
    v = np.sqrt(xp**2 + yp**2)  # Speed
    curvature_vals = (xp * d2y - yp * d2x) / v**3  # (Signed) curvature
    
    # Handle possible NaN values due to division by zero
    curvature_vals[np.isnan(curvature_vals)] = 0.0
    
    return np.abs(curvature_vals)  # Absolute curvature of the data

kappa = curvature(time, fx, fy)  # Compute curvature values

# Find maximum curvature value, handling NaN values
max_kappa = np.nanmax(kappa)
curvature_zero = 2 * np.pi / np.max(np.ptp(xy, axis=0))  # A small threshold

# Calculate i_col while handling potential NaN values
if max_kappa > 0:
    i_col = np.floor(127 * curvature_zero / (curvature_zero + kappa)).astype(int)
else:
    i_col = np.zeros_like(kappa, dtype=int)

# Clip i_col to ensure it is within valid range of colors
i_col = np.clip(i_col, 0, 127)

# Get colormap
colors = plt.cm.terrain(np.linspace(0, 1, 128))

plt.figure(figsize=(8, 6))
plt.plot(xy[:,0], xy[:,1], 'o', color='black')

# Plot each line segment with corresponding color
for i in range(1, len(uv)):
    plt.plot([uv[i-1, 0], uv[i, 0]], [uv[i-1, 1], uv[i, 1]], color=colors[i_col[i]])

threshold = 0.25 * max_kappa  
inflection_points_indices = np.where(kappa > threshold)[0]
# Plot the inflection points on the existing plot
plt.plot(uv[inflection_points_indices, 0], uv[inflection_points_indices, 1], 's', color='red', label='Inflection Points')

plt.xlabel('x')
plt.ylabel('y')
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.savefig('inflection_points_plot.png')
