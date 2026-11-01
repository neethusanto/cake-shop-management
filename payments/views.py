from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import hmac
import hashlib
from .models import Payment
from orders.models import Order


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={'user': request.user, 'amount': order.total_amount}
    )

    # Try to create Razorpay order if key is configured
    razorpay_order_id = None
    razorpay_key = settings.RAZORPAY_KEY_ID

    try:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_in_paise = int(order.total_amount * 100)
        rzp_order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': f'order_{order.pk}',
        })
        payment.razorpay_order_id = rzp_order['id']
        payment.save()
        razorpay_order_id = rzp_order['id']
    except Exception:
        # Razorpay not available – use demo/COD flow
        pass

    return render(request, 'payments/payment.html', {
        'order': order,
        'payment': payment,
        'razorpay_key': razorpay_key,
        'razorpay_order_id': razorpay_order_id,
    })


@login_required
def payment_success_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order)
    payment_id = request.GET.get('razorpay_payment_id', '')
    signature = request.GET.get('razorpay_signature', '')

    if payment_id:
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = 'success'
        payment.save()
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()
        messages.success(request, f'Payment successful! Order #{order.order_number} confirmed.')
    return render(request, 'payments/payment_success.html', {'order': order, 'payment': payment})


@login_required
def cod_payment_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment, _ = Payment.objects.get_or_create(
        order=order,
        defaults={'user': request.user, 'amount': order.total_amount}
    )
    payment.payment_method = 'cod'
    payment.status = 'pending'
    payment.save()
    order.payment_status = 'pending'
    order.status = 'confirmed'
    order.save()
    messages.success(request, f'Order #{order.order_number} placed with Cash on Delivery!')
    return redirect('payments:success', order_id=order.pk)


@csrf_exempt
def razorpay_webhook_view(request):
    if request.method == 'POST':
        try:
            payload = request.body
            sig_header = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
            webhook_secret = settings.RAZORPAY_KEY_SECRET
            generated_signature = hmac.new(
                webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
            if hmac.compare_digest(generated_signature, sig_header):
                data = json.loads(payload)
                if data.get('event') == 'payment.captured':
                    payment_entity = data['payload']['payment']['entity']
                    try:
                        payment = Payment.objects.get(razorpay_payment_id=payment_entity['id'])
                        payment.status = 'success'
                        payment.save()
                        payment.order.payment_status = 'paid'
                        payment.order.status = 'confirmed'
                        payment.order.save()
                    except Payment.DoesNotExist:
                        pass
        except Exception:
            pass
    return JsonResponse({'status': 'ok'})
