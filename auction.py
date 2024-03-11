import re


class Auction:
    """An auction where people can submit bids for an item.

    One Auction instance is for bidding on a single item.
    """

    def __init__(self, auction_name: str, min_increment: float = 1):
        """Create a new auction with a given auction name and minimum increment."""
        self._name = auction_name
        self._bids = {"no bids": 0}
        self._increment = min_increment
        self._active = False

    @property
    def name(self):
        """Return the name of the auction."""
        return self._name

    @property
    def increment(self) -> float:
        """Return the minimum increment that a new bid must exceed the best bid."""
        return self._increment

    def start(self) -> None:
        """Enable bidding."""
        self._active = True

    def stop(self) -> None:
        """Disable bidding."""
        self._active = False

    def is_active(self) -> bool:
        """Return True if bidding is enabled."""
        return self._active

    def bid(self, bidder_name: str, amount: float) -> None:
        """Submit a bid to this auction."""
        if not isinstance(bidder_name, str):
            raise TypeError("Bidder name must be a non-empty string")
        if not isinstance(amount, (int, float)):
            raise TypeError('Amount must be a number')
        if not self._active:
            raise AuctionError('Bidding not allowed now')
        if len(bidder_name.strip()) == 0:
            raise ValueError("Missing bidder name")
        if amount <= 0:
            raise ValueError('Amount must be positive')
        if amount < self.best_bid() + self.increment:
            raise AuctionError("Bid is too low")

        bidder_name = Auction.normalize(bidder_name)
        self._bids[bidder_name] = amount

    def best_bid(self) -> float:
        """Return the highest bid so far."""
        return max(self._bids.values())

    def winner(self):
        """Return the name of the person who placed the highest bid."""
        best = self.best_bid()
        for bidder, bid in self._bids.items():
            if bid == best:
                return Auction.normalize(bidder)

    def __str__(self):
        """Return a string description for this auction."""
        return 'Auction for ' + self.name

    def __repr__(self):
        """Return a string form of a Python command to recreate the object."""
        return (f"Auction('{self.name}', min_increment={self.increment})")

    @classmethod
    def normalize(cls, name):
        """Remove excess white space and convert a name to title case."""
        namewords = re.split("\\s+", name.strip())
        name = " ".join(namewords)
        return name.title()


class AuctionError(Exception):
    """Exception to raise when an invalid Auction action is performed."""
    pass
