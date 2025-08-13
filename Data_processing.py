import pandas as pd
import random
import logging
import string
import numpy as np
import matplotlib.pyplot as plt

def generate_log_entry():
    """Generate a single log entry."""
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    action = random.choice(["Login","Logout","Date Request","Download","Error"])
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp} - {log_level} - User: {user_id} - Action: {action}"

def write_logs_to_file(filename, num_entries=100):
    """Write multiple log entries to a file."""
    try:
        with open(filename, 'a') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + "\n")
        print(f"log entries written to {filename}")
    except Exception as e:
        logging.error(f"Error writing logs to file: {e}")
        print("Error writing logs to file. Check log_generator.log for details.")

def load_and_process_logs(filename="generated_logs.txt"):   
    """Load logs from a file and process them into a DataFrame."""
    try:
        df = pd.read_csv(
            filename,
            sep=r' - ',
            header=None,
            engine='python',
            names=['Timestamp', 'LogLevel', 'User', 'Action']
        )
        df['Timestamp'] = df['Timestamp'].str.strip()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.dropna(subset=['Timestamp'])
        if df.empty:
            print("No valid log entries found.")
        else:
            print("Data after timestamp conversion:")
            print(df.head())
        df.set_index('Timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error loading or processing logs: {e}")
        return None    
    
def analyze_data(df):
    """Analyze the DataFrame and plot the number of actions per user."""
    try:
        if df is None or df.empty:
            print("DataFrame is empty or not loaded properly.")
            return None, None

        log_level_counts = df['LogLevel'].value_counts()
        action_counts = df['Action'].value_counts()
        log_count = len(df)
        unique_users = df['User'].nunique()
        logs_per_day = df.resample('D').size()
        average_logs_per_day = logs_per_day.mean()
        max_logs_per_day = logs_per_day.max()
        print("\nLog Level Counts:\n", log_level_counts)
        print("\nAction Counts:\n", action_counts)
        print(f"\nTotal number of logs: {log_count}")
        print(f"Number of unique users: {unique_users}")
        print(f"Average logs per day: {average_logs_per_day:.2f}")
        print(f"Maximum logs in a single day: {max_logs_per_day}")

        stats = {
            'log_level_counts': log_level_counts,
            'action_counts': action_counts,
            'log_count': log_count,
            'unique_users': unique_users,
            'average_logs_per_day': average_logs_per_day,
            'max_logs_per_day': max_logs_per_day
        }
        return stats
    except Exception as e:
        print(f"Error during data analysis: {e}")
        return None


def visualize_trends(df):
    """Visualize trends in the log data."""
    try:
        logs_by_day = df.resample('D').size()
        plt.figure(figsize=(10, 5))
        plt.plot(logs_by_day.index, logs_by_day.values, marker='o', linestyle='-',color='b')
        plt.title('Number of Logs per Day')
        plt.xlabel('Date')
        plt.ylabel('Number of Logs')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error during visualization: {e}")

log_filename = "generated_logs.txt"
write_logs_to_file(log_filename, num_entries=200)
df = load_and_process_logs(log_filename)      
if df is not None:
    stats = analyze_data(df)
    
    visualize_trends(df)