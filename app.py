import os
from flask import Flask, render_template, url_for, json, request, redirect, g, session, escape
import datetime
import peewee
from schema import Thread, Piece, Comment, Tag, db

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '\x157;S\xc0\xa2M\x89\xedS\xffAlBx\xdaf\xc9<\x1e oZ\x04'

# Windows can't read Heroku's postgres properly enough to put it
#   into DATABASE_URL :(
# Can't use this in the database .py file yet because of a weird recursive import bug
try:
    app.config.update(dict (
    DATABASE=os.environ['DATABASE_URL']
    ))
except KeyError:
    pass
    

# ###############
# Database handling
@app.before_request
def before_request():
    if 'author' not in session:
        session['author'] = ""
    if 'colour' not in session:
        session['colour'] = ""
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response
    
def retrieve_threads_db(selected_threads):
    threads = []
    
    for t in selected_threads:
        pieces = []
        for piece in Piece.select().where(Piece.thread==t):
            pieces.append(piece)
        threads.append({'id': t.id, 'title': t.title, 'pieces': pieces})
    
    return threads

# ###############
# Routing et cetera
@app.route('/')
def front_page():
    selector = Thread.select().order_by(Thread.latest_date.desc()).limit(5)
    threads = retrieve_threads_db(selector)
    
    return render_template('index.html', threads=threads, authorses=escape(session['author']), colourses=escape(session['colour']))
    
@app.route('/about')
def about_page():
    return render_template('about.html')
    
@app.route('/thread/<threadid>/')
def thread_page(threadid):

    t = Thread.select().where(Thread.id==threadid).get()
    pieces = []
    for piece in Piece.select().where(Piece.thread==t):
        pieces.append(piece)
        
    comments = []
    for comment in Comment.select().where(Comment.thread==t):
        comments.append(comment)
        
    tags = []
    for tag in Tag.select().where(Tag.thread==t):
        tags.append(tag)
        
    thread = {'id': t.id, 'title': t.title, 'pieces': pieces}
    
    return render_template('thread.html', thread=thread, comments=comments, tags=tags, authorses=escape(session['author']), colourses=escape(session['colour']))
    
@app.route('/newpiece', methods=['POST'])
def new_piece():
    threadid = request.form['threadid']
    author = request.form['author']
    date = getdate()
    content = request.form['content']
    colour = request.form['colour']
    
    if author == "":
        author = "Anonymous"
    else:
        session['author'] = author
    session['colour'] = colour
    
    threadid = int(threadid)
    thread = Thread.select().where(Thread.id==threadid).get()
    thread.latest_date = getdate()
    thread.save()
    
    piece = Piece.create(thread=thread, content=content, colour=colour, author=author, date=date)
    piece.save()
    
    return redirect(url_for('thread_page', threadid=threadid))
    
@app.route('/newthread', methods=['GET', 'POST'])
def new_thread():
    if request.method == 'GET':
        threads = retrieve_threads_db()
        return render_template('newthread.html', threads=threads, authorses=escape(session['author']), colourses=escape(session['colour']))
    
    title = request.form['title']
    author = request.form['author']
    date = getdate()
    content = request.form['piececontent']
    colour = request.form['colour']
    tags = splittags(request.form['tags'])
    
    if title == "":
        title = "Untitled"
    if author == "":
        author = "Anonymous"
    else:
        session['author'] = author
    session['colour'] = colour
    
    thread = Thread.create(title=title, create_date=date, latest_date=date)
    thread.save()
    
    for tag in tags:
        if tag == '':
            pass
        else:
            tagsindb = Tag.create(thread=thread, sharp=tag)
            tagsindb.save()
    
    piece = Piece.create(thread=thread, content=content, colour=colour, author=author, date=date)
    piece.save()
    
    return redirect(url_for('front_page'))
    
@app.route('/newcomment', methods=['POST'])
def new_comment():
    threadid = request.form['threadid']
    author = request.form['author']
    colour = request.form['colour']
    content = request.form['content']
    date = getdate()
    
    session['author'] = author
    session['colour'] = colour
    
    threadid = int(threadid)
    thread = Thread.select().where(Thread.id==threadid).get()
    comment = Comment.create(thread=thread, comment=content, colour=colour, author=author, date=date)
    comment.save()
    
    return redirect(url_for('thread_page', threadid=threadid))
    
@app.route('/search/')
def search_threads():
    searchin = request.args.get('search')
    if not searchin:
        return render_template('searchpage.html')
    
    searchin = searchin.split() 
    #split words
    
    searched_threads = []
    
    for word in searchin:
        if word[0] == '#':
            #if word is a tag, search through Tags
            word = word.strip('#')
            for tag in Tag.select().where(Tag.sharp == word):
                if tag.thread in searched_threads:
                    pass
                else:
                    searched_threads.append(tag.thread)

        else:
            #search through content in Pieces
            for piece in Piece.select().where(Piece.content.contains(word)):
                if piece.thread in searched_threads:
                    pass
                else:
                    searched_threads.append(piece.thread)
                    
            #search through thread titles
            for thread in Thread.select().where(Thread.title.contains(word)):
                searched_threads.append(thread)
    
    return render_template('searchpage.html', threads=searched_threads)
    

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
    
def splittags(tags):
    tags = tags.split('#')
    if tags[0] == '':
        tags.pop(0)
    for tags in tags:
        tag = tag.strip()
    return tags;    
    
if __name__ == "__main__":
    app.run(debug=True)