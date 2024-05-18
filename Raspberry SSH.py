import paramiko
import psutil
import time

class SSHConnection:

    def __init__(self, hostname, username, password):
        """
        Initializes the SSH client with the given hostname, username, and password.

        Args:
           hostname (str): The hostname or IP address of the remote server.
           username (str): The username for authentication.
           password (str): The password for authentication.
        """
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname, username=username, password=password)

    def send_command(self, command):
        """
        Sends a command to the remote server and returns the output.

        Args:
            command (str): The command to be executed on the remote server.

        Returns:
            str: The output of the command.
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def get_cpu_temp(self):
        """
        Gets the CPU temperature of the remote server.

        Returns:
            str: The CPU temperature in degrees Celsius.
        """
        temp = self.send_command('vcgencmd measure_temp').strip().split('=')[1].split("'")[0]
        return temp

    def get_cpu_usage(self):
        """
        Gets the CPU usage of the remote server.

        Returns:
            float: The CPU usage as a percentage.
        """
        usage = psutil.cpu_percent(interval=1)
        return usage

    def get_ram_usage(self):
        """
        Gets the RAM usage of the remote server.

        Returns:
            float: The RAM usage as a percentage.
        """
        usage = psutil.virtual_memory().percent
        return usage

    def close(self):
        self.client.close()


class RaspberryPi1(SSHConnection):

    def __init__(self, hostname, username, password):
        """
        Initializes the Raspberry Pi 1 object with the given hostname, username, and password.

        Args:
            hostname (str): The hostname or IP address of the Raspberry Pi 1.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        super().__init__(hostname, username, password)

        self.hostname = hostname

    def __str__(self):
        """
        Returns a string representation of the Raspberry Pi 1 object.

        Returns:
            str: The string representation of the Raspberry Pi 1 object.
        """
        return "Raspberry Pi 1 ({})".format(self.hostname)


class RaspberryPi2(SSHConnection):

    def __init__(self, hostname, username, password):
        """
        Initializes the Raspberry Pi 2 object with the given hostname, username, and password.

        Args:
            hostname (str): The hostname or IP address of the Raspberry Pi 2.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        super().__init__(hostname, username, password)

        self.hostname = hostname

    def __str__(self):
        """
        Returns a string representation of the Raspberry Pi 2 object.

        Returns:
            str: The string representation of the Raspberry Pi 2 object.
        """
        return "Raspberry Pi 2 ({})".format(self.hostname)


if __name__ == "__main__":
    raspberry1 = RaspberryPi1('172.20.10.6', 'konradkrauze', '1984')
    raspberry2 = RaspberryPi2('172.20.10.8', 'jacks', 'jacks')
    while True:
        for pi in [raspberry1, raspberry2]:
            print(str(pi))
            print("CPU temp: {} C".format(pi.get_cpu_temp()))
            print("CPU usage: {}%".format(pi.get_cpu_usage()))
            print("RAM usage: {}%".format(pi.get_ram_usage()))
            print()
            time.sleep(5)
    raspberry1.close()
    raspberry2.close()