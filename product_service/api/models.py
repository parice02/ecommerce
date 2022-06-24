from django.db import models

# Create your models here.


class Product(models.Model):
    """ """

    designation = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    price = models.FloatField("Prix (en Franc CFA)")
    stock = models.FloatField("Stock")

    def __str__(self) -> str:
        return self.designation

    class Meta:
        ordering = ["id"]


class History(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    make_at = models.DateTimeField(auto_now_add=True)
    transaction = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.product.designation

    class Meta:
        ordering = ["id"]
