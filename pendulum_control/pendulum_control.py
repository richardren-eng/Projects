import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

class PendulumAnimation:
    def __init__(self):
        # Define parameters for the pendulum and motor
        self.m = 5
        self.L = 1.234
        self.g = 9.81
        self.theta0 = np.deg2rad(-47.3)
        self.theta_dot0 = np.deg2rad(-15.2)
        self.dt = 0.01  # Adjusted step size
        self.K_motor = 0.05

        # PID parameters
        self.setpoint = np.deg2rad(60)  # Desired angle in radians
        
        #These paramters work
        self.KP = 3.5
        self.KI = 0.28
        self.KD = 0.1

        #You can play around with these parameters
        self.KP = 4.0
        self.KI = 0.5
        self.KD = 0.1

        
        # Initialize state
        self.theta = [self.theta0]
        self.theta_dot = [self.theta_dot0]
        self.x_coord = [self.theta2xy_inertial(self.theta0)[0]]
        self.y_coord = [self.theta2xy_inertial(self.theta0)[1]]

        self.noise = -3
        self.theta_measured = [self.theta0 + np.random.uniform(-self.noise, self.noise)]
        
        self.current_time = 0
        self.time = [self.current_time]
        
        # PID controller state
        self.integral = 0
        self.previous_error = 0
        self.pid_init = True
        
        # Initialize counters for measured theta text update
        self.theta_measured_update_counter = 0
        self.theta_measured_update_interval = 10  # Number of frames between updates for measured theta text
        
        # Setup the plot and animation
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
    
    def normalize_angle(self, angle):
        # Convert angle from radians to degrees and normalize to [-180, 180)
        angle_deg = np.rad2deg(angle) % 360
        if angle_deg >= 180:
            angle_deg -= 360
        return angle_deg
    
    def update_state_with_pid(self):
        # Simulate measurement noise
        noise = np.random.normal(np.deg2rad(-3), np.deg2rad(3))  
        theta_measured = self.theta[-1] + noise
        self.theta_measured.append(theta_measured)
        
        # Normalize measured angle
        theta_measured = self.normalize_angle(theta_measured)
        
        # PID control
        error = self.setpoint - self.theta[-1]  # Use theta in radians for PID
        
        #Initiate PID controller for i = 0
        if self.pid_init:
            derivative = 0
            self.integral = 0
            self.pid_init = False

        #Main control law for i > 0
        else:
            self.integral += 0.5 * self.dt * (error + self.previous_error)
            derivative = (error - self.previous_error) / self.dt
        
        self.previous_error = error

        control = self.K_motor * (self.KP * error + self.KI * self.integral + self.KD * derivative)

        # Update the state with the control input
        theta_dot_i = self.theta_dot[-1] + control
        theta_i = self.theta[-1]
        
        # Compute k1, k2, k3, k4 values for RK4
        k1_theta = self.f_theta_dot(theta_dot_i)
        k1_theta_dot = self.f_theta_dot_dot(theta_i)
        k2_theta = self.f_theta_dot(theta_dot_i + 0.5 * self.dt * k1_theta_dot)
        k2_theta_dot = self.f_theta_dot_dot(theta_i + 0.5 * self.dt * k1_theta)
        k3_theta = self.f_theta_dot(theta_dot_i + 0.5 * self.dt * k2_theta_dot)
        k3_theta_dot = self.f_theta_dot_dot(theta_i + 0.5 * self.dt * k1_theta)
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
        
        return theta_measured  # Return measured theta for displaying

    def setup_plot(self):
        d = 0.3
        self.ax.set_xlim(-self.L - d, self.L + d)
        self.ax.set_ylim(-self.L - d, self.L + d)
        self.ax.set_aspect('equal')

        # Initialize the line and the circle
        self.line, = self.ax.plot([], [], 'k-', lw=3)
        self.circle = Circle((0, 0), 0.08, fc='r')
        self.ax.add_patch(self.circle)

        # Initialize time text
        self.time_template = 'Time = %.1fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)
        
        # Initialize measured theta text
        self.measured_theta_text = self.ax.text(0.05, 0.8, '', transform=self.ax.transAxes)

        # Initialize actual theta text
        self.actual_theta_text = self.ax.text(0.05, 0.7, '', transform=self.ax.transAxes)

        # Initialize setpoint line
        setpoint_x = [-self.L, self.L]
        setpoint_y = [-self.L * np.cos(self.setpoint), self.L * np.cos(self.setpoint)]
        self.setpoint_line, = self.ax.plot(setpoint_x, setpoint_y, 'g--', lw=2)  # Green dashed line

    def init_animation(self):
        self.line.set_data([], [])
        self.circle.set_center((0, 0))
        self.time_text.set_text('')
        self.measured_theta_text.set_text('')
        self.actual_theta_text.set_text('')
        return self.line, self.circle, self.time_text, self.measured_theta_text, self.actual_theta_text, self.setpoint_line

    def update_animation(self, frame):
        # Update the pendulum state and obtain the measured theta
        theta_measured = self.update_state_with_pid()
        
        # Update line and circle
        x, y = self.x_coord[-1], self.y_coord[-1]
        self.line.set_data([0, x], [0, y])
        self.circle.set_center((x, y))
        
        # Update time text
        self.current_time += self.dt
        self.time.append(self.current_time)
        self.time_text.set_text(self.time_template % self.current_time)
        
        # Update measured theta text less frequently
        if self.theta_measured_update_counter % self.theta_measured_update_interval == 0:
            self.measured_theta_text.set_text(f'Measured θ = {theta_measured:.1f}°')
            self.actual_theta_text.set_text(f'Actual θ = {self.normalize_angle(self.theta[-1]):.1f}°')
        
        # Increment update counter
        self.theta_measured_update_counter += 1

        # Update setpoint line
        setpoint_x = [self.theta2xy_inertial(self.setpoint)[0] , 0]
        setpoint_y = [self.theta2xy_inertial(self.setpoint)[1] , 0]

        self.setpoint_line.set_data(setpoint_x, setpoint_y)
        
        return self.line, self.circle, self.time_text, self.measured_theta_text, self.actual_theta_text, self.setpoint_line

    def create_animation(self):
        self.ani = FuncAnimation(
            self.fig,
            self.update_animation,
            frames=np.arange(0, 500),
            init_func=self.init_animation,
            blit=True,
            interval=self.dt * 1000,  # Interval for animation
            repeat=True
        )

    def show(self):
        plt.show()

def main():
    pendulum_animation = PendulumAnimation()
    pendulum_animation.show()
    
    #Plot the theta vs time
    plt.plot(pendulum_animation.time , np.rad2deg(pendulum_animation.theta_measured), 'b-', label='measured' )
    plt.plot(pendulum_animation.time , np.rad2deg(pendulum_animation.theta), 'r-', label='actual')
    plt.axhline(np.rad2deg(pendulum_animation.setpoint), color='g', linestyle='--', label='Setpoint')  # Green dashed line

    plt.legend(loc='upper right')

    plt.title('Pendulum Trajectory Over Control Life')
    plt.xlabel('Time (sec)')
    plt.ylabel('Theta (deg)')

    plt.xlim(left=0 , right=max(pendulum_animation.time))

    plt.show()


if __name__ == '__main__':
    main()
