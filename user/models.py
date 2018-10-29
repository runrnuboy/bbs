from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('S', '保密'),
    )

    nickname = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    sex = models.CharField(max_length=8, choices=SEX)
    age = models.IntegerField()

    def to_dict(self):
        return {
            'nickname': self.nickname,
            'icon': self.icon.url,
            'sex': self.sex,
            'age': self.age,
        }
