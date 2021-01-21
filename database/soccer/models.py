import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class TBLUser(AbstractUser):

    class Meta:
        db_table = 'tbl_user'


class TBLToken(models.Model):
    token = models.TextField()
    user_id = models.IntegerField()
    created_time = models.DateTimeField()

    class Meta:
        db_table = 'tbl_token'

    def save(self, *args, **kwargs):
        self.created_time = datetime.datetime.now(datetime.timezone.utc)
        super().save(*args, **kwargs)


class TBLMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    age = models.IntegerField()
    type = models.IntegerField(choices=[
        (0, 'Goal Keepers'),
        (1, 'Defender'),
        (2, 'Midfielder'),
        (3, 'Attacker'),
    ])
    value = models.FloatField(default=1000000)
    team_id = models.IntegerField()

    class Meta:
        db_table = 'tbl_member'


class TBLTeam(models.Model):
    owner = models.ForeignKey(TBLUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    extra_value = models.FloatField(default=5000000)
    members = models.ManyToManyField(TBLMember, default=None, null=None)

    class Meta:
        db_table = 'tbl_team'


class TBLMarket(models.Model):
    member = models.ForeignKey(TBLMember, on_delete=models.CASCADE)
    price = models.FloatField()

    class Meta:
        db_table = 'tbl_market'


