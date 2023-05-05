from django.shortcuts import render, redirect
from .import models
from .forms import SearchForm
from telebot import TeleBot

bot = TeleBot ('6276022103:AAF5LDh29EYcSJ_Varyr94ejiYjySI1sgnI',parse_mode='HTML')
# Create your views here.
def homepage(request):
    all_products = models.Product.objects.all()
    search_bar = SearchForm()
    all_categories = models.Category.objects.all()

    context = {'products': all_products,
               'all_categories': all_categories,
               'form': search_bar}

    if request.method == "POST":
        product_find = request.POST.get('search_product')
        try:
            search_result = models.Product.objects.get(product_name=product_find)
            return redirect(f'/item/{search_result.id}')
        except:
            return redirect('/')
    return render(request, 'index.html', context)


# Получить определенный продукт
def get_exact_product(request, pk):
    product = models.Product.objects.get(id=pk)
    context={'product':product}
    if request.method == 'POST':
        models.UserCart.objects.create(user_id=request.user.id,
                                       user_product=product,
                                       user_product_quantity=request.POST.get('user_product_quantity'),
                                       total_for_product=int(request.POST.get('user_product_quantity'))*product.product_price)
        return redirect('/cart')

    return render(request, 'about_product.html', context)

def get_user_cart(request):
    user_cart= models.UserCart.objects.filter(user_id=request.user.id)
    total=sum([i.total_for_product for  i in user_cart ])
    context={'cart':user_cart,'total':total}
    return render(request,'user_cart.html',{'cart':user_cart})

def exact_category(request,pk):
    exact_category = models.Category.objects.get(id=pk)
    categories=models.Category.objects.all()
    category_products = models.Product.objects.filter(product_category=exact_category)
    return render(request,'categrory_products.html',{'category_products': category_products,
                                                    'categories':categories})




#Ofomleniye zakaza
def complete_order(request):
    #poluchayem korzinu
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)

    #Formiruyem soobsheniye dlya tg admina
    result_message='Noviy zakaz(Sayt)\n\n'
    total_for_all_cart=0
    for cart in user_cart:
        result_message+=f'<b>{cart.user_product}</b> x {cart.user_product_quantity} = {cart.total_for_product} сум\n'

        total_for_all_cart += cart.total_for_product

    result_message+=f'\n----------\n<b>Itogo: {total_for_all_cart} sum</b>'


    #Otpravlyayem adminu soobsheniy v tg
    bot.send_message(1321230134, result_message)

    return redirect('/')