import pytest
from auction import Auction, AuctionError


@pytest.fixture
def auction():
    """Create an auction before each test. Minimum increament is 1"""
    return Auction("Test Auction")


@pytest.fixture
def auction_2():
    """Create an openned action with minimum increament of 50 highest bid as 100"""
    auction = Auction("Game\'s PS5", 50)
    auction.start()
    auction.bid("Jj", 100)
    return auction


def test_bid_new_auction(auction):
    """a new auction has no bids and bidding is disabled."""
    assert auction.best_bid() == 0
    assert auction.winner() == 'No Bids'


def test_first_bit(auction):
    """Bid with 0 plus minimum increment"""
    auction.start()
    auction.bid("Game", 1)
    assert auction.winner() == "Game"
    assert auction.best_bid() == 1


def test_bid_after_other_bidder(auction_2):
    """Bid after other user with highest bid plus minimum increment"""
    assert auction_2.winner() == "Jj"
    assert auction_2.best_bid() == 100
    auction_2.bid("Boom", 150)
    assert auction_2.winner() == "Boom"
    assert auction_2.best_bid() == 200


def test_bid_not_exceed_best_bid(auction_2):
    """Bid does not exceed or equal to highest bid plus minimum increment"""
    assert auction_2.winner() == "Jj"
    assert auction_2.best_bid() == 100
    with pytest.raises(AuctionError):
        auction_2.bid("Yanat", 120)
    assert auction_2.winner() == "Jj"
    assert auction_2.best_bid() == 100


def test_lower_than_or_equal_to_zero_bit_price(auction):
    """The bid price shouldn't lower than or equal to 0."""
    auction.start()
    with pytest.raises(ValueError):
        auction.bid("Negative Bid", -1)

    with pytest.raises(ValueError):
        auction.bid("Zero Bid", 0)


def test_closed_auction_bid(auction):
    """Bidder shouldn't be able to bid the closed auction."""
    auction.start()
    auction.bid("User1", 100)
    auction.stop()
    with pytest.raises(AuctionError):
        auction.bid("Closed", auction.best_bid() + auction.increment)


def test_bid_not_started_auction(auction):
    """Bidder shouldn't be able to bid the auction that not started yet."""
    with pytest.raises(AuctionError):
        auction.bid("Not started", auction.best_bid() + auction.increment)


def test_blank_bidder(auction):
    """The bid method requires a non-blank bidder name."""
    auction.start()
    with pytest.raises(ValueError):
        auction.bid(" ", 0)


def test_too_low_bid(auction):
    """The bid shouldn't below the increment."""
    auction.start()
    with pytest.raises(AuctionError):
        auction.bid("Bidder", 0.1)


def test_not_active_winner(auction):
    """The winner should show the winner name even inactive."""
    auction = Auction("Test Auction 2", 100)
    auction.start()
    auction.bid("Bidder 1", 100.50)
    auction.bid("Bidder 2", 200.50)
    auction.bid("Bidder 3", 400.50)
    auction.stop()
    assert auction.winner() == "Bidder 3"
