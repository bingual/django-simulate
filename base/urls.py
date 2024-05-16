from django.contrib import admin
from django.urls import path, include
from django_nextjs.render import render_nextjs_page


async def root(request):
    return await render_nextjs_page(request)


urlpatterns = [
    path("", root),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("product/", include("product.urls")),
]
