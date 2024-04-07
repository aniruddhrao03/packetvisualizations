import socket

def scan_port(target_host, target_port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout for connection attempt
        sock.settimeout(1)
        # Attempt to connect to target host and port
        result = sock.connect_ex((target_host, target_port))
        if result == 0:
            print(f"Port {target_port} is open")
        else:
            print(f"Port {target_port} is closed")
        # Close the socket connection
        sock.close()
    except socket.error:
        print("Couldn't connect to server")

def port_scan(target_host, port_range):
    # Split port range into start and end ports
    start_port, end_port = port_range.split('-')
    start_port = int(start_port)
    end_port = int(end_port)
    for port in range(start_port, end_port + 1):
        scan_port(target_host, port)

if __name__ == "__main__":
    target_host = input("Enter target host: ")
    port_range = input("Enter port range (e.g., 1-100): ")
    port_scan(target_host, port_range)
