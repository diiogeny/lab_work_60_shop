from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, CartItem, Order, OrderItem
from .forms import ProductForm, OrderForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | Q(category__icontains=query)
            ).filter(quantity__gte=1).order_by("category", "name")
        return Product.objects.filter(quantity__gte=1).order_by("category", "name")

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(product=product)
        if not created:
            if cart_item.quantity < product.quantity:
                cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')

def cart_view(request):
    cart_items = CartItem.objects.all()
    total = sum(item.total_price() for item in cart_items)
    return render(request, "products/cart.html", {"cart_items": cart_items, "total": total})

def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart')

def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            cart_items = CartItem.objects.all()
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                item.product.quantity -= item.quantity
                item.product.save()
            cart_items.delete()
            return redirect('product_list')
    return redirect('cart')
