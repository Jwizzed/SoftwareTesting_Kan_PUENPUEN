"""Tests of the Auction class.

Author: your name
"""
import unittest
from auction import Auction, AuctionError


class AuctionTest(unittest.TestCase):
    """Tests of the Auction class."""

    def setUp(self):
        """Create an auction before each test."""
        self.auction = Auction("Test Auction")

    def test_new_auction(self):
        """a new auction has no bids and bidding is disabled."""
        self.assertEqual(0, self.auction.best_bid())
        self.assertEqual('no bids', self.auction.winner())

    def test_lower_than_or_equal_to_zero_bit_price(self):
        """The bit price shouldn't lower than or equal to 0."""
        self.auction.start()
        with self.assertRaises(ValueError):
            self.auction.bid("Negative Bid", -1)

        with self.assertRaises(ValueError):
            self.auction.bid("Zero Bid", 0)

    def test_closed_auction_bid(self):
        """Bidder shouldn't be able to bid the closed auction."""
        self.auction.start()
        self.auction.bid("User1", 100)
        self.auction.stop()
        with self.assertRaises(AuctionError):
            self.auction.bid("Closed", self.auction.best_bid() +
                             self.auction.increment)

    def test_bid_not_started_auction(self):
        """Bidder shouldn't be able to bid the auction that not started yet."""
        with self.assertRaises(AuctionError):
            self.auction.bid("Not started", self.auction.best_bid() +
                             self.auction.increment)

    def test_blank_bidder(self):
        """The bid method requires a non-blank bidder name."""
        self.auction.start()
        with self.assertRaises(ValueError):
            self.auction.bid(" ", 100)

    def test_too_low_bid(self):
        """The bid shouldn't below the increment."""
        self.auction.start()
        with self.assertRaises(AuctionError):
            self.auction.bid("Bidder", 0.1)

    def test_not_active_winner(self):
        """The winner should show the winner name even inactive."""
        self.auction = Auction("Test Auction 2", 100)
        self.auction.start()
        self.auction.bid("Bidder 1", 100.50)
        self.auction.bid("Bidder 2", 200.50)
        self.auction.bid("Bidder 3", 400.50)
        self.auction.stop()
        self.assertEqual("Bidder 3", self.auction.winner())
