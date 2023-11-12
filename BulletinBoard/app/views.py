from django.shortcuts import render, redirect
from django.views import View # Импортируем простую вьюшку
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from datetime import datetime, timedelta, time
from django.utils import timezone 
from .models import User, Post, Category, Response
from django.core.paginator import Paginator # Импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .filters import PostFilter # импортируем недавно написанный фильтр
from .forms import PostForm, ResponseForm # импортируем нашу форму

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import mail_managers

# дженерик для удаления
class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
   template_name = 'app/post_delete.html'
   queryset = Post.objects.all()
   success_url = reverse_lazy('app:feed') # не забываем импортировать функцию reverse_lazy из пакета django.urls
   permission_required = ('app.delete_post')

# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
   template_name = 'app/post_update.html'
   form_class = PostForm
   success_url = reverse_lazy('app:feed')
   permission_required = ('app.change_post')
   
   # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
   def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)
   

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
   template_name = 'app/post_create.html'
   form_class = PostForm
   permission_required = ('app.add_post')
   

   def form_valid(self, form):
        # form.data['user'] = self.request.user
        result = super().form_valid(form)
        if form.is_valid():
            print("This is my newly created post", self.object.pk)
        
        return result

   def post(self, request, *args, **kwargs):
        # self.object = self.get_object() # assign the object to the view
        # form = self.get_form()
        
        form = self.form_class(request.POST, request.FILES) # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            # user = User.objects.get(pk=request.user)
            # request.POST['user'] = request.user.id
            # form.data['user'] = request.user
            post = form.save(commit=False)
            post.user = User.objects.get(username = self.request.user)
            if 'image' in request.FILES.keys():
                post.image = request.FILES['image']
            post.save()
            # Проверка на максимум постов автора в день
            # today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
            # today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
            # user = User.objects.get(pk=request.POST['user'])
            # posts_for_today = Post.objects.filter(date_create__range=(today_min, today_max), author = auth)
            # if len(posts_for_today) >= 3:
            #     print('ПРЕВЫШЕН ЛИМИТ ПОСТИНГА')
            #     mail_managers(
            #         subject='Превышено количество постов',
            #         message='Ошибка на сайте',
            #     )
            # else:


                # user = self.request.user
                # pushUsers = []
                # for cat in post.categories.all():
                #     s = SubscriberCategory.objects.all().filter(category = cat).values('user')
                #     if len(s) > 0:
                #         for user in s:
                #             if user not in pushUsers:
                #                 pushUsers.append(user)
                                

                # for userForEmail in pushUsers:
                #     usr = User.objects.get(pk=userForEmail['user'])
                #     # получем наш html
                #     html_content = render_to_string( 
                #         'news/post_created_email.html',
                #         {
                #             'post': post,
                #             'userName':usr.username
                #         }
                #     )
                
                #     # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
                #     msg = EmailMultiAlternatives(
                #         subject=f'{post.author}',
                #         body=post.content, #  это то же, что и message
                #         from_email='ostapdev@epoha.ru',
                #         to=[usr.email], # это то же, что и recipients_list
                #     )
                #     msg.attach_alternative(html_content, "text/html") # добавляем html
                #     msg.send() # отсылаем
        return redirect('/')
        # return super().get(request, *args, **kwargs)

class PostDetailView(DetailView):
    template_name = 'app/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Response.objects.filter(
             post=self.get_object()).order_by('-date_create')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = ResponseForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Response(message=request.POST.get('message'),
                                  user=self.request.user,
                                  post=self.get_object(), 
                                  isAccepted = False)
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


# Create your views here.
class PostsList(ListView):
    model = Post
    template_name = 'app/feed.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10 # поставим постраничный вывод в один элемент
    # form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['time_now'] = datetime.utcnow()
        # context['value1'] = None
        # context['form'] = PostForm()
        return context
    
    # def post(self, request, *args, **kwargs):
    #     # self.object = self.get_object() # assign the object to the view
    #     # form = self.get_form()
        
    #     form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса
    #     if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
    #         form.save()
    #     return super().get(request, *args, **kwargs)


# Create your views here.
class Responses(ListView):
    model = Post
    template_name = 'app/responses.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    paginate_by = 10 # поставим постраничный вывод в один элемент
    # form_class = PostForm
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Post.objects.all().filter(user = self.request.user).order_by('-id')
        comments_connected = Response.objects.filter(post__user=self.request.user).order_by('-date_create')
        context['comments'] = comments_connected
        context['filter'] = PostFilter(self.request.GET, queryset=queryset) # вписываем наш фильтр в контекст
        # context['time_now'] = datetime.utcnow()
        context['myPosts'] = Post.objects.all().filter(user = self.request.user)
        # context['form'] = PostForm()
        return context
    
    # def post(self, request, *args, **kwargs):
        
    #     return '/responses'
    
def AcceptResponse(request, **kwargs):
    permission_required = ('app.change_response')
    id = kwargs.get('pk')
    comment = Response.objects.get(pk=id)
    comment.isAccepted = True
    comment.date_accepted = datetime.now()
    comment.save()
    return redirect('/responses')

def DeclineResponse(request, **kwargs):
    permission_required = ('app.change_response')
    id = kwargs.get('pk')
    comment = Response.objects.get(pk=id)
    comment.isAccepted = False
    comment.date_accepted = datetime.now()
    comment.save()
    return redirect('/responses')

def DeleteResponse(request, **kwargs):
    permission_required = ('app.delete_response')
    id = kwargs.get('pk')
    Response.objects.filter(pk=id).delete()
    return redirect('/responses')
    
