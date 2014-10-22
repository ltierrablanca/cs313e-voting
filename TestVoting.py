#!/usr/bin/env python3

# -------------------------------
# projects/collatz/TestCollatz.py
# Copyright (C) 2014
# Glenn P. Downing
# -------------------------------

# -------
# imports
# -------

from unittest import main, TestCase

from Voting import Candidate, Ballot, det_winner, redis_votes

# -----------
# TestVoting
# -----------

class TestVoting (TestCase) :
    
    # -------------
    # Ballot
    # -------------

    def test_Ballot1 (self):
        b = Ballot("1 2 3")
        self.assertEqual(str(b), "1 2 3")

    def test_Ballot2 (self):
        b = Ballot("1 2 3")
        self.assertEqual(b.getchoice(), '1')
    
    # -------------
    # Candidate
    # -------------

    # def test_Candidate1 (self):
    #     c = Candidate("John Doe", 1)
    #     b = Ballot("1 2 3")
    #     can.addballot(b)

    

    # def test_det_winner1 (self) :


    # def test_redis_votes1 (self):
        

# ----
# main
# ----

main()