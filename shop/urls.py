
from django.urls import include, path
from shop import views

app_name = "shop"
urlpatterns = [
    path("", views.product_list, name = "shop"),
    path("adminshop/add", views.ProductPostSerializer.as_view(), name = "postshop"),
    path("shop/add", views.add_product, name = "addproduct"),
    path("adminshop/category", views.CategoryAddSerializer.as_view(), name = "postcategory"),
    path("shop/<slug:category_slug>/", views.product_list, name = "product_list_by_category"),
    path("<int:id>/<slug:slug>/detail/", views.product_detail, name = "product_detail"),
    path("search/" ,views.post_search, name = "post_search"),
    path("contactus/" ,views.contact_us, name = "contact"),
]
