function scanPorts() {
    var host = document.getElementById("host").value;
    var startPort = document.getElementById("startPort").value;
    var endPort = document.getElementById("endPort").value;

    if (!host || !startPort || !endPort) {
        alert("Please enter all fields.");
        return;
    }

    var outputDiv = document.getElementById("output");
    outputDiv.innerHTML = "Scanning " + host + "...<br>";

    fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `host=${host}&startPort=${startPort}&endPort=${endPort}`
    })
    .then(response => response.json())
    .then(data => {
        data.output.forEach(message => {
            outputDiv.innerHTML += message + "<br>";
        });
    });
}
