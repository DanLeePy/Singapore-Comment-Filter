#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from model import censor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'input.html',
        data=[])
@app.route("/result" , methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get("comment")
    resp = censor(select)
    pp(resp)
    if resp:
        data = resp
    return render_template(
        'result.html',
        data=data,
        error=error)

if __name__=='__main__':
    app.run(debug=True)            