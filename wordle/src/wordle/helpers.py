from english_words import english_words_set
from sqlite3 import dbapi2 as sqlite3
from quart import abort

def valid_word(db, word:str):
    cur = db.execute(
        """
        SELECT * FROM all_words
        """,
    )
    all_words = cur.fetchall()
    wordlist = []
    for i in all_words:
        wordlist.append(i["word"])
    return word in wordlist

def save_words_in_database(db):
    word_list = list(english_words_set)
    for i in range(len(word_list)):
        word_list[i] = word_list[i].lower()
    word_list = [*set(word_list)]

    for word in word_list:
        if len(word) == 5:
            try:
                db.execute("INSERT INTO all_words (word) VALUES (?)",
                        [word.lower()])
                db.commit()
                i = i + 1
            except sqlite3.IntegrityError as e:
                abort(409, e)
