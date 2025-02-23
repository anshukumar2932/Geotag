from function_module import *
from flask import Flask, render_template, request, jsonify, send_file, Response

app = Flask(__name__)

# Routes
@app.route('/')
def entry_page():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
