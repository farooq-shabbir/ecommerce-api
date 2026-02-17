from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id}"
