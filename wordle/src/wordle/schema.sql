DROP TABLE IF EXISTS auth;
CREATE TABLE auth(
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    uname VARCHAR UNIQUE, 
    'pwd' VARCHAR
    );

DROP TABLE IF EXISTS all_words;
CREATE TABLE all_words(
    wid INTEGER PRIMARY KEY AUTOINCREMENT,
    word VARCHAR UNIQUE
    );

DROP TABLE IF EXISTS used_words;
CREATE TABLE used_words(
    uwid INTEGER PRIMARY KEY AUTOINCREMENT,
    wid INTEGER,
    word VARCHAR UNIQUE,
    uid INTEGER,
    guess_count INTEGER,
    status TEXT,
    FOREIGN KEY (wid) REFERENCES all_words(wid),
    FOREIGN KEY (word) REFERENCES all_words(word),
    FOREIGN KEY (uid) REFERENCES auth(uid)
    );

DROP TABLE IF EXISTS guess_words;
CREATE TABLE guess_words(
    wid INTEGER PRIMARY KEY AUTOINCREMENT,
    guess VARCHAR,
    color VARCHAR
    );

