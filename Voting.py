# will simulate a candidate and keep track of the candidate's name, number of votes 
# it has and which ballots are currently choosing this candidate
class Candidate:
    
    # constructor for the candidate class
    def __init__ (self, name, num):
	    self.name = name
	    self.num = num
	    self.ballots = []

    #will add a ballot object to a candidates ballots
    def addballot(self, ballot):
        self.ballots.append(ballot)

    # will return the current number of votes for the candidate
    def getnumvotes(self):
	    return len(self.ballots)

    # will return string version of the candidate
    def __str__ (self):
        return "Candidate " + str(self.num) + ", " + self.name + ", has " + str(self.getnumvotes()) + " votes."

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

    def __str__ (self):
        s = ""
        for i in range(len(self.votes) - 1):
            s = s + self.votes[i] + " "
        s = s + self.votes[len(self.votes) - 1]
        return s

    
# will read the input and build the ballot and candidate objects
def voting_read(r, w):
    line = r.readline()
    line = line.strip()
    cases = int(line)
    line = r.readline()
    for i in range(cases):              # run through all of the cases
        candidates = []
        line = r.readline()
        line = line.strip()
        num_candidates = int(line)
        for j in range(num_candidates):             # create candidate objects
            line = r.readline()
            line = line.strip()
            candidates.append(Candidate(line, j + 1))
        line = r.readline()
        line = line.strip()
        num_votes = 0
        while(line != ""):              # create ballot objects
            b = Ballot(line)
            choice = int(b.getchoice())
            candidates[choice - 1].addballot(b)
            num_votes += 1
            line = r.readline()
            line = line.strip() 
        winner = det_winner(candidates, num_votes, num_candidates)
        for can in winner:
            print(can)
        if((i + 1) != cases):
            print()


# will determine the winner of the election and return it as a list
def det_winner(candidates, num_votes, num_candidates):
    can_votes = []
    winner = []
    for can in candidates:
    	can_votes.append(can.getnumvotes())
    top = max(can_votes)
    if(top > (num_votes / 2)):              #candidate has over 50% of the votes
        index = can_votes.index(top)
        winner.append(candidates[index].name)
        return winner
    elif(top == (num_votes / num_candidates)):              #all candidates are tied
        for can in candidates:
            winner.append(can.name)
        return winner
    else:
        redis_votes(candidates, num_votes)


# will redistribute the ballots that chose a the candidate with the least votes
def redis_votes(candidates, num_votes):
    can_votes = []
    for can in candidates:              #create list with all of the candidates' vote totals
        can_votes.append(can.getnumvotes())
    low = min(can_votes)
    index = can_votes.index(low)
    loser = candidates.pop(index)
    ballots = loser.ballots
    for x in ballots:
        x.adjustchoice()
    while(len(ballots) != 0):
        for x in ballots:
            valid = False
            choice = x.getchoice()
            for can in candidates:
                if(choice == can.num):
                    valid = True
                    can.addballot(x)
                    ballots.remove(x)
                    break
            if(not(valid)):
                x.adjustchoice()
    det_winner(candidates, num_votes, len(candidates))
