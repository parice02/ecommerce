from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PAYMENT_EXPECTED = "PAYMENT_EXPECTED", _("Paiement attendu")
        PAID = "PAID", _("Payé")
        READY = "READY", _("Prêt")
        TAKEN = "TAKEN", _("Pris")

    status = models.CharField(
        choices=PaymentStatus.choices,
        max_length=20,
        default=PaymentStatus.PAYMENT_EXPECTED,
    )
    ordered_date = models.DateTimeField(auto_now_add=True)
    product = models.IntegerField()
    quantity = models.IntegerField()
    client = models.IntegerField()

    def __str__(self) -> str:
        return str(self.product) + "-" + str(self.quantity) + "-" + str(self.client)
