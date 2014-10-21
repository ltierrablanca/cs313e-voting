class Candidate:

	def __init__ (self, name, num):
	    self.name = name
	    self.num= num
	    self.ballots = []

	def getvotes(self):
		return len(self.ballots)

	def __str__ (self):
		return "Candidate " + str(self.num) + ", " + self.name + ", has " + str(self.getvotes()) + " votes."


class Ballot:

    def __init__(self, votes):
	    self.votes = votes.split()
	    self.choice = 0

    def getchoice(self):
    	return self.votes[self.choice]

    def adjustchoice(self):
    	self.choice += 1

    def __str__(self):
    	return str(self.votes)

# candidates = []

# for i in range(num_candidates):
# 	s = r.readline()
# 	s = s.strip()
# 	x = Candidate(s, i)
# 	candidates.append(x)
	
# for i in range(num_ballots):
# 	s = r.readline()
# 	s = s.strip()
# 	x = Ballot(s)
# 	choice = x.getchoice()
# 	candidates[choice - 1].ballots.append(x)
# 	numvotes += 1





#this method will do all of reading

def voting_read(r, w):
    line = r.readline()
    line = line.strip()
    cases = int(line)
    line = r.readline()

    for i in range(cases):
        candidates = []
        line = r.readline()
        line = line.strip()
        num_candidates = int(line)
        for j in range(num_candidates):
            line = r.readline()
            line = line.strip()
            candidates.append(Candidate(line, j + 1))

        line = r.readline()
        line = line.strip()
        num_votes = 0
        while(line != ""):
            b = Ballot(line)
            choice = int(b.getchoice())
            candidates[choice - 1].ballots.append(b)
            num_votes += 1
            line = r.readline()
            line = line.strip() 
        
        for can in candidates:
        	print(str(can))




