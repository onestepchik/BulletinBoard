from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Response, Post, User

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст

 

@receiver(post_save, sender=Post)
def notify_all_new_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Новое объявление {instance.title}!'
        usr = instance.user
        # получем наш html
        html_content = render_to_string( 'app/post_created_email.html',
            {
                'post': instance,
                'userName':usr.username
            }
        )
                
        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        email_list = list(User.objects.values_list("email", flat=True))

        msg = EmailMultiAlternatives(
            subject=subject,
            body=instance.content, #  это то же, что и message
            from_email='ostapdev@epoha.ru',
            to=email_list, # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send() # отсылаем
    

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Response)
def notify_post_author_new_response(sender, instance, created, **kwargs):
    if created:
        subject = f'У вас новый отклик по объявлению {instance.post.title}'
        usr = instance.post.user
        # получем наш html
        html_content = render_to_string( 'app/response_created_email.html',
            {
                'post': instance.post,
                'response': instance,
                'userName':usr.username
            }
        )
                
        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=subject,
            body=instance.message, #  это то же, что и message
            from_email='ostapdev@epoha.ru',
            to=[usr.email], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send() # отсылаем
    else:
        if instance.isAccepted:
            
            subject = f'Автор принял Ваш отклик! Объявление {instance.post.title}'
            usr = instance.user
            # получем наш html
            html_content = render_to_string( 'app/response_accepted_email.html',
                {
                    'post': instance.post,
                    'response': instance,
                    'userName':usr.username
                }
            )
                
            # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
            msg = EmailMultiAlternatives(
                subject=subject,
                body=instance.message, #  это то же, что и message
                from_email='ostapdev@epoha.ru',
                to=[usr.email], # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html") # добавляем html
            msg.send() # отсылаем
        else:
            subject = f'Автор отклонил Ваш отклик! Объявление {instance.post.title}'
            usr = instance.user
            # получем наш html
            html_content = render_to_string( 'app/response_declined_email.html',
                {
                    'post': instance.post,
                    'response': instance,
                    'userName':usr.username
                }
            )
                
            # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
            msg = EmailMultiAlternatives(
                subject=subject,
                body=instance.message, #  это то же, что и message
                from_email='ostapdev@epoha.ru',
                to=[usr.email], # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html") # добавляем html
            msg.send() # отсылаем
        
