from random import random, randint, choice
from segment import Segment
from copy import deepcopy, copy
from host import Host
from datetime import datetime
from joblib import Parallel, delayed
from id_generator import generate_id
from multiprocessing import Pool
import ctypes

import hashlib

def _replicate(virus):
	"""
	This version of replicate is called in the Parallel delayed function, to 
	allow this to speed up the replication of viruses.
	"""
	return virus.replicate()

class Virus(object):
	"""
	The Virus class is at the third highest level in the viral simulator. The 
	Virus class is a metaphor for any pathogen; because this simulator is being
	written first for a Viral pathogen as opposed to a different one, we will 
	for now stick with the Virus class name. In the future, this will be 
	generalized to a generic Pathogen class.
	TODO: RENAME VIRUS CLASS TO PATHOGEN.

	----------

	ATTRIBUTES

	- STRING: id
		a unique identifier for the virus object, generated by concatenating a 
		random number with the current local time, and then hashing it.

	- LIST OF OBJECTS: segments 
		a list of viral Segment objects that belong to the virus.
	
	- VARIABLE: parent
		a variable that references another virus as its parent, if descended 
		from a single virus, or a tuple of two viruses, if it is a reassorted 
		progeny.
	
	- TUPLE: burst_size_range
		a two-tuple that specifies the minimum and maximum number of viruses 
		that come out of one replication cycle.

	- FLOAT: replication_time
	 	an integer that specifies how long it takes (in minutes) for one 
	 	replication cycle to take place.

	----------

	MAIN METHODS

	- mutate:
	 	a method that mutates all of the segments present in the virus 
	 	according to the mutation rate of the virus.

	- replicate: 
	 	a method that returns a copy of the virus. The mutate function is
	 	guaranteed to be called.

	- generate_progeny:
	 	a method that returns a list of progeny that were replicated out of the
	 	virus.

	The methods described above are the main and important methods; the other
	methods in this class are mostly helper methods that do getting/setting of 
	attributes (with type checking for setters).
	"""

	def __init__(self, creation_date, host, num_segments=2, \
		burst_size_range=(5, 10), replication_time=30):
		"""
		Initiailize the virus with 2 segments, with default segment length.
		"""
		super(Virus, self).__init__()

		self.id = generate_id()

		self.parent = None

		self.creation_date = creation_date

		self.segments = self.generate_segments(num_segments=num_segments)

		if type(host) != Host:
			raise TypeError('A Host object must be specified!')
		else:
			self.host = host
			host.add_virus(self)

		self.burst_size_range = None
		self.set_burst_size_range(burst_size_range)

		self.replication_time = None
		self.set_replication_time(replication_time)


	def __repr__(self):
		return str(self.id)

	def mutations(self):
		"""
		This method returns a list of dictionaries that have recorded the 
		mutations in the virus.
		"""
		mutations = []
		for segment in self.segments:
			mutations.append(segment.mutations)
		return mutations

	def sequence(self):
		"""
		This method returns the sequence of each of the segments of the virus.
		"""
		sequences = []
		for segment in self.segments:
			sequences.append(segment.compute_sequence())

		return sequences

	def mutate(self):
		"""
		This method will mutate all of the viral segments according to their 
		specified substitution rates.
		"""

		for segment in self.segments:
			segment.mutate()

	def burst_size(self):
		"""
		This method returns an integer number between the burst size range 
		values inclusive.
		"""
		return randint(self.burst_size_range[0], self.burst_size_range[1])

	def generate_progeny(self):
		"""
		This method replicates the virus according to the burst size, which is 
		specified by choosing an integer at random from the burst size range.
		"""
		burst_size = randint(self.burst_size_range[0], self.burst_size_range[1])
		
		# burst_size = 5

		# results = Parallel()(delayed(_replicate)(self) for i in range(burst_size))

		# print('Adding viruses to host %s' % id(self.host))

		progeny = []
		for i in range(burst_size):
			progeny.append(self.replicate())

		# self.host.add_viruses(results)

		return progeny

	def replicate(self):
		"""
		This method returns a deep copy of the virus chosen to replicate.

		mutate is guaranteed to be called, but not guaranteed to happen. 
		Whether a mutation occurs or not depends on the mutation rate of the 
		virus.
		"""
		new_virus = copy(self)
		new_virus.creation_date = self.host.environment.current_time
		new_virus.parent = self.id
		new_virus.id = generate_id()
		new_virus.mutate()
		# self.host.add_virus(new_virus)

		# Return statement included for the purposes of Parallel processing in 
		# the generate_progeny function.
		return new_virus


	def generate_segment(self, segment_number, substitution_rate=7E-3, \
		sequence=None, length=1800):
		"""
		This method creates a segment with the parameters passed in.
		"""
		segment = Segment(segment_number=segment_number, \
			substitution_rate=substitution_rate, sequence=sequence, length=length)

		return segment

	def generate_segments(self, num_segments):
		"""
		This method generates the specified number of segments.
		"""
		segments = []

		for i in range(num_segments):
			segments.append(self.generate_segment(segment_number=i))

		return segments

	def genome_length(self):
		"""
		This method returns the length of the virus genome, summed over all    
		segments in the viral genome.
		"""
		length = sum(segment.length for segment in self.segments)
		return length

	def set_burst_size_range(self, burst_size_range):
		"""
		This method will set the burst size range. The burst size range must
		be passed in as a two-element list or tuple, with minimum at the first 
		position, and maximum at the second position.
		"""
		if type(burst_size_range) not in [tuple, list]:
			raise TypeError("A tuple/list of two integers must be specified!")

		elif len(burst_size_range) != 2:
			raise ValueError("A two-element tuple/list must be specified!")

		elif type(burst_size_range[0]) != int or type(burst_size_range[1]) != int:
			raise TypeError("Integer values of burst sizes must be specified!")

		elif burst_size_range[0] > burst_size_range[1]:
			raise ValueError("The burst size range must be specified as (min, max)!")
		else:
			self.burst_size_range = burst_size_range

	def set_replication_time(self, replication_time):
		if type(replication_time) != int:
			raise TypeError('An integer number of minutes must be specified!')
		else:
			self.replication_time = replication_time

	def set_parent(self, parent_virus):
		"""This method records the ID of the virus' parent."""
		if parent_virus == None:
			self.parent = None
		elif not isinstance(parent_virus, Virus):
			raise TypeError('A Virus object must be specified!')
		else:
			self.parent = parent_virus

	def is_reassorted(self):
		"""This method returns the reassortant status of the virus."""
		if len(self.parent) == 2:
			return True

		elif len(self.parent) == 1:
			return False








