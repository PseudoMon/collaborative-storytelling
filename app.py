import os
import sqlite3
from flask import Flask, render_template, url_for, json, request, redirect, g
import datetime
import peewee
from schema import Thread, Piece, db
import sys

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict (
    DATABASE=os.environ['DATABASE_URL']
))

################
# Database Test
@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response
    
def retrieve_threads_db():
    threads = []
    
    for t in Thread.select().order_by(Thread.latest_date.desc()).limit(5):
        pieces = []
        for piece in Piece.select().where(Piece.thread==t):
            pieces.append(piece)
        threads.append({'id': t.id, 'title': t.title, 'pieces': pieces})
    
    return threads
    
# ###Data schema
# [thread, thread, thread]
# thread = {id: int, title: string, pieces: [piece, piece, piece]}
# piece = {id: int, content: string, colour: string, author: string, date: dateobject?}

@app.route('/')
def front_page():
    #threads = retrieve_threads()
    #threads = isotopydate(threads)
    threads = retrieve_threads_db()
    return render_template('index.html', threads=threads)
    
@app.route('/about')
def about_page():
    return render_template('about.html')
    
@app.route('/newpiece', methods=['POST'])
def new_piece():
    threadid = request.form['threadid']
    #pieceid = request.form['pieceid']
    author = request.form['author']
    date = getdate()
    content = request.form['content']
    colour = request.form['colour']
    
    if author == "":
        author = "Anonymous"
    
    threadid = int(threadid)
    #pieceid = int(pieceid)
    thread = Thread.select().where(Thread.id==threadid).get()
    thread.latest_date = getdate()
    thread.save()
    
    piece = Piece.create(thread=thread, content=content, colour=colour, author=author, date=date)
    
    piece.save()
    #piece = {'id': pieceid, 'content': content, 'colour': colour, 'author': author, 'date': date}    
    #threadid = threadid - 1
    #threads[threadid]['pieces'].append(piece)
    
    #save_threads(threads)
    
    return redirect(url_for('front_page'))
    
@app.route('/newthread', methods=['GET', 'POST'])
def new_thread():
    #threads = retrieve_threads()
    #threadid = len(threads) + 1
    
    if request.method == 'GET':
        threads = retrieve_threads_db()
        return render_template('newthread.html', threads=threads)
    
    title = request.form['title']
    author = request.form['author']
    date = getdate()
    content = request.form['piececontent']
    colour = request.form['colour']
    
    if title == "":
        title = "Untitled"
    if author == "":
        author = "Anonymous"
    
    thread = Thread.create(title=title, create_date=date, latest_date=date)
    thread.save()
    
    piece = Piece.create(thread=thread, content=content, colour=colour, author=author, date=date)
    piece.save()
    #piece = {'id': 1, 'content': content, 'colour': colour, 'author': author, 'date': date}
    #thread = {'id': threadid, 'title': title, 'pieces': [piece]}
    #threads.append(thread)
    
    #save_threads(threads)
    
    return redirect(url_for('front_page'))
    
def retrieve_threads():
    try:
        file = open("alldata.dat", "r")
    except FileNotFoundError:
        newdatafile()
        file = open("alldata.dat", "r")
        
    threads = json.loads(file.read())
    file.close()
    return threads

def save_threads(threads):
    threads = json.dumps(threads)
    file = open("alldata.dat", "w")
    file.write(threads)
    file.close()
    return
    
def getdate():
    #d = datetime.date.today()
    #d = d.isoformat()
    d = datetime.datetime.now()
    return d
    
def isotopydate(threads):
    for thread in threads:
        for piece in thread['pieces']:
            piece['date'] = datetime.datetime.strptime(piece['date'], '%Y-%m-%d')
            
    return threads
    
def newdatafile():
    piece = {'id': 1, 'content': "EMPTY", 'colour': "", 'author': "System",
    'date': "1997-10-07"}
    thread = {'id': 1, 'title': "Stock", 'pieces': [piece]}
    save_threads([thread])
    return
    
if __name__ == "__main__":
    app.run(debug=True)