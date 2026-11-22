from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.core.validators import RegexValidator


class DailyNote(models.Model):

    id = models.BigAutoField(primary_key=True)

    note_date = models.DateField(
        db_index=True
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    note_text = models.TextField()

    color = models.CharField(
        max_length=7,
        default="#e53935",
        validators=[
            RegexValidator(
                regex=r'^#[0-9A-Fa-f]{6}$',
                message="Enter a valid HEX color."
            )
        ]
    )

    is_pinned = models.BooleanField(
        default=False
    )

    is_archived = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "daily_notes"

        ordering = ["-note_date", "-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["note_date", "color"],
                name="unique_note_color_per_date"
            )
        ]

    def __str__(self):
        return f"{self.note_date} - {self.title or self.note_text[:40]}"

