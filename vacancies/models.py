from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS = [
        ('draft', 'Черновик'),
        ('open', 'Открыто'),
        ('closed', 'Закрыто')
    ]

    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

        # ordering = ["text", "slug]  # Сортировка, но не рекомендуют, потому что замедляет выполнение программы


    def __str__(self):
        return self.slug

