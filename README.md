# An Open Space
An experiment. Supposedly  a website to write collaborative story, mostly anonymously. In development/experimentation/I dunno. 

Idk, man. I'm just learning how to use git, web development, database management, and web design at the same time.

### Data schema
- [thread, thread, thread]
- thread = {id: int, title: string, pieces: [piece, piece, piece]}
- piece = {id: int, content: string, colour: string, author: string, date: dateobject?}

## Issues:
- I'm using Windows to develop this. Why am I using Windows
- Can't use the same database locally
- app.config['DATABASE'] is useless because I can't use it on schema.py (circular import issues) 

## To-Do:
- Archive page, individual thread page
- Ability to delete own post.
- Using cookies to store name + associated colour.
- A discussion room per story thread
- Tags per story thread (+ ability to sort by tags)
