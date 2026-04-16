from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required

# Импорты для REST API
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer

# Твои модели
from .models import Category, Product, Review, Favorite, News, Advertisement 

# Твои формы
from .forms import ContactForm, ReviewForm, CartAddProductForm

# Логика корзины
from .cart import Cart

# --- КАТАЛОГ, ПОИСК И СОРТИРОВКА ---

def product_list(request, category_slug=None):
    """Список товаров с поиском, сортировкой, новостями и рекламой"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # 1. ПОИСК (Проверка параметра 'q' в URL)
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # 2. ФИЛЬТР ПО КАТЕГОРИЯМ
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # 3. СОРТИРОВКА (Проверка параметра 'sort' в URL)
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')
    else:
        # По умолчанию сортируем по названию или порядку в Meta
        products = products.order_by('name')

    # 4. ДОПОЛНИТЕЛЬНЫЙ КОНТЕНТ (Новости и Реклама)
    news = News.objects.all()[:3] 
    ads = Advertisement.objects.filter(is_active=True).order_by('-created_at')[:1]
    
    return render(request, 'shop/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'news': news,
        'ads': ads,
        'query': query,
        'current_sort': sort
    })

def product_detail(request, id, slug):
    """Детальная страница товара и отзывы"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    review_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = ReviewForm(data=request.POST)
            if review_form.is_valid():
                if Review.objects.filter(product=product, author=request.user).exists():
                    messages.error(request, 'Вы уже оставили отзыв на этот товар.')
                else:
                    new_review = review_form.save(commit=False)
                    new_review.product = product
                    new_review.author = request.user
                    new_review.save()
                    messages.success(request, 'Ваш отзыв успешно добавлен!')
                return redirect('shop:product_detail', id=id, slug=slug)
        else:
            review_form = ReviewForm()

    return render(request, 'shop/detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'average_rating': average_rating
    })

# --- ОБРАТНАЯ СВЯЗЬ ---

def contact_view(request):
    """Страница контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('shop:contact')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})

# --- ИЗБРАННОЕ ---

def add_to_favorite(request, product_id):
    """Добавить/Удалить из избранного"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Войдите, чтобы добавлять товары в избранное.')
        return redirect('account:login')
        
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f'Товар {product.name} добавлен в избранное.')
    else:
        favorite.delete()
        messages.info(request, f'Товар {product.name} удален из избранного.')
        
    return redirect('shop:product_list')

@login_required 
def favorite_list(request):
    """Список избранного"""
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'shop/favorites.html', {'favorites': favorites})

# --- REST API ---

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# --- КОРЗИНА ---

def cart_add(request, product_id):
    """Добавление товара в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    else:
        cart.add(product=product)
        
    messages.success(request, f'Товар {product.name} добавлен в корзину')
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    """Удаление из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    """Страница корзины"""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'shop/cart_detail.html', {'cart': cart})