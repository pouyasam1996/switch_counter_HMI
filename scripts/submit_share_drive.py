import os
import subprocess
import sys
import datetime

class FolderManager:
    def __init__(self):
        self.base_path = "/mnt/shared/Maintenance/16.OnlineManufacturing"
        self.folder_name = "Effytec3"
        self.sub_folder = "runtimes"
        self.current_date = None
        self.csv_file = None
        self._update_folder_and_file()

    def _run_sudo_command(self, command):
        try:
            result = subprocess.run(['sudo'] + command, check=True, text=True, capture_output=True)
            print(f"Success: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            return False

    def _update_folder_and_file(self):
        new_date = datetime.datetime.now().strftime("%m_%d_%Y")
        if new_date != self.current_date:
            self.current_date = new_date
            target_folder = os.path.join(self.base_path, self.folder_name, self.sub_folder)
            self.csv_file = os.path.join(target_folder, f"{self.current_date}.csv")

            print(f"Creating folder: {target_folder}")
            if not self._run_sudo_command(['mkdir', '-p', target_folder]):
                print("Failed to create folder. Check permissions or path.")
                sys.exit(1)

            if not os.path.exists(self.csv_file):
                try:
                    echo_cmd = f"echo 'Timestamp,PouchNumber' | sudo tee {self.csv_file}"
                    subprocess.run(echo_cmd, shell=True, check=True, text=True, capture_output=True)
                    print("CSV file created.")
                except subprocess.CalledProcessError as e:
                    print(f"Error creating CSV: {e.stderr}")
                    sys.exit(1)

    def data_saving_function(self, function_number):
        self._update_folder_and_file()
        timestamp = datetime.datetime.now().strftime("%-H:%M")
        try:
            echo_cmd = f"echo '{timestamp},{function_number}' | sudo tee -a {self.csv_file}"
            subprocess.run(echo_cmd, shell=True, check=True, text=True, capture_output=True)
            print(f"saving {function_number} at {timestamp}")
        except subprocess.CalledProcessError as e:
            print(f"Error writing to CSV: {e.stderr}")