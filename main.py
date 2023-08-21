import subprocess
import threading

def run_script(script_name):
    # Using subprocess to run the script and collect the output
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    print(f"Output from {script_name}:\n{result.stdout}")

if __name__ == "__main__":
    # List of scripts to run
    scripts = ['./modules/client_server_communication.py', './modules/temperature_control.py']

    threads = []
    for script in scripts:
        # Starting each script in a separate thread
        thread = threading.Thread(target=run_script, args=(script,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All scripts finished.")