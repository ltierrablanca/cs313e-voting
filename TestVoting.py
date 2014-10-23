# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from Voting import Candidate, Ballot, voting_read, det_winner, redis_votes

# -----------
# TestVoting
# -----------

class TestVoting (TestCase) :
    
    # -------------
    # Candidate
    # -------------

    def test_Candidate1 (self):
        c = Candidate("Jack", 1)
        self.assertEqual(c.name, "Jack")

    def test_Candidate2 (self):
        c = Candidate("Jack", 2)
        self.assertEqual(c.num, 2)

    def test_Candidate3 (self):
        c = Candidate("John Doe", 1)
        b = Ballot("1 2 3")
        c.addballot(b)
        self.assertEqual(c.ballots[0].votes, ['1', '2', '3'])

    def test_Candidate4 (self):
        c = Candidate("John", 1)
        b = Ballot("1 2 3")
        self.assertEqual(type(c.getnumvotes()), int)

    def test_Candidate5 (self):
        c = Candidate("John Doe", 1)
        b = Ballot("1 2 3")
        c.addballot(b)
        b = Ballot("1 3 2")
        c.addballot(b)
        self.assertEqual(c.ballots[1].votes, ['1', '3', '2'])

    def test_Candidate6 (self):
        c = Candidate("John Doe", 1)
        self.assertEqual(c.getnumvotes(), 0)

    def test_Candidate7 (self):
        c = Candidate("John Doe", 1)
        c.addballot(Ballot("1 2 3"))
        self.assertEqual(c.getnumvotes(), 1)

    def test_Candidate8 (self):
        c = Candidate("John Doe", 1)
        s = "Candidate 1, John Doe, has 0 votes."
        self.assertEqual(str(c), s)

    # -------------
    # Ballot
    # -------------

    def test_Ballot1 (self):
        b = Ballot("1 2 3")
        self.assertEqual(type(b.getchoice()), str)

    def test_Ballot2 (self):
        b = Ballot("1 2")
        b.adjustchoice()
        self.assertEqual(b.getchoice(), '2')

    def test_Ballot3 (self):
        b = Ballot("1 2 3 4 5 6")
        b.adjustchoice()
        b.adjustchoice()
        self.assertEqual(b.getchoice(), '3')

    def test_Ballot4 (self):
        b = Ballot("3 2 1 4")
        b.adjustchoice()
        b.adjustchoice()
        b.adjustchoice()
        self.assertEqual(b.getchoice(), '4')

    def test_Ballot5 (self):
        b = Ballot("1 2 3")
        self.assertEqual(str(b), '1 2 3')

    # --------------
    # voting_read
    # --------------

    def test_read1 (self):
        r = StringIO("1\n\n2\nJohn Johnson\nJane Smith\n1 2\n2 1\n1 2\n")
        w = StringIO()
        voting_read(r, w)
        self.assertEqual(w.getvalue(), 'John Johnson\n')

    def test_read2 (self):
        r = StringIO("1\n\n3\nJohn Johnson\nJane Smith\nBob Doe\n1 2 3\n2 1 3\n1 2 3\n2 1 3\n 3 1 2")
        w = StringIO()
        voting_read(r, w)
        self.assertEqual(w.getvalue(), 'John Johnson\n')

    def test_read3 (self):
        r = StringIO("1\n\n1\nJohn\n1\n")
        w = StringIO()
        voting_read(r,w)
        self.assertEqual(w.getvalue(), 'John\n')


    # --------------
    # det_winner
    # --------------

    def test_det_winner1 (self) :
        can = []
        c = Candidate("John Doe", 1)
        c.addballot(Ballot("1 2"))
        can.append(c)
        c = Candidate("Jane Johnson", 2)
        c.addballot(Ballot("2 1"))
        can.append(c)
        winner = det_winner(can, 2)
        self.assertEqual(winner, ['John Doe', 'Jane Johnson'])


    def test_det_winner2 (self) :
        can = []
        c = Candidate("John Doe", 1)
        c.addballot(Ballot("1 2"))
        c.addballot(Ballot("1 2"))
        can.append(c)
        c = Candidate("Jane Johnson", 2)
        c.addballot(Ballot("2 1"))
        can.append(c)
        winner = det_winner(can, 3)
        self.assertEqual(winner, ['John Doe'])

    def test_det_winner3 (self) :
        can = []
        c = Candidate("John Doe", 1)
        c.addballot(Ballot("1 2"))
        can.append(c)
        winner = det_winner(can, 1)
        self.assertEqual(winner, ['John Doe'])

    # -------------
    # redis_votes
    # -------------

    def test_redis_votes1 (self):
        can = []
        c = Candidate("John Doe", 1)
        c.addballot(Ballot("1 2 3 4"))
        c.addballot(Ballot("1 2 3 4"))
        can.append(c)
        c = Candidate("Jane Smith", 2)
        c.addballot(Ballot("2 1 3 4"))
        c.addballot(Ballot("2 1 3 4"))
        can.append(c)
        c = Candidate("Srihan Srihan", 3)
        c.addballot(Ballot("4 3 2 1"))
        can.append(c)
        c = Candidate("Jack Johnson", 4)
        c.addballot(Ballot("3 4 1 2"))
        can.append(c)
        can = redis_votes(can, 6)
        winners = []
        for c in can:
            winners.append(c.name)
        self.assertEqual(winners, ['John Doe', 'Jane Smith'])

    def test_redis_votes2 (self):
        can = []
        c = Candidate("John Doe", 1)
        c.addballot(Ballot("1 2 3"))
        c.addballot(Ballot("1 2 3"))
        can.append(c)
        c = Candidate("Jane Smith", 2)
        c.addballot(Ballot("2 1 3"))
        c.addballot(Ballot("2 1 3"))
        can.append(c)
        c = Candidate("Srihan Srihan", 3)
        c.addballot(Ballot("3 2 1"))
        can.append(c)
        can = redis_votes(can, 5)
        winners = []
        for c in can:
            winners.append(c.name)
        self.assertEqual(winners, ['John Doe', 'Jane Smith'])
        

# ----
# main
# ----

main()