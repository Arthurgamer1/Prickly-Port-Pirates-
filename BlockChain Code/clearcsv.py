def clear_csv(file_path):
    try:
        # Open the file in write mode, which will automatically erase its contents
        with open(file_path, 'w') as file:
            pass  # No need to write anything, just opening and closing will clear the file
        print(f"Cleared the contents of {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
clear_csv("receiver_time_data.csv")
clear_csv("sender_time_data.csv")
