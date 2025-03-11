from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentPostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

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

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month = month,
                             publish__day = day)
    # Список активных комментариев к посту. Вызываем через менеджера
    comments = post.comments.filter(active=True)
    
    form = CommentPostForm()
    
    return render(request=request, template_name='blog/post/detail.html', context={'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                              id=post_id,
                              status=Post.Status.PUBLISHED)
    
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} порекомендовал вам прочитать пост" \
                f"{post.title}"
            message = f"Прочти {post.title} {post_url}\n\n" \
                f"{cd['name']} оставил вам следующий комментарий: {cd['comments']}"
            send_mail(subject=subject, message=message, from_email='vvvanusha62@mail.ru', recipient_list=[cd['to']])
            
            sent = True
    else:
        form = EmailPostForm()
    return render(request=request, template_name="blog/post/share.html", context={'form': form, 'post': post, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentPostForm(data=request.POST)
    if form.is_valid():
        # Создали объект комментарии без сохранения в бд, чтобы потом присвоить post, а затем сохранить
        comment = form.save(commit=False)
        
        comment.post = post
        
        comment.save()
    return render(request=request,
                  template_name='blog/post/comment.html',
                  context={
                      "post": post,
                      "form": form,
                      "comment": comment
                  })
    
        
    