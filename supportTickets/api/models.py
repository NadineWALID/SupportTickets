from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class Ticket(models.Model):
    ticketNumber = models.CharField(max_length=100, default='')
    ticketDescription = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('closed', 'Closed')
    ], default='new')
    assignedUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    additionDate = models.DateTimeField(auto_now_add=True)
    ticketAgentUID = models.UUIDField(null=True, blank=True, unique=False)

    def __str__(self): # function for when printing a ticket
        return self.ticketNumber
    

