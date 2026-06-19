import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Helo")

@app.route("/hola")
def primer_mensaje():
    return render_template("primer_hola.html", title="Hola")
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



