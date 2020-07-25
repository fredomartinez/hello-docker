from flask import Flask, render_template
import os
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    name = os.getenv("NAME")
    hostname = socket.gethostname()
    return render_template('hello.html', name=name, hostname=hostname)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)