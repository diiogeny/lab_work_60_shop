from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    add_to_cart,
    cart_view,
    remove_from_cart,
    create_order
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("add-to-cart/<int:pk>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart"),
    path("remove-from-cart/<int:pk>/", remove_from_cart, name="remove_from_cart"),
    path("create-order/", create_order, name="create_order"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


