class Host(object):
	"""
	The Host exists within the environment.

	The host exists to allow viruses to replicate within it.

	One host can have many viruses, replicating and mutating within it.

	When a Sampler samples something, it will sample the host and grab one 
	of the many viral particles present inside the host. That virus is then
	sequenced, and used for reconstruction.
	"""
	def __init__(self, id, infected_by=None):
		super(Host, self).__init__()
		self.id = id

		self.infected_by = None

		self.viruses = []

	def __repr__(self):
		return "Host %s infected with %s viruses." % (self.id, \
			len(self.viruses))
	
	def SetInfectedBy(self, other_host):
		"""
		This method will set the "infected_by" variable to the source of the 
		virus for the host.
		"""
		if type(other_host) != Host:
			raise TypeError('A Host object must be specified!')
		else:
			self.infected_by = other_host

	def IsInfected(self):
		"""
		This method checks the length of the viruses list to see if the host
		was infected with virus or not.
		"""
		if len(self.viruses) == 0:
			return False
		else:
			return True

	def AddVirus(self, virus):
		# The following line has to be placed inside here, in order to make 
		# the code work.
		from virus import Virus
		"""
		This method adds a virus to the list of viruses present in the host.
		"""
		if isinstance(virus, Virus):
			self.viruses.append(virus)
		else:
			raise TypeError('A Virus object must be specified!')

	def GetViruses(self):
		"""
		This method gets the list of viruses present in the host.
		"""
		return self.viruses

	def RemoveVirus(self, virus):
		"""
		This method exists for the purpose of removing a virus from a host
		during a transmission event. The particular viral particle goes
		away, though the particle's descendents or ancestors may still
		remain inside the host.
		"""
		from virus import Virus:
		if isinstance(virus, Virus):
			self.viruses.pop(self.viruses.index(virus))
		else:
			raise TypeError('A Virus object must be specified!')

