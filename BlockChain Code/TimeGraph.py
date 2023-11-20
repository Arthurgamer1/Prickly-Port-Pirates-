import matplotlib.pyplot as plt


class P2PGraph:
    def __init__(self, y_time):
        self.msg_times = []
        self.y_time = y_time

    # Adds ms times to the list
    def add_times(self, time):
        self.msg_times.append(time)

    # Draws a graph with specific list of points
    def draw_graph(self):
        # plotting the points
        fraction = self.y_time / len(self.msg_times)
        y_list = 0
        time_y = []
        for i in range(len(self.msg_times)):
            time_y.append(y_list)
            y_list += fraction

        plt.plot(self.msg_times, time_y)

        # naming the x axis
        plt.xlabel("x - Miliseconds")
        # naming the y axis
        plt.ylabel("y - Minute")

        # giving a title to my graph
        plt.title("Blockchain Runtime 1 min")

        # function to show the plot
        plt.show()

    # Clear X-axis
    def clear_times(self):
        for i in range(len(self.msg_times) - 1):
            self.msg_times.pop(i)


# Testing the class!
"""
# x axis values
graph = P2PGraph(60)
# corresponding y axis values
for i in range(5):
    # print(i)
    graph.add_times(i)
graph.draw_graph()
"""
