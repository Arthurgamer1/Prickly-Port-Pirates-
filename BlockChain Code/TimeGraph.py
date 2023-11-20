import matplotlib.pyplot as plt


class P2PGraph:
    # Initializa Function with specific # of messages sent
    def __init__(self, x_num):
        self.msg_times = []
        self.x_msg_num = x_num

    # Adds ms times to the list
    def add_times(self, time):
        self.msg_times.append(time)

    # Draws a graph with specific list of points
    def draw_graph(self):
        fraction = self.x_msg_num / self.x_msg_num
        x_list = 0
        time_x = []
        for i in range(len(self.msg_times)):
            time_x.append(x_list)
            x_list += fraction

        plt.plot(time_x, self.msg_times)

        # naming the x axis
        plt.xlabel("x - # of messages")
        # naming the y axis
        plt.ylabel("y - milliseconds")

        # giving a title to my graph
        plt.title("Blockchain Runtime 1 min")

        # function to show the plot
        plt.show()

    # Clear X-axis
    def clear_times(self):
        for i in range(len(self.msg_times) - 1):
            self.msg_times.pop(i)


# List Values for receive & send
send_time = []
receive_time = []
total_times = []


with open("sender_time_data.csv", "r") as file:
    for line in file:
        send_time.append(line)

with open("receiver_time_data.csv", "r") as file:
    for line in file:
        receive_time.append(line)

for i in range(len(send_time) - 1):
    total = (float(send_time[i]) + float(receive_time[i])) * 1000
    total = round(total)
    print(total)
    total_times.append(total)

# x axis values
graph = P2PGraph(100)
# corresponding y axis values
for x in range(len(total_times) - 1):
    graph.add_times(total_times[x])
graph.draw_graph()
