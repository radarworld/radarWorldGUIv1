import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random


class Animate:

    def __init__(self, sensor):
        # Create figure for plotting
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.xs = []
        self.ys = []
        self.ylabel = sensor
        self.readings = 20

    # This function is called periodically from FuncAnimation
    def _update(self, i):

        # Read temperature (Celsius) from TMP102
        temp_c = random()

        # Add x and y to lists
        self.xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        self.ys.append(temp_c)

        # Limit x and y lists to 20 items
        self.xs = self.xs[-self.readings:]
        self.ys = self.ys[-self.readings:]

        # Draw x and y lists
        self.ax.clear()
        self.ax.plot(self.xs, self.ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title(self.ylabel + ' over Time')
        plt.ylabel(self.ylabel)

    def start(self):
        print('Starting')
        # Set up plot to call animate() function periodically
        self.anim = animation.FuncAnimation(self.fig, self._update, interval=200)
        plt.show()


rand = Animate('Torque')
rand.start()


