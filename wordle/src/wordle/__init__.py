import enum
from pathlib import Path
from quart import Quart, render_template, g, redirect, request, url_for
# from quart_schema import RequestSchemaValidationError
# from db import _get_db
import databases
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request
from sqlite3 import dbapi2 as sqlite3
from .helpers import save_words_in_database, valid_word


app = Quart(__name__)

def run() -> None:
    app.run()

app.config.update({
  "DATABASE": app.root_path / "wordle.db",
})

def _connect_db():
    engine = sqlite3.connect(app.config["DATABASE"])
    engine.row_factory = sqlite3.Row
    return engine

def init_db():
    db = _connect_db()
    with open(app.root_path / "schema.sql", mode="r") as file_:
        db.cursor().executescript(file_.read())
    save_words_in_database(db)

def _get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = _connect_db()
    return g.sqlite_db


@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        return redirect(url_for("wordguess"))
    else:
        db = _get_db()
        cur = db.execute(
            """
            SELECT * FROM all_words WHERE wid IN (SELECT wid FROM all_words ORDER BY RANDOM() LIMIT 1)
            """,
        )
        curr_word = cur.fetchone()

        print("NEW GAME: ", curr_word["word"])

        db.execute(
            """
            INSERT INTO used_words (wid,word,guess_count) VALUES (?,?,?)
            """,
            [curr_word["wid"], curr_word["word"], 0]
            )
        db.commit()

        # db.execute(
        #     """
        #     DELETE from all_words where wid = ?
        #     """,
        #     (curr_word["wid"],)
        #     )
        # db.commit()

        db.execute(
            """
            DELETE from guess_words
            """,
            )
        db.commit()

        return await render_template("index.html")


@app.route("/guess", methods=["GET", "POST"])
async def wordguess():
    db = _get_db()
    cur = db.execute(
        """
        SELECT * FROM guess_words
        """,
    )
    guess_words = cur.fetchall()
    guesses = []
    for guess in guess_words:
        guesses.append(guess["guess"])

    if request.method == "POST":
        cur = db.execute(
            """
            SELECT * FROM used_words WHERE uwid = (SELECT max(uwid) FROM used_words)
            """,
        )
        used_word = cur.fetchone()

        form = await request.form
        flag = 0
        for guess in guess_words:
            if form["guessword"] == guess["guess"]:
                flag = 1
                break

        if flag == 0 and valid_word(db, str(form["guessword"])):      
            db.execute(
                    """
                    INSERT INTO guess_words (guess) VALUES (?)
                    """,
                    [form["guessword"]]
                    )
            db.commit()
            cnt = used_word["guess_count"]+1
        else:
            cnt = used_word["guess_count"]
        print(cnt)
        db.execute(
            """
            UPDATE used_words SET guess_count=? WHERE uwid=?
            """,
            (cnt, used_word["uwid"])
            )
        db.commit()

        if form["guessword"] == used_word["word"]:
            db.execute(
                """
                UPDATE used_words SET status=? WHERE uwid=?
                """,
                ("win", used_word["uwid"])
                )
            db.commit()
            return redirect(url_for("winresult"))

        elif cnt == 6:
            db.execute(
                """
                UPDATE used_words SET status=? WHERE uwid=?
                """,
                ("exhaust", used_word["uwid"])
                )
            db.commit()

            # db.execute(
            #     """
            #     INSERT INTO all_words (word) VALUES (?)
            #     """,
            #     [used_word["word"]]
            #     )
            # db.commit()

            # db.execute(
            #     """DELETE from used_words where uwid = ?
            #     """,
            #     (used_word["uwid"],)
            #     )
            # db.commit()
            return redirect(url_for("gameresult", word=used_word["word"]))
        return redirect(url_for("wordguess", guesslist = guess_words))
    else:
        cur = db.execute(
            """
            SELECT * FROM used_words WHERE uwid = (SELECT max(uwid) FROM used_words)
            """,
        )
        used_word = cur.fetchone()
        flag = ''
        if len(guesses) != 0:
            temp = guesses[len(guesses)-1]
            for i,(x,y) in enumerate(zip(used_word["word"],temp)):
                if x == y:
                    flag = flag + '='
                elif y in used_word["word"]:
                    flag = flag + 'i'
                else:
                    flag = flag + 'o'
        db.execute(
            """
            UPDATE guess_words SET color=? WHERE wid = (SELECT max(wid) FROM guess_words)
            """,
            [flag]
            )
        db.commit()
        cur = db.execute(
            """
            SELECT * FROM guess_words
            """,
        )
        guess_words = cur.fetchall()
        return await render_template("wordguess.html", guesslist = guess_words)

@app.route("/result", methods=["GET", "POST"])
async def gameresult():
    if request.method == "POST":
        return redirect(url_for("index"))
    else:
        word = request.args["word"]
        db = _get_db()
        cur = db.execute(
            """
            SELECT * FROM guess_words
            """,
        )
        guess_words = cur.fetchall()
        return await render_template("result.html", word=word, guess_words=guess_words)

@app.route("/winresult", methods=["GET", "POST"])
async def winresult():
    if request.method == "POST":
        return redirect(url_for("index"))
    else:
        return await render_template("winner.html")


# async def _connect_db():
#     database = databases.Database(app.config["DATABASES"]["URL"])
#     await database.connect()
#     return database


# def _get_db():
#     if not hasattr(g, "sqlite_db"):
#         g.sqlite_db = _connect_db()
#     return g.sqlite_db


# @app.teardown_appcontext
# async def close_connection(exception):
#     db = getattr(g, "_sqlite_db", None)
#     if db is not None:
#         await db.disconnect()

