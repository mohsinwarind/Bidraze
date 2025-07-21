from django.contrib import admin
from .models import User, Category , AuctionListing, Bid , Comment  
# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'starting_bid', 'current_price', 'category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'is_active')
    ordering = ('-created_at',)

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'bid_amount', 'timestamp')
    search_fields = ('listing__title', 'bidder__username')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'commenter', 'content', 'timestamp')
    search_fields = ('listing__title', 'commenter__username', 'content')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)