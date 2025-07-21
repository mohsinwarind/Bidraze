from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AuctionListingForm , BidForm, CommentForm
from .models import User,AuctionListing , Bid , Comment , Category
from django.contrib import messages

def index(request):
    listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.current_price = form.cleaned_data['starting_bid']
            listing.save()
            return redirect('index')
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {
        'form': form
    })
        
def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    bid_form = BidForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if "place_bid" in request.POST and listing.active:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_amount = bid_form.cleaned_data['bid_amount']
                if bid_amount >= listing.starting_bid and bid_amount > listing.current_price:
                    bid = bid_form.save(commit=False)
                    bid.listing = listing
                    bid.bidder = request.user
                    bid.save()
                    listing.current_price = bid_amount
                    listing.save()
                    messages.success(request, "Bid placed successfully!")
                else:
                    messages.error(request, "Bid must be at least the starting bid and greater than the current bid.")
        elif "add_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.commenter = request.user
                comment.save()
                messages.success(request, "Comment added successfully!")
        elif "add_watchlist" in request.POST:
            request.user.watchlist.add(listing)
            messages.success(request, "Listing added to your watchlist!")
        elif "remove_watchlist" in request.POST:
            request.user.watchlist.remove(listing)
            messages.success(request, "Listing removed from your watchlist!")
        elif "close_auction" in request.POST and request.user == listing.created_by:
            return close_auction(request, listing_id)

    comments = listing.comments.all()
    on_watchlist = request.user.is_authenticated and listing in request.user.watchlist.all()
    highest_bid = listing.bids.order_by('-bid_amount').first()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
        "on_watchlist": on_watchlist,
        "highest_bid": highest_bid,
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user
    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
        messages.success(request, "Removed from watchlist.")
    else:
        user.watchlist.add(listing)
        messages.success(request, "Added to watchlist.")
    return redirect('listing', listing_id=listing.id)

@login_required
def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = category.listings.filter(active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id, created_by=request.user)
    listing.active = False
    listing.save()

    # Get the highest bid if any
    highest_bid = listing.bids.order_by('-bid_amount').first()
    if highest_bid:
        messages.success(request, f"Auction closed! The winner is {highest_bid.bidder.username} with a bid of ${highest_bid.bid_amount}.")
    else:
        messages.success(request, "Auction closed with no bids.")

    return redirect('listing', listing_id=listing_id)