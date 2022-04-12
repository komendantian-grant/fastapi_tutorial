# wordle_app.py

from fastapi import FastAPI
from fastapi import Form
from fastapi.responses import HTMLResponse, Response
from fastapi.responses import RedirectResponse
from fastapi.requests import Request
import starlette.status as status

from wordler import Wordler
import random

app = FastAPI()

@app.on_event("startup")
async def startup_event():
	app.wordler = Wordler()
	answer = random.choice(Wordler.word_list)
	app.wordler.set_answer(answer)

@app.get("/")
async def main():
	content = """
<body>
<a href="/wordle/">Wordle game!</a>
</body>
"""
	return HTMLResponse(content=content)

def get_painted_guess(guess, comparison, answer):
	painted_guess = ""
	print (guess, comparison)
	for (g, c) in zip(guess, comparison):
		if c == "+":
			color = "green"
		elif c == "~":
			color = "orange"
		elif c == "-":
			color = "black"
		painted_guess += """<font color="%s">%s</font>""" % (color, g)
	if (guess == answer):
		painted_guess = "<u>"+painted_guess+"</u>"
	return painted_guess

@app.get("/wordle/")
async def wordle_get():
	print (app.wordler.get_guesses())
	print (app.wordler.get_comparisons())
	guesses_comparisons = app.wordler.get_guesses_comparisons()
	guesses_html = ""
	for (guess, comparison) in guesses_comparisons:
		guesses_html += get_painted_guess(guess, comparison, app.wordler.get_answer())
		guesses_html += "</br>"
	content = """
<body>
<font size="+3">
%s
</font>
<form action="/wordle/" method="post">
	<input type="text" name="guess">
	</br>
	<input type="submit" value="Guess">
</form>
<br>
<form action="/wordle_reset/" method="post">
	<input type="submit" value="New game">
</form>
</body>
""" % (guesses_html)	
	return HTMLResponse(content=content)


@app.post("/wordle/")
async def wordle_post(guess: str = Form("")):
	
	if guess:
		n = len(app.wordler.get_answer())
		if len(guess) > n:
			guess = guess[0:n]
		app.wordler.add_guess(guess.upper())
	
	return RedirectResponse('/wordle/', status_code=status.HTTP_302_FOUND)

@app.post("/wordle_reset/")
async def wordle_reset():
	app.wordler = Wordler()
	answer = random.choice(Wordler.word_list)
	app.wordler.set_answer(answer)
	return RedirectResponse('/wordle/', status_code=status.HTTP_302_FOUND)
