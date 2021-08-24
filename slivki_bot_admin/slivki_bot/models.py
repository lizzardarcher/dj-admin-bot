from django.db import models


class Employee(models.Model):
    eid = models.CharField(max_length=20)
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    econtact = models.CharField(max_length=15)

    class Meta:
        db_table = "employee"


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "users"


class Messages(models.Model):
    msg_id = models.IntegerField(primary_key=True, )
    user_name = models.CharField(max_length=100)
    msg_text = models.TextField(max_length=4000)
    photo_1 = models.CharField(max_length=1000)
    photo_2 = models.CharField(max_length=1000)
    photo_3 = models.CharField(max_length=1000)
    payment = models.IntegerField()
    exp_date = models.CharField(max_length=100)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.CharField(max_length=4000, default='комментарий')

    class Meta:
        db_table = "messages"
