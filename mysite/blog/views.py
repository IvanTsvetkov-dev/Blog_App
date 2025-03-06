from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    posts = Post.published.all()
    page_number = request.GET.get('page', 1) # Извлечение GET параметра. Если параметр отсутствует, то туда записывается стандратное значение 1
    # Постраничная разбивка 3 постами на страницу
    paginator = Paginator(posts, 2)
    try:
        post = paginator.page(page_number)
    except EmptyPage:
        post = paginator.page(paginator.num_pages) # paginator.num_pages возвращает количество страниц. Это означает, что если пользователь введёт в query параметрах page >, чем возможно, то его перенаправит на самую последнюю страницу
    except PageNotAnInteger:
        post = paginator.page(1)
    return render(request=request, template_name='blog/post/list.html', context={'posts': post})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month = month,
                             publish__day = day)
    return render(request=request, template_name='blog/post/detail.html', context={'post': post})
    