import pytest
from auction import Auction, AuctionError


@pytest.fixture
def auction():
    """Create an auction before each test."""
    return Auction("Test Auction")


def test_new_auction(auction):
    """a new auction has no bids and bidding is disabled."""
    assert auction.best_bid() == 0
    assert auction.winner() == 'No Bids'


def test_lower_than_or_equal_to_zero_bit_price(auction):
    """The bit price shouldn't lower than or equal to 0."""
    auction.start()
    with pytest.raises(ValueError):
        auction.bid("Negative Bid", -1)

    with pytest.raises(ValueError):
        auction.bid("Zero Bid", 0)


def test_jong_jai_fail(auction):
    """Test fail naja"""
    auction.bid("test", 20)
    assert auction.winner() == "test"
    assert auction.best_bid() == 20


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
        auction.bid(" ", 100)


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
