from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.forms import CommentForm
from product.models import Comment


# def index(request):
#
#     return HttpResponse("product page")


def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            # data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد. ممنون از ارسال نظر شما...')
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)