from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """User model - inherited from Django implementation"""
    pass

class Auction(models.Model):
    """All info about one auction:
    * auction title
    * auction description
    * seller
    * current price
    * when auction was publicated
    * auction's category
    * auction image URL
    * is auction ended?
    """

    # Categories - choices
    CARS = "CARS"
    FASHINON = "FAS"
    ELECTRONICS = "ELE"
    ARTS = "ART"
    HOME_GARDES = "HGA"
    SPORTING_GOODS = "SPO"
    TOYS = "TOY"

    CATEGORY = [
        (CARS, "Cars"),
        (FASHINON, "Fashion"),
        (ELECTRONICS, "Electronics"),
        (ARTS, "Arts"),
        (HOME_GARDES, "Home & Garden"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOYS, "Toys"),
    ]

    # Model fields
    # auto: auction_id
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    category = models.CharField(max_length=4, choices=CATEGORY, default=CARS)
    image_url = models.URLField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "auction"
        verbose_name_plural = "auctions"

    def __str__(self):
        return f"Auction id: {self.id}, title: {self.title}, seller: {self.seller}"

class Bid(models.Model):
    """Bid model contains all info about single bid:
    * price
    * seller
    * when
    * on what auction
    """

    # Model fields
    # auto: bid_id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = "bid"
        verbose_name_plural = "bids"

    def __str__(self):
        return f"{self.user} bid {self.bid_price} $ on {self.auction}"

class Comment(models.Model):
    """Comment model contains all info about single comment
    * content
    * who posted
    * when
    * on what auction
    """

    # Model fields
    # auto: comment_id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"Comment {self.id} on auction {self.auction} made by {self.user}"

class Watchlist(models.Model):
    """Watchlist model contains all info about object on watchlist
    * which auction is on watchlist
    * on whose watchlist this auction is
    """

    # Model field
    # auto: watchlist_id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"
        # Forces to not have auction duplicates for one user
        unique_together = ["auction", "user"]

    def __str__(self):
        return f"{self.auction} on user {self.user} watchlist"