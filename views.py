# INSTALLATION:
#     pip install paypalrestsdk
# SETTINGS.PY (PayPal api credentials):
#     PAYPAL_CLIENT_ID = 'your_paypal_client_id'
#     PAYPAL_SECRET = 'your_paypal_secret'
# HTML FILES :
#     payment_success.html
#     payment_cancel.html
#     payment_form.html
# URLS.PY :
#     path('create-payment/', create_payment, name='create-payment'),
#     path('execute-payment/', execute_payment, name='execute-payment'),
# VIEWS.PY :
#     COPY THE CODE BELOW
# USAGE :
#     Run the server and go to create-payment/


import paypalrestsdk
from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.conf import settings

def create_payment(request):
    paypalrestsdk.configure({
        "mode": "sandbox",  # Change to "live" for production
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_SECRET
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://example.com/return",
            "cancel_url": "http://example.com/cancel"
        },
        "transactions": [{
            "amount": {
                "total": "10.00",  # Total amount
                "currency": "CAD"
            },
            "description": "Payment description"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return HttpResponseRedirect(link.href)
    else:
        return HttpResponseServerError("Failed to create payment: %s" % payment.error)

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        return HttpResponseRedirect("http://example.com/payment-success")
    else:
        return HttpResponseServerError("Failed to execute payment: %s" % payment.error)
