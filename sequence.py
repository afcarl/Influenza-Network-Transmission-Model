from random import choice, random, randint, sample

class Sequence(object):
	"""
	The Sequence object is a container for a string along with some
	methods to act on it.
	"""
	def __init__(self, length=10, sequence=None):
		"""
		Initialize the sequence with a random sequence of length 10 if 
		sequence is not specified.

		Otherwise, initialize sequence with a sequence that is specified. 
		"""
		super(Sequence, self).__init__()
		if sequence == None:
			self.sequence = self.GenerateSequence(length)
		else:
			self.sequence = sequence

		self.length = len(self.sequence)

	def __repr__(self):
		return self.sequence
		
	def GenerateSequence(self, length):
		"""
		This method will generate a sequence, and set the Sequence object's 
		sequence to that sequence.
		"""
		sequence = ''
		for i in range(length):
			letter = choice(['A', 'T', 'G', 'C'])
			sequence += letter
		return sequence

	def SetSequence(self, sequence):
		"""Setter method for a segment's sequence."""
		self.sequence = sequence

	def GenerateAndSetSequence(self, length):
		"""
		Syntactic sugar for generating and setting the sequence
		of a virus.
		"""
		sequence = self.GenerateSequence(length)
		self.SetSequence(sequence)

	def Append(self, sequence):
		"""
		Appends a sequence to the 3' end of the segment's sequence.
		The 3' end is the right hand side of the sequence.
		"""
		self.sequence += sequence

	def GetSequence(self):
		return self.sequence

	def Mutate(self, start=None, end=None, num_positions=1):
		"""
		This method will randomly pick a letter in the segment's sequence,
		and proceed to mutate that letter.

		If you wish to mutate a specific region, then specify the "start" and
		"end" positions.

		If you wish to mutate more than 1 position in the specified region, 
		then specify the num_positions that you wish to mutate.
		"""

		def ChooseNewLetter(letter):
			"""
			This function chooses a new letter from ATGC that is
			different from the letter passed into the function.
			"""
			possible_letters = set(['A', 'T', 'G', 'C'])
			new_letter = choice(list(
				possible_letters.difference(set(letter))))

			return new_letter

		def ChoosePositions(start, end, num_positions):
			"""
			This function chooses n positions at random within
			range(start, end)
			"""
			return sample(range(start, end), num_positions)

		# If it is not specified where to start or end, or if one is specified
		# and the other isn't, then set the start to 0, and end to the length
		# of the sequence.
		if start == None or end == None:
			start = 0
			end = len(self.sequence)

		positions = ChoosePositions(start, end, num_positions)
		# print positions

		new_sequence = ''

		for i, letter in enumerate(self.sequence):
			if i in positions:
				new_sequence += ChooseNewLetter(letter)
			else:
				new_sequence += letter

		self.SetSequence(new_sequence)