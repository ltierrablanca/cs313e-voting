# will simulate a candidate and keep track of the candidate's name, number of votes 
# it has and which ballots are currently choosing this candidate
class Candidate:

    def __init__ (self, name, num):
	    self.name = name
	    self.num = num
	    self.ballots = []

    # will return the current number of votes for the candidate
    def getvotes(self):
	    return len(self.ballots)

    def getname(self):
        return self.name

    def __str__ (self):
        return "Candidate " + str(self.num) + ", " + self.name + ", has " + str(self.getvotes()) + " votes."

# this class will simulate a ballot and keeps track of the current candidate choice
class Ballot:
    # constructor for ballot class
    def __init__(self, votes):
	    self.votes = votes.split()
	    self.choice = 0

    # will return the current choice on the ballot
    def getchoice(self):
    	return self.votes[self.choice]
    
    # will adjust the current choice on the ballot
    def adjustchoice(self):
    	self.choice += 1

    
# will read the input and build the ballot and candidate objects
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
        
        winner = det_winner(candidates, num_votes, num_candidates)
        for can in winner:
            print(can)
        if((i + 1) != cases):
            print()


# will determine the winner of the election
def det_winner(candidates, num_votes, num_candidates):
        all_votes = []
        winner = []
        for can in candidates:
        	all_votes.append(can.getvotes())
        top = max(all_votes)
        if(top > (num_votes / 2)):
            index = all_votes.index(top)
            winner.append(candidates[index].getname())
            return winner
        # elif(top == (num_votes / num_candidates)):
        #     for can in candidates:
        #         winner.append(can.getname())
        #         return 
        # else:
        #     losers = []
        #     for num in all_votes:
        #         if (top >= num):
        #             losers.append(num)



