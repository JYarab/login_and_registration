from django.db import models
from django.db.models.fields import DateTimeField
from datetime import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        users = User.objects.all()
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 charaters'        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 charaters'        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invaild email address'
        else:
            for user in users:
                if postData['email'] == user.email:
                    errors['email'] = 'Email already in use'
        if len(postData['birth_date']) == 0:
            errors['birth_date'] = 'Must enter birth date'
        else:
            age = datetime.now() - datetime.strptime(postData['birth_date'], '%Y-%m-%d')
            if (age.days / 365.2425) < 13: 
                errors['date'] = 'Must be at least 13 years old to register'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 charaters'
        else:
            if postData['password'] != postData['conf_pass']:
                errors['password'] = "Passwords do not match"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField()
    password = models.CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = UserManager()


