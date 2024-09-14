import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

class PendulumAnimation:
    def __init__(self):
        # Define parameters for the pendulum
        self.m = 5 #kg
        self.L = 1.234 #m
        self.g = 9.81 #m/s^2
        self.theta0 = np.deg2rad(60) #rad
        self.theta_dot0 = np.deg2rad(-31.2) #rad/s
        self.dt = 0.001 #sec
        
        # Initialize state
        self.theta = [self.theta0]
        self.theta_dot = [self.theta_dot0]
        self.x_coord = [self.theta2xy_inertial(self.theta0)[0]]
        self.y_coord = [self.theta2xy_inertial(self.theta0)[1]]
        self.current_time = 0
        
        # Setup the animation plot window and axes
        self.fig, self.ax = plt.subplots()
        self.setup_plot()
        self.create_animation()
    
    def theta2xy_inertial(self, theta):
        # Determines the (x,y) coords of the pendulum mass for a given theta
        x = self.L * np.sin(theta)
        y = -self.L * np.cos(theta)
        return x, y
    
    def f_theta_dot(self, theta_dot):
        return theta_dot

    def f_theta_dot_dot(self, theta):
        return -self.g / self.L * np.sin(theta)
    
    def update_state(self):
        # Update the pendulum state using RK4
        theta_i = self.theta[-1]
        theta_dot_i = self.theta_dot[-1]

        # Compute k1 values
        k1_theta = self.f_theta_dot(theta_dot_i)
        k1_theta_dot = self.f_theta_dot_dot(theta_i)
        
        # Compute k2 values
        k2_theta = self.f_theta_dot(theta_dot_i + 0.5 * self.dt * k1_theta_dot)
        k2_theta_dot = self.f_theta_dot_dot(theta_i + 0.5 * self.dt * k1_theta)
        
        # Compute k3 values
        k3_theta = self.f_theta_dot(theta_dot_i + 0.5 * self.dt * k2_theta_dot)
        k3_theta_dot = self.f_theta_dot_dot(theta_i + 0.5 * self.dt * k2_theta)
        
        # Compute k4 values
        k4_theta = self.f_theta_dot(theta_dot_i + self.dt * k3_theta_dot)
        k4_theta_dot = self.f_theta_dot_dot(theta_i + self.dt * k3_theta)
        
        # Update the next values using RK4 formula
        theta_next = theta_i + (self.dt / 6) * (k1_theta + 2 * k2_theta + 2 * k3_theta + k4_theta)
        theta_dot_next = theta_dot_i + (self.dt / 6) * (k1_theta_dot + 2 * k2_theta_dot + 2 * k3_theta_dot + k4_theta_dot)
        
        self.theta.append(theta_next)
        self.theta_dot.append(theta_dot_next)

        # Calculate the (x, y) position
        x, y = self.theta2xy_inertial(theta_next)
        self.x_coord.append(x)
        self.y_coord.append(y)
    
    def setup_plot(self):
        d = 0.3
        self.ax.set_xlim(-self.L - d, self.L + d)
        self.ax.set_ylim(-self.L - d, self.L + d)  # Adjusted to match the new y-axis range
        self.ax.set_aspect('equal')

        # Initialize the line and the circle
        self.line, = self.ax.plot([], [], 'k-', lw=3)
        self.circle = Circle((0, 0), 0.08, fc='r')  # Red circle for the pendulum mass
        self.ax.add_patch(self.circle)

        # Initialize time text
        self.time_template = 'Time = %.1fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)
    
    def init_animation(self):
        # Initiates the animation
        self.line.set_data([], [])
        self.circle.set_center((0, 0))
        self.time_text.set_text('')
        return self.line, self.circle, self.time_text

    def update_animation(self, frame):
        self.update_state()
        
        # Update line and circle
        x, y = self.x_coord[-1], self.y_coord[-1]
        self.line.set_data([0, x], [0, y])
        self.circle.set_center((x, y))
        
        # Update time text
        self.current_time += self.dt  # Increment time
        self.time_text.set_text(self.time_template % (self.current_time))
        
        return self.line, self.circle, self.time_text

    def create_animation(self):
        # Create the animation
        self.ani = FuncAnimation(
            self.fig, 
            self.update_animation, 
            frames=np.arange(0, 500),  # Large enough range to simulate indefinite animation
            init_func=self.init_animation, 
            blit=True, 
            interval=self.dt * 1000,
            repeat=True
        )

    def show(self):
        plt.show()

def main():
    pendulum_animation = PendulumAnimation()
    pendulum_animation.show()

if __name__ == '__main__':
    main()
