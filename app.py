import os
from flask import Flask, render_template, url_for, json, request, redirect, g
import datetime
import peewee
from schema import Thread, Piece, db

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict (
    DATABASE=os.environ['DATABASE_URL']
))

# ###############
# Database handling
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

# ###############
# Routing et cetera
@app.route('/')
def front_page():
    threads = retrieve_threads_db()
    return render_template('index.html', threads=threads)
    
@app.route('/about')
def about_page():
    return render_template('about.html')
    
@app.route('/newpiece', methods=['POST'])
def new_piece():
    threadid = request.form['threadid']
    author = request.form['author']
    date = getdate()
    content = request.form['content']
    colour = request.form['colour']
    
    if author == "":
        author = "Anonymous"
    
    threadid = int(threadid)
    thread = Thread.select().where(Thread.id==threadid).get()
    thread.latest_date = getdate()
    thread.save()
    
    piece = Piece.create(thread=thread, content=content, colour=colour, author=author, date=date)
    piece.save()
    
    return redirect(url_for('front_page'))
    
@app.route('/newthread', methods=['GET', 'POST'])
def new_thread():
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
    
    return redirect(url_for('front_page'))

# ###############
# Misc functions
def getdate():
    #d = datetime.date.today()
    #d = d.isoformat()
    d = datetime.datetime.now()
    return d
    
def isotopydate(threads):
    # a converter for when when I was using json for everything
    for thread in threads:
        for piece in thread['pieces']:
            piece['date'] = datetime.datetime.strptime(piece['date'], '%Y-%m-%d')
            
    return threads
    
    
if __name__ == "__main__":
    app.run(debug=True)