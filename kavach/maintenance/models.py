from django.db import models

# Create your models here.

class Complaint(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
