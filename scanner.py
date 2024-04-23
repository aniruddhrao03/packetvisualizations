from flask import Flask, render_template, request
import socket
from threading import Thread
from queue import Queue

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def scan_port(target_host, target_port, output_queue):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_host, target_port))
        protocol = identify_protocol(target_port)
        if result == 0:
            output_queue.put(f"Port {target_port} is open ({protocol})")
        else:
            output_queue.put(f"Port {target_port} is closed")
        sock.close()
    except Exception as e:
        output_queue.put(f"Error scanning port {target_port}: {e}")

def identify_protocol(port):
    protocol_dict = {
        21: "FTP",
        22: "SSH",
        23: "TELNET",
        25: "SMTP",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP",
        8080: "HTTP-ALT"
    }
    return protocol_dict.get(port, "Unknown")

@app.route("/scan", methods=["POST"])
def scan():
    host = request.form["host"]
    start_port = int(request.form["startPort"])
    end_port = int(request.form["endPort"])

    output_queue = Queue()
    threads = []

    for port in range(start_port, end_port + 1):
        thread = Thread(target=scan_port, args=(host, port, output_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    output = []
    while not output_queue.empty():
        output.append(output_queue.get())

    return {"output": output}

if __name__ == "__main__":
    app.run(debug=True)
