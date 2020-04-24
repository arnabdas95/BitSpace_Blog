from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=500)
    pro_pic = models.ImageField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
     return f'{self.user.username} profile'
    def save(self):
        super().save()
        img = Image.open(self.pro_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.pro_pic.path)


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    details = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    '''
        def save(self,*args,**kwargs):
        self.details_html=misaka.html(self.details)
        super().save(*args,**kwargs)
        '''


    class Meta:
       ordering = ['-publish_date']





