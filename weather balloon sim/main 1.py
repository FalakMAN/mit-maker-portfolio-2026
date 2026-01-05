import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import json

dt = 1 #seconds
t_max = 6*60*60 #6 hours
h = 8500 #scale height/H
v0 = 8.0

time = np.arange(0, t_max, dt)
altitude = np.zeros_like(time, dtype = float)

for i in range(1, len(time)):
    v = v0*np.exp(-altitude[i-1]/h)
    altitude[i] = altitude[i-1] + v*dt

    if altitude[i] > 30000:
        altitude = altitude[:i]
        time = time[:i]
        break

#radiation vs. altitude measurement model

R0 = 0.12   # µSv/hr at ground level in UAE
Hr = 7000
lat_factor = 0.85
z_max = 17000    #pfotzer maximum altitude (in m)
true_radiation = lat_factor*R0*np.exp(altitude/Hr)*(altitude/z_max)*np.exp(1-altitude/z_max)
noise = np.random.normal(0, 0.05, size = len(true_radiation))
measured_radiation = np.clip(true_radiation + noise, 0, None)

#3d factors (wind)
wind_speed = 10 + 0.002*altitude #in m/s
wind_direction = np.pi/4 #pi/4 rad or 45 degrees

x = np.cumsum(wind_speed*np.cos(wind_direction)*dt)
y = np.cumsum(wind_speed*np.sin(wind_direction)*dt)
z = altitude



#graphing in 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(min(x), max(x))
ax.set_ylim(min(y), max(y))
ax.set_zlim(0, max(z))

ax.set_xlabel("East-West (m)")
ax.set_ylabel("North-South (m)")
ax.set_zlabel("Altitude (m)")

balloon, = ax.plot(
    [], [], [],
    marker = 'o',
    markersize = 10,
    color = 'red',
    alpha = 0.9,
    markeredgecolor = 'black'
)

tether, = ax.plot(
    [], [], [],
    color = 'gray',
    linewidth = 1,
    alpha = 0.6
)

norm = mcolors.Normalize(
    vmin = np.min(measured_radiation),
    vmax = np.max(measured_radiation)
)

sc = ax.scatter(
    [], [], [],
    c = [],
    cmap = 'plasma',
    norm = norm,
    s = 8
                )

sc.set_alpha(1.0)
balloon.set_data([x[0]], [y[0]])
balloon.set_3d_properties([z[0]])

def update(frame):
    sc._offsets3d = (
        x[:frame],
        y[:frame],
        z[:frame]
    )
    sc.set_array(measured_radiation[:frame])
    sc.set_clim(norm.vmin, norm.vmax)

    balloon.set_data([x[frame]], [y[frame]])
    balloon.set_3d_properties([z[frame]])
    tether.set_data([x[frame], x[frame]], [y[frame], y[frame]])
    tether.set_3d_properties([0, z[frame]])

    return sc, balloon, tether

ani = FuncAnimation(
    fig,
    update,
    frames = range(1, len(z), 10),
    interval = 20,
    blit = False,
    repeat = False
)
cmap = cm.plasma
norm = mcolors.Normalize(vmin = min(measured_radiation), vmax = max(measured_radiation))
sm = cm.ScalarMappable(cmap = cmap, norm = norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax = ax)
cbar.set_label("Radiation (µSv/hr)")

plt.show()





#data export
flight_data = []
for i in range(len(z)):
    flight_data.append({
        "x": float(x[i]),
        "y": float(y[i]),
        "z": float(z[i]),
        "radiation": float(measured_radiation[i]),
        "wind": float(wind_speed[i])
    })

with open("balloon_flight.json", "w") as f:
    json.dump(flight_data, f)

print("Saved balloon_flight.json")