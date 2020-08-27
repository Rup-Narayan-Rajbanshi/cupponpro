from django.db import models

class NewsArticle(models.Model):
    news_partner = models.CharField(max_length=50)
    url = models.TextField()
    headline = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news_article'

    def __str__(self):
        return self.headline
