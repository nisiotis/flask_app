# -*- coding: utf-8 -*-
#!/usr/bin/env python

import g2
from flask import Flask, send_file, render_template
from flask import request, Response
from database import engine, db_session
from models import User
from cStringIO import StringIO

app = Flask(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/")
def index():
    u = User.query.all()
    return render_template('index.html', users=u)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        r = do_save(request.form['name'], request.form['email'], request.form['progress'])
        u = User.query.all()
        return render_template('index.html', users=u, result = r)
    else:
        u = User.query.all()
        return render_template('add.html', users=u)

def do_save(name, email, progress):
    try:
        if name <> "" and email <> "":
            u = User(name, email, progress)
            db_session.add(u)
            db_session.commit()
            return "Added Successfully"
        else:
            return "Nothing to Add"
    except:
        return "Add Failed"

@app.route('/edit/<int:uid>', methods=['GET', 'POST'])
def edit(uid):
    if request.method == 'POST':
        r = do_update(uid, request.form['name'], request.form['email'], request.form['progress'])
        u = User.query.all()
        return render_template('index.html', users=u, result = r)
    else:
        u = User.query.get(uid)
        return render_template('edit.html', user=u)

def do_update(uid, name, email, progress):
    try:
        if name <> "" and email <> "":
            u = User.query.filter_by(id=uid).first()
            u.name = name
            u.email = email
            u.progress = progress
            db_session.commit()
            return "%s Updated Successfully" % name
        else:
            return "Nothing to Update"
    except:
        return "Update Failed"


@app.route('/delete/<int:uid>')
def delete(uid):
    try:
        d = User.query.get(uid)
        db_session.query(User).filter(User.id==uid).delete()
        db_session.commit()
        r = "%s Deleted" % d.name
    except:
        r = "Delete Failed"
    u = User.query.all()     
    return render_template('index.html', users=u, result = r)

@app.route("/stats")
def stats(image="image.png"):
    return render_template('stats.html', image=image)

@app.route('/image.png')
def image_png():
    image = StringIO()
    u = User.query.all()
    g2.plot(image, u)
    image.seek(0)
    return send_file(image,
                     attachment_filename="image.png",
                     as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
