from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from .managers import ProductsManager
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here
class Products(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['name','price'])
        ]


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail',args=[self.slug])
    
    def delete(self,using=None,keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=['is_deleted', 'deleted_at'])

    seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name='product')
    name = models.CharField(max_length=100,db_index=True)
    price = models.FloatField(db_index=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True,blank=True)
    stock = models.IntegerField()
    active = models.BooleanField(default=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)

    objects = ProductsManager()
    all_objects = models.Manager()

    def save(self,*args, **kwargs):
        if not self.slug:
            #self.slug = slugify(self.name)
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Products.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter+=1
            self.slug = slug
        super().save(*args, **kwargs)
