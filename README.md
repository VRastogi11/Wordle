# Wordle

`pip3 install rich english_words random2`
`poetry add english-words`

Initialize db:
`poetry run init_db`

Run app:
`poetry run start`

Issue:
1. Delete the words from all_words database after it is used.
This is the problem when we need to check if the guess word is a valid word but still incorrect.
