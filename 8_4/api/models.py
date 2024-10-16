from django.db import models
from django.db.models import CASCADE
from django.utils.text import slugify


def uniq_slug(class_, instance, value, *args, **kwargs):
    if not instance.slug:
        original_slug = slugify(value)
        slug = original_slug
        counter = 1

        while class_.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        instance.slug = slug


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name
    full_name.short_description = "Ism va familiya"

    def __str__(self):
        return self.full_name()

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def save(self, *args, **kwargs):
        uniq_slug(Category, self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Food(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu/', null=True, blank=True)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        uniq_slug(Food, self, self.title)
        super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            return self.image.url
        return 'media/default.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Taom'
        verbose_name_plural = "Taomlar"


class Order(models.Model):
    STATUS_CHOICES = (
        ('wait', "Kutilmoqda"),
        ('cancel', "Bekor qilindi"),
        ('prepared', "Tayyor"),
        ('submit', "Topshirildi")
    )
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    items = models.ManyToManyField(Food)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wait')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.full_name() + ' ' + self.date.strftime('%m %d, %Y - %H:%M:%S')

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
