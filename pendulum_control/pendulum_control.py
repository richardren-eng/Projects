import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ellipk
import matplotlib.animation as animation

def theta2xy(L, theta):
    # Determines the (x,y) coords of the pendulum mass for a given theta
    x = L * np.cos(theta)
    y = L * np.sin(theta)
    return x, y

# Define parameters for the pendulum
m = 5  # kg
L = 1  # m
g = 9.81  # m/s^2

# Initial conditions
theta0 = np.deg2rad(45)  # radians
theta_dot0 = np.deg2rad(0)  # rad/s

# Time step for numerical solver
dt = 0.0001  # seconds

# Theoretical pendulum period
T_theory = 2 * np.pi * np.sqrt(L / g)

# Initialize time and state parameters
time = np.arange(0, T_theory, dt)

theta = [theta0]
theta_dot = [theta_dot0]

x0, y0 = theta2xy(L, theta0)
x_coord = [x0]
y_coord = [y0]

# Define the equations of motion
def f_theta_dot(theta_dot):
    return theta_dot

def f_theta_dot_dot(theta):
    return -g / L * np.sin(theta)

# Runge-Kutta 4th order method (RK4)
for i in range(0, len(time) - 1):
    # Current state
    theta_i = theta[i]
    theta_dot_i = theta_dot[i]
    
    # Compute k1 values
    k1_theta = f_theta_dot(theta_dot_i)
    k1_theta_dot = f_theta_dot_dot(theta_i)
    
    # Compute k2 values
    k2_theta = f_theta_dot(theta_dot_i + 0.5 * dt * k1_theta_dot)
    k2_theta_dot = f_theta_dot_dot(theta_i + 0.5 * dt * k1_theta)
    
    # Compute k3 values
    k3_theta = f_theta_dot(theta_dot_i + 0.5 * dt * k2_theta_dot)
    k3_theta_dot = f_theta_dot_dot(theta_i + 0.5 * dt * k2_theta)
    
    # Compute k4 values
    k4_theta = f_theta_dot(theta_dot_i + dt * k3_theta_dot)
    k4_theta_dot = f_theta_dot_dot(theta_i + dt * k3_theta)
    
    # Update the next values using RK4 formula
    theta_next = theta_i + (dt / 6) * (k1_theta + 2 * k2_theta + 2 * k3_theta + k4_theta)
    theta_dot_next = theta_dot_i + (dt / 6) * (k1_theta_dot + 2 * k2_theta_dot + 2 * k3_theta_dot + k4_theta_dot)
    
    theta.append(theta_next)
    theta_dot.append(theta_dot_next)

    # Calculate the (x, y) position
    x, y = theta2xy(L, theta_next)
    x_coord.append(x)
    y_coord.append(y)

# Optional: Plotting the results if needed
    #plt.plot(time, theta)
    #plt.show()

#Animate
#Create the figure and axis
d = 0.2
fig, ax = plt.subplots()
ax.set_xlim(-L - d , L + d)
ax.set_ylim(-L - d, L + d)

#Create a line object for the massless rod
line, = ax.plot([], [], 'o-', lw=2)

#Initialize
def animation_init():
    line.set_data([],[])
    return license

#Update
def animation_update(frame):
    x = x_coord[frame]
    y = y_coord[frame]
    line.set_data([0, x] , [0, y])
    return line,

ani = animation.FuncAnimation(fig, animation_update, frames=len(time), init_func=animation_init, blit=True, interval=20)

plt.show()