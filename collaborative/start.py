from flask import Flask, render_template, url_for, json, request, redirect
import datetime

app = Flask(__name__)
title = "An Open Space"
# ###Data schema
# [thread, thread, thread]
# thread = {id: int, title: string, pieces: [piece, piece, piece]}
# piece = {id: int, content: string, colour: string, author: string, date: dateobject?}

@app.route('/')
def front_page():
	threads = retrieve_threads()
	threads = isotopydate(threads)
	return render_template('index.html', threads=threads)
	
@app.route('/about')
def about_page():
	return render_template('about.html')
	
@app.route('/newpiece', methods=['POST'])
def new_piece():
	threads = retrieve_threads()
	
	threadid = request.form['threadid']
	pieceid = request.form['pieceid']
	author = request.form['author']
	date = getdate()
	content = request.form['content']
	colour = request.form['colour']
	
	if author == "":
		author = "Anonymous"
	
	threadid = int(threadid)
	pieceid = int(pieceid)
	
	piece = {'id': pieceid, 'content': content, 'colour': colour, 'author': author, 'date': date}	
	threadid = threadid - 1
	threads[threadid]['pieces'].append(piece)
	
	save_threads(threads)
	
	return redirect(url_for('front_page'))
	
@app.route('/newthread', methods=['GET', 'POST'])
def new_thread():
	threads = retrieve_threads()
	threadid = len(threads) + 1
	
	datestamp = getdate()
	
	if request.method == 'GET':
		return render_template('newthread.html', threads=threads, date=datestamp)
	
	title = request.form['title']
	author = request.form['author']
	date = getdate()
	content = request.form['piececontent']
	colour = request.form['colour']
	
	if title == "":
		title = "Untitled"
	if author == "":
		author = "Anonymous"
	
	piece = {'id': 1, 'content': content, 'colour': colour, 'author': author,
	'date': date}
	thread = {'id': threadid, 'title': title, 'pieces': [piece]}
	threads.append(thread)
	
	save_threads(threads)
	
	return redirect(url_for('front_page'))
	
def retrieve_threads():
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
	d = datetime.date.today()
	d = d.isoformat()
	return d
	
def isotopydate(threads):
	for thread in threads:
		for piece in thread['pieces']:
			piece['date'] = datetime.datetime.strptime(piece['date'], '%Y-%m-%d')
			
	return threads