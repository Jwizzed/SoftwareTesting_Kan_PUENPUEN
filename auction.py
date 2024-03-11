import re

class Auction:
    """An auction where people can submit bids for an item.

    One Auction instance is for bidding on a single item.

    Example:
    >>> auction = Auction("TDD with Python")
    >>> print("Minimum bid increment is", auction.increment)
    Minimum bid increment is 1
    >>> auction.start()
    >>> auction.bid("Jim", 250)
    >>> auction.bid("Harry", 300)
    >>> auction.bid(" biRd ", 400)
    >>> auction.best_bid()
    400
    >>> auction.winner()            # Bidder names are normalized
    'Bird'
    >>> auction.bid("Jim", 400.1)   # bid is less than best_bid + min_increment
    Traceback (most recent call last):
      ...
    auction.AuctionError: Bid is too low
    >>> auction.bid("", 1000)
    Traceback (most recent call last):
      ...
    ValueError: Missing bidder name
    >>> auction.is_active()
    True
    >>> auction.stop()               # bidding is not allowed now
    >>> auction.bid("Jim", 1000)
    Traceback (most recent call last):
      ...
    auction.AuctionError: Bidding not allowed now
    >>> auction.start()
    >>> auction.bid("mai", 402.50)
    >>> auction.best_bid()
    402.5
    >>> auction.winner()
    'Mai'
    """

    def __init__(self, auction_name: str, min_increment: float =1):
        """Create a new auction with given auction name.

           min_increment is the minimum amount that a new bid must
           exceed the current best bid.
        """
        self._name = auction_name
        self._bids = {"no bids": 0}
        self._increment = min_increment
        self._active = False
    
    @property
    def name(self):
        return self._name

    @property
    def increment(self) -> float:
        """The minimum increment that a new bid must exceed best bid."""
        return self._increment

    def start(self) -> None:
        """Enable bidding."""
        self._active = True

    def stop(self) -> None:
        """Disable bidding."""
        self._active = False

    def is_active(self) -> bool:
        """Query if bidding is enabled. Returns True if bidding enabled."""
        return self._active
    
    def bid(self, bidder_name: str, amount: float) -> None:
        """ 
        Submit a bid to this auction.

        bidder_name - name of bidder, a non-empty non-blank string.
               Names are converted to Title Case, and excess space
               inside and surrounding the string is removed.
               " harry   haCkeR " is normalized to "Harry Hacker"
        amount - amount (int or float) of this bid. Must be positive 
               and greater than previous best bid by at least a
               minimum bid increment, as described in class docstring.

        Returns:
            object: 

        Raises:
            TypeError if bidder_name or amount are incorrect data types.
            ValueError if bidder_name is only whitespace, or amount < 0.
            AuctionError if bidding disabled or bid amount is too low.
        """
        if not isinstance(bidder_name, str):
            raise TypeError("Bidder name must be a non-empty string")
        if not isinstance(amount, (int,float)):
            raise TypeError('Amount must be a number')
        if not self._active:
            raise AuctionError('Bidding not allowed now')
        if len(bidder_name) < 1:
            raise ValueError("Missing bidder name")
        if amount < 0:
            raise ValueError('Amount is invalid')
        # check if this is best bid so far
        if amount <= self.best_bid() + self.increment:
            raise AuctionError("Bid is too low")
        # fix case of letters and remove whitespace
        bidder_name = Auction.normalize(bidder_name)
        # Accept the bid!
        self._bids[bidder_name] = amount

    def best_bid(self) -> float:
        """Return the highest bid so far."""
        return max(self._bids.values())

    def winner(self):
        """Return name of person who placed the highest bid."""
        best = self.best_bid()
        for (bidder,bid) in self._bids.items():
            if bid == best: return bidder

    def __str__(self):
        """Return a string description for this auction."""
        return 'Auction for ' + self.name 

    def __repr__(self):
        """String form of a Python command to recreate the object."""
        return(f"Auction('{self.name}', min_increment={self.increment})")

    @classmethod
    def normalize(cls, name):
        """
        Remove excess white space and convert a name to title case.

        No need to write unittests for this.

        Examples:
        >>> Auction.normalize("KUNG FU  ")
        'Kung Fu'
        >>> Auction.normalize("KUNG-FU  ")
        'Kung-Fu'
        >>> Auction.normalize("   too    MuCh  SpacE")
        'Too Much Space'
        >>> Auction.normalize("noSpacE")
        'Nospace'
        >>> Auction.normalize("    ")
        ''
        """
        namewords = re.split("\\s+",name.strip())
        name = " ".join(namewords)
        return name.title()


class AuctionError(Exception):
    """
    Exception to raise when an invalid Auction action is performed.
    """
    # Superclass provides all the behavior we need, so nothing to add here.
    pass


