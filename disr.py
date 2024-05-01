from matplotlib import pyplot as plt
import numpy as np

maxlines = 10
plt.figure(figsize=(10,10))
plt.vlines(list(np.arange(-maxlines-.5,maxlines)), -maxlines, maxlines)
plt.hlines(list(np.arange(-maxlines-.5,maxlines)), -maxlines, maxlines)
plt.ylim(-maxlines,maxlines)
plt.xlim(-maxlines,maxlines)
plt.tick_params(labelleft=False, labelbottom=False)
plt.subplots_adjust(left=.05, right=.95, top=.95, bottom=.05)

# plt.scatter(0.5, 0.5)
p1_rad = np.deg2rad(60)
p3_rad = np.deg2rad(180)
p2_rad = np.deg2rad(300)

for r in range(maxlines):
    x_points = r*np.cos(p1_rad), r*np.cos(p2_rad), r*np.cos(p3_rad)
    y_points = r*np.sin(p1_rad), r*np.sin(p2_rad), r*np.sin(p3_rad)
    plt.scatter(x_points, y_points, label=r)

plt.legend()
plt.show()