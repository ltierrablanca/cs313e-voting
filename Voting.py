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
        winners = det_winner(candidates, num_votes)
        for can in winners:
            w.write(can)
            w.write('\n')
        if((i + 1) != cases):
            w.write('\n')


# will determine the winner of the election and return it as a list
def det_winner(candidates, num_votes):
    assert len(candidates) != 0             #there must be at least one candidate
    assert num_votes != 0               #there must be at least one vote
    done = False
    while(not(done)):               #while not done
        can_votes = []
        winner = []
        num_candidates = len(candidates)
        for can in candidates:              #create can_votes, which contains the vote totals
        	can_votes.append(can.getnumvotes())
        top = max(can_votes)                #top has the highest vote count
        if(top > (num_votes / 2)):              #a candidate has over 50% of the votes
            index = can_votes.index(top)
            winner.append(candidates[index].name)               #winner now contains candidate with most votes
            assert len(winner) != 0             #winner must contain at least one name
            return winner
        elif(top == (num_votes / num_candidates)):              #all candidates are tied
            for can in candidates:
                winner.append(can.name)             #winner now contains all candidate names
            assert len(winner) != 0             #winner must contain at least one name
            return winner
        else:
            candidates = redis_votes(candidates, num_votes)             #redistribute the loser's votes


# will redistribute the ballots that chose the candidate with the least votes
def redis_votes(candidates, num_votes):
    assert len(candidates) != 0
    assert num_votes != 0
    can_votes = []
    for can in candidates:              #create list with all of the candidates' vote totals
        can_votes.append(can.getnumvotes())
    low = min(can_votes)                #low has the lowest vote count
    losers = []
    for can in candidates:              #remove losers from candidates and create a list with them
        if(can.getnumvotes() == low):
            losers.append(can)
    for can in losers:
        candidates.remove(can)
    ballots = []
    for can in losers:              #get all ballots that voted for the losers
        for b in can.ballots:
            ballots.append(b)
    for x in ballots:               #adjust the choice of all of the ballots that voted for losers
        x.adjustchoice()
    while(len(ballots) > 0):        #while there are ballots left to adjust
        for x in ballots:
            valid = False
            choice = x.getchoice()
            for can in candidates:
                if(choice == str(can.num)):             #if the adjusted ballot choice is a candidate
                    valid = True
                    can.addballot(x)                #give ballot to new candidate
                    ballots.remove(x)               #remove from ballots left to adjust
                    break
            if(not(valid)):             #havent found a valid candidate yet, adjust choice again
                x.adjustchoice()
    assert len(candidates) != 0
    return candidates
