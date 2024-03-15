import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
import telebot


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity


                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                       В наличии - {product.quantity}')

                            neworder = OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            telegram(neworder, cart_item)
                            product.save()


                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()



                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)


def telegram(neworder, cart_item):
    token = '6716144931:AAEb_gb6qe_PsSNyGOF1TITjFK1CH9Op0lY'
    chat = '1342409'
    message = f" Получатель: {neworder.order.user}\n" \
              f" Телефон: {neworder.order.phone_number}\n" \
              f" Товар: {cart_item.product.name}\n" \
              f" Цена: {cart_item.product.sell_price()}\n" \
              f" Кол-во: {cart_item.quantity}\n"

    now = datetime.datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    message += f"Дата: {date_str}\n"



    bot = telebot.TeleBot(token)

    try:
        bot.send_message(chat, "Новый заказ")
        bot.send_message(chat, message)
        print("Сообщение успешно отправлено")
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")