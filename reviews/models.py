from django.db import models


class Review(models.Model):
    review = models.TextField()
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
