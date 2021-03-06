from random import choice, random, randint, sample

class Sequence(object):
	"""
	The Sequence object is the lowest level object in the viral simulator. 
	It provides a container for storing seed sequences for the viruses present
	in the environment. 

	This can be subclassed to store seed sequences for other viruses, rather 
	than using a generated sequence. 

	Note that when a virus replicates, the full sequence object is not copied 
	for each of its segments; rather, each segment only keeps track of the 
	mutations that have happened.
	"""
	def __init__(self, length=1000, sequence=None):
		"""
		Initialize the sequence with a random sequence of length 10 if 
		sequence is not specified.

		Otherwise, initialize sequence with a sequence that is specified. 
		"""
		super(Sequence, self).__init__()

		self.sequence = None

		if sequence == None:
			self.sequence = self.generate_sequence(length)
		else:
			self.sequence = None
			self.set_sequence(sequence)

	def __repr__(self):
		return self.sequence
		
	def generate_sequence(self, length):
		"""
		This method will generate a sequence, and set the Sequence object's 
		sequence to that sequence.
		"""
		sequence = ''
		for i in range(length):
			letter = choice(['A', 'T', 'G', 'C'])
			sequence += letter
		return sequence

	def set_sequence(self, sequence):
		"""Setter method for a segment's sequence."""

		if isinstance(seuqence, str):
			self.sequence = sequence
		else:
			raise TypeError('A string must be specified!')

