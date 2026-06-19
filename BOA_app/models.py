from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=CloudinaryField('images/profile_pic/', blank=True, null=True )
    national_id=CloudinaryField('images/profile_id/', blank=True, null=True )
    first_name=models.CharField(max_length=50, blank=True, null=True)
    last_name=models.CharField(max_length=50, blank=True, null=True)
    dob= models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    country=models.CharField(max_length=100, blank=True, null=True)
    income_source=models.CharField(max_length=100, blank=True, null=True)
    phone=models.CharField(max_length=100, blank=True, null=True)
    job_title=models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False, null=True)
    def __str__(self):
         return f'{self.user.username} Profile created at {self.created_at}'

class Emmergency_Fund_Account(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     account_type = models.CharField(max_length=100, blank=True, null=True)
     created_at = models.DateField(auto_now_add=True, null=True, blank=True)
     balance = models.CharField(max_length=100, null=True, blank=True)
     status = models.BooleanField(default=False, null=True)
     def __str__(self):
          return f'{self.user.username} Emmergency account details created at {self.created_at}'
     
class Ticket(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     type = models.CharField(max_length=100, null=True, blank=True)
     message = models.CharField(max_length=500, null=True, blank=True)
     created_at= models.DateField(auto_now_add=True, null=True, blank=True)
     viewed = models.BooleanField(default=False, null=True)
     def __str__(self):
          return f'{self.type} Ticket created by {self.user.username} on {self.created_at}'
     
class Ticket_Response(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
     response = models.CharField(max_length=500, null=True, blank=True)
     created_at = models.DateField(auto_now_add=True, null=True, blank=True)
     viewed = models.BooleanField(default=False, null=True)
     def __str__(self):
          return f'Ticket response to {self.ticket.type} ticket'
     
     