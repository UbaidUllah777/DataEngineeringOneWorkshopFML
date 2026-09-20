import matplotlib.pyplot as plt


class WebUI:

    def __init__(self):
        self.times = []
        self.values = []

    def plot_data(self, time, value):
        self.times.append(time)
        self.values.append(value)

        plt.clf()
        plt.plot(self.times, self.values)
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("Robot Data Stream")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.pause(0.01)