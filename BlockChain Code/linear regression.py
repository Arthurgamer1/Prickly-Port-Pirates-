import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

try:
    # Load the data from CSV files
    sender_data = pd.read_csv("sender_time_data.csv", names=["TimeTaken"])
    receiver_data = pd.read_csv("receiver_time_data.csv", names=["TimeTaken"])

    #print("Sender Data:\n", sender_data.head())
    #print("Receiver Data:\n", receiver_data.head())

    # Ensure both datasets have the same length
    min_length = min(len(sender_data), len(receiver_data))
    sender_data = sender_data.head(min_length)
    receiver_data = receiver_data.head(min_length)

    # Combine the time taken by sender and receiver for each message
    combined_data = sender_data['TimeTaken'] + receiver_data['TimeTaken']
    combined_data = combined_data.reset_index()
    combined_data.columns = ['MessageCount', 'CombinedTimeTaken']

    #print("Combined Data:\n", combined_data.head())

    # Perform Linear Regression
    slope, intercept, _, _, _ = stats.linregress(combined_data['MessageCount'], combined_data['CombinedTimeTaken'])

    # Create a function for the linear model (y = mx + c)
    def linear_model(x, slope, intercept):
        return slope * x + intercept

    # Generate a range of values for messages
    message_range = np.linspace(1, len(combined_data), 100)

    # Plotting
    plt.figure(figsize=(8, 6))

    plt.scatter(combined_data['MessageCount'], combined_data['CombinedTimeTaken'], label="Combined Data")
    plt.plot(message_range, linear_model(message_range, slope, intercept), color="red", label="Fitted Line")
    plt.title("Combined: Messages vs Time Taken")
    plt.xlabel("Number of Messages")
    plt.ylabel("Combined Time Taken (seconds)")
    plt.legend()

    plt.show(block=True)
except Exception as e:
    print("An error occurred: ", e)
