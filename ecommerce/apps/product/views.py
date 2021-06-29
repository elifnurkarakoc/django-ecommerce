import random
import mimetypes
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddToCartForm
from .models import Category, Product
from apps.cart.cart import Cart
from django.http import HttpResponse, FileResponse
from django.conf import settings


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search.html', {'products': products, 'query': query})


def product(request, category_slug, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product has been added to the cart.')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    return render(request, 'product/product.html',
                  {'form': form, 'product': product, 'similar_products': similar_products})


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'product/category.html', {'category': category})


""" def download_file(request):
    product = get_object_or_404(Product)

    fl_path = settings.MEDIA_ROOT + product.pdf_file
    file_name = str(product.pdf_file).replace('/uploads', '')

    fl = open(fl_path, 'r')
    mime_type = mimetypes.guess_type(settings.MEDIA_ROOT)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response """