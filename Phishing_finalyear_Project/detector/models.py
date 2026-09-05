from django.db import models


class PredictionHistory(models.Model):
    url = models.URLField(max_length=2000)
    result = models.CharField(max_length=20)
    confidence = models.FloatField()
    model = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.url[:50]} - {self.result}"
