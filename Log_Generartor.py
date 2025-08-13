import random
import string
import time
import logging
logging.basicConfig(filename="log_generator.log", level=logging.ERROR)
LOG_LEVELS= ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

ACTIONS= ["Login","Logout","Date Request","Download","Error"]

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception as e:
        logging.error(f"Error generating random string: {e}")
        return "Error"

def generate_log_entry():
    """Generate a single log entry."""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_level = random.choice(LOG_LEVELS)
        action = random.choice(ACTIONS)
        user_id = generate_random_string(8)
        log_entry = f"{timestamp} - {log_level} - User: {user_id} - Action: {action}"
        return log_entry
    except Exception as e:
        logging.error(f"Error generating log entry: {e}")
        return "Error"    
    
def write_logs_to_file(filename, num_entries=100):
    """Write multiple log entries to a file."""
    try:
        with open(filename, 'a') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                if log != "Error":
                    file.write(log+ "\n")  
        print(f"log entries written to {filename}")  
    except Exception as e:
        logging.error(f"Error writing logs to file: {e}")
        print("Error writing logs to file. Check log_generator.log for details.")                

write_logs_to_file("generated_logs.txt", num_entries=200)        