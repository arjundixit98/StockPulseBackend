from django.shortcuts import render, redirect
from .models import WishList
from .forms import WishListForm
from django.shortcuts import get_object_or_404
# Create your views here.
stocks = [
  {
    "ticker": "SWIGGY.NS",
    "current_price": round(334.6499938964844,2),
    "day_percent_change": -2.85,
  },
  {
    "ticker": "AAPL",
    "current_price": round(241.83999633789062,2),
    "day_percent_change": 1.91
  },
  {
    "ticker": "GOOGL",
    "current_price": 170.27999877929688,
    "day_percent_change": 1.06
}

]

def index(request):
  wishlists = WishList.objects.all().order_by('-created_at')
  return render(request, 'index.html', {'wishlists':wishlists})


def wishlist_list(request):
  wishlists = WishList.objects.all().order_by('-created_at')
  return render(request, 'wishlist_list.html', {'wishlists':wishlists})

def wishlist_create(request):
  if request.method == 'POST':
    form = WishListForm(request.POST)
    if form.is_valid():
      wishlist = form.save(commit=False)
      wishlist.user = request.user
      wishlist.save()
      return redirect('wishlist_list')
  else:
    form = WishListForm()
    return render(request, 'wishlist_form.html', {'form': form})

def wishlist_edit(request, wishlist_id):
  wishlist = get_object_or_404(WishList, pk=wishlist_id, user=request.user)
  if request.method == 'POST':
    form = WishListForm(request.POST, instance=wishlist)
    if form.is_valid():
      wishlist = form.save(commit=False)
      wishlist.user = request.user
      wishlist.save()
      return redirect('wishlist_list')
  else:
    form = WishListForm(instance=wishlist)
    return render(request, 'wishlist_form.html', {'form':form})

def wishlist_delete(request, wishlist_id):
  wishlist = get_object_or_404(WishList, pk=wishlist_id, user=request.user)
  if request.method=='POST':
    wishlist.delete()
    return redirect('wishlist_list')
  else:
    return render(request, 'wishlist_confirm_delete.html', {'wishlist': wishlist})
