from django.db import models

from django.contrib.auth.models import User

class Author(models.Model):
    rating = models.IntegerField(default = 0)
    #рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #cвязь «один к одному» с встроенной моделью пользователей User;


    def update_rating(self):
        post_rating = 0
        postObj = Post.objects.filter(author = self.id).values("rating")
        for obj_in_dict in postObj:
            post_rating += int(obj_in_dict.get("rating"))
        post_rating = post_rating * 3
        
        auth_com = 0
        auth_comObj = Comment.objects.filter(user = self.user).values("rating")
        for obj_in_dict in auth_comObj:
            auth_com += int(obj_in_dict.get("rating")) #комментарии от автора
    
        post_com = 0
        #post_comObj = Post.objects.filter(author = self).Comment.objects.all().values("rating")
        postAuth = Post.objects.filter(author = self.id)
        for post_i in postAuth:

            post_comObj = Comment.objects.filter(post = post_i.id ).values("rating")
            for obj_in_dict in post_comObj:
                post_com =+ int(obj_in_dict.get("rating")) #комментарии автору

        self.rating = post_rating +  auth_com + post_com
        self.save()
        return self.rating

    #Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный 
# в аргумент этого метода.
#Он состоит из следующего:
#суммарный рейтинг каждой статьи автора умножается на 3;
#суммарный рейтинг всех комментариев автора;
#суммарный рейтинг всех комментариев к статьям автора.


class Category(models.Model):
    category_name = models.CharField(max_length = 100,unique = True)
    #Категории новостей/статей — темы, которые они отражают 
    # (спорт, политика, образование и т. д.). 
    # Имеет единственное поле: название категории. 
    # Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).

class Post(models.Model):
    article = 'AR'
    news = 'NE'
    TYPE_OF_CONTENT = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    title = models.CharField(max_length=100) #заголовок статьи/новости;
    text = models.TextField() #текст статьи/новости;
    type_of_content = models.CharField(max_length=2, choices=TYPE_OF_CONTENT, default=news) #поле с выбором — «статья» или «новость»;
    rating = models.IntegerField(default = 0) #рейтинг статьи/новости.
    datetime = models.DateTimeField(auto_now_add=True) #автоматически добавляемая дата и время создания;

    category = models.ManyToManyField(Category, through="PostCategory")
    #связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    #связь «один ко многим» с моделью Author;

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating
    
    def preview(self):
        return self.text[0:123] + '...'
    
    def __str__(self):
        return f'{self.title} {self.author}\n{self.text}'
    

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #связь «один ко многим» с моделью Category.

class Comment(models.Model):
    rating = models.IntegerField(default = 0) #рейтинг комментария.
    com_text = models.TextField() #текст комментария;
    datetime = models.DateTimeField(auto_now_add=True) #дата и время создания комментария;

    user = models.ForeignKey(User, on_delete=models.CASCADE) #связь «один ко многим» со встроенной моделью User 
    #(комментарии может оставить любой пользователь, необязательно автор);
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #связь «один ко многим» с моделью Post;

    def like(self):
        self.rating += 1
        self.save()
        return self.rating
    
    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

#Методы like() и dislike() в моделях Comment и Post, которые увеличивают/уменьшают рейтинг на единицу.
# #Метод preview() модели Post, который возвращает начало статьи (предварительный просмотр) длиной 124 
# символа и добавляет многоточие в конце.
#Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный 
# в аргумент этого метода.
#Он состоит из следующего:
#суммарный рейтинг каждой статьи автора умножается на 3;
#суммарный рейтинг всех комментариев автора;
#суммарный рейтинг всех комментариев к статьям автора.
