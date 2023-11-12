from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
from django import forms
 
# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {'title':['icontains'], 
                  'content':['icontains'], 
                  'date_create': ['gt'] ,
                  'category': ['exact']
                  } # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        # widgets = {
        #     "title": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Напишите комментарий к посту"}
        #     ),
        #     "content": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Напишите комментарий к посту"}
        #     ),
        #     "date_create": forms.Select(
        #         attrs={
        #             "class": "form-control",
        #         }
        #     ),
        #     "category": forms.Select(
        #         attrs={
        #             "class": "form-control",
        #         }
        #     ),
        # }