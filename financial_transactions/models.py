import datetime

from django.db import models


class Status(models.Model):
    """Статус транзакции."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return str(self.name)


class TransactionType(models.Model):
    """Тип транзакции."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    """Категория транзакции."""

    name = models.CharField(max_length=128, unique=True)
    transaction_types = models.ManyToManyField(
        'TransactionType',
    )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['name', 'transaction_type'],
    #             name="unique_category",
    #         ),
    #     ]

    def __str__(self):
        return str(self.name)


class Subcategory(models.Model):
    """Подкатегория транзакции."""

    name = models.CharField(max_length=128)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name="unique_subcategory",
            ),
        ]

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    """Финансовая транзакция."""

    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        help_text="Комментарий к записи",
        blank=True,
    )
    amount = models.PositiveIntegerField(
        help_text="Количество средств в рублях.",
    )
    created_at = models.DateField(default=datetime.date.today)

    transaction_type = models.ForeignKey(
        'TransactionType',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        on_delete=models.CASCADE,
    )
