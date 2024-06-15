# from flask import Flask, render_template, request, jsonify
#
#
# app = Flask(__name__)

from uuid import uuid4


# @app.route('/')
# def index():
#     return render_template(f'index.html')

for i in range(5):
    print(uuid4())