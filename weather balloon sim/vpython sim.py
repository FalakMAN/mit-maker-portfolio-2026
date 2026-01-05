from vpython import *
import numpy as np
from matplotlib import cm

dt = 1
t_max = 6*60*60
h = 8500
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


R0 = 0.12
Hr = 7000
lat_factor = 0.85
z_max = 17000
true_radiation = lat_factor*R0*np.exp(altitude/Hr)*(altitude/z_max)*np.exp(1-altitude/z_max)
noise = np.random.normal(0, 0.05, size=len(true_radiation))
measured_radiation = np.clip(true_radiation + noise, 0, None)

#wind
wind_speed = 10 + 0.002*altitude   # m/s
wind_direction = np.pi/4            # 45 degrees
x = np.cumsum(wind_speed * np.cos(wind_direction) * dt)
y = np.cumsum(wind_speed * np.sin(wind_direction) * dt)
z = altitude
print(len(x), len(z))


#scene setup
scene.title = "Weather Balloon Simulation"
scene.width = 900
scene.height = 600
scene.background = color.cyan
scene.center = vector(0, 0, 15000)
scene.range = 50000

scene.userspin = True
scene.userzoom = True
scene.userpan = True
scene.autoscale = False

#balloon
balloon = sphere(pos = vector(x[0], y[0], z[0]), radius = 200, color = color.red, make_trail = True, trail_type = 'points', interval = 10, retain = 200)
scene.follow(balloon)

#Tether
tether = cylinder(pos = vector(x[0], y[0], 0), axis = vector(0, 0, z[0]), radius = 5, color = color.gray(0.5))

#wind arrow
wind_arrow = arrow(pos = vector(x[0], y[0], z[0]), axis = vector(50, 50, 0), shaftwidth = 10, color = color.white)

#animation loop
plasma = cm.get_cmap('plasma')
for i in range(1,len(z)):
    rate(50)    #animation speed
    balloon.pos = vector(x[i], y[i], z[i])

    #update tether
    tether.pos = vector(x[i], y[i], 0)
    tether.axis = vector(0, 0, z[i])

    #balloon color (based on radiation)
    rad_norm = (measured_radiation[i] - min(measured_radiation)) / (max(measured_radiation) - min(measured_radiation))
    c = plasma(rad_norm)
    balloon.color = vector(c[0], c[1], c[2])

    wind_arrow.pos = balloon.pos
    wind_arrow.axis = vector(wind_speed[i]*10*np.cos(wind_direction), wind_speed[i]*10*np.sin(wind_direction), 0)

scene.waitfor('click')