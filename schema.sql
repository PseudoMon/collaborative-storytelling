DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS post;

CREATE TABLE threads (
    id integer primary key autoincrement,
    title text not null,
    pieces FOREIGN KEY,
}

CREATE TABLE post (
    id integer primary key autoincrement,
    content text not null,
    colour text not null,
    author string not null,
    datestamp date
)
    
    