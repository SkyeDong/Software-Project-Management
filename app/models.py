
# 一个数据库对应一个模型
from django.db import models
'''
# 模型对应一张表songs
class songs(models.Model):
    songs_id = models.IntegerField()  # 字段
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    songUrl = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=300)
'''