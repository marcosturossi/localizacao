from django.db import models
from django.urls import reverse

CATEGORIAS = (
    ('INT', 'Introdução'),
    ('LIN', 'Linguagens'),
    ('EXT', 'Extensão de Arquivos'),
)


class Version(models.Model):
    version = models.CharField(max_length=5)

    def __str__(self):
        return f'version: {self.version}'


class Documentation(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    category = models.CharField(max_length=3, choices=CATEGORIAS)
    resume = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('base:documentation', args=[self.slug])

    @property
    def get_category(self):
        for categoria in CATEGORIAS:
            if self.category in categoria:
                return categoria[1]

    def __str__(self):
        return self.title


class UpdateNotes(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return
