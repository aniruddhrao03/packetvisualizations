from flask import Flask, render_template, request
import socket
from threading import Thread

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def scan_port(target_host, target_port, output):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_host, target_port))
        if result == 0:
            output.append(f"Port {target_port} is open")
        else:
            output.append(f"Port {target_port} is closed")
        sock.close()
    except socket.error:
        output.append("Couldn't connect to server")

@app.route("/scan", methods=["POST"])
def scan():
    host = request.form["host"]
    start_port = int(request.form["startPort"])
    end_port = int(request.form["endPort"])

    output = []

    for port in range(start_port, end_port + 1):
        Thread(target=scan_port, args=(host, port, output)).start()

    return {"output": output}

if __name__ == "__main__":
    app.run(debug=True)
