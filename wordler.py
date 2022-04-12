class Wordler():
	
	word_list = ["STARE", "SCARE", "WASTE", "GOING", "APPLE"]
	
	def __init__(self, answer=""):
		self.guesses = []
		self.answer = answer
	
	def set_answer(self, answer):
		self.answer = answer
	
	def get_answer(self):
		return self.answer
	
	def add_guess(self, guess):
		self.guesses.append(guess)		
	
	def compare_words(self, word_answer, word_guess):
		maxlen = max(len(word_answer), len(word_guess))
		comp = ["0"]*maxlen
		word_answer = word_answer.ljust(maxlen, "@")
		word_guess = word_guess.ljust(maxlen, "@")
		print (word_answer, word_guess)
		for i in range(maxlen):
			if word_guess[i] == word_answer[i]:
				comp[i] = "+"
			elif word_guess[i] in word_answer:
				comp[i] = "~"
			else:
				comp[i] = "-"
		return "".join(comp)
	
	def get_guesses(self):
		return self.guesses
	
	def get_comparisons(self):
		comparisons = [self.compare_words(self.answer, guess) for guess in self.guesses]
		return comparisons
	
	def get_guesses_comparisons(self):
		return zip(self.get_guesses(), self.get_comparisons())


