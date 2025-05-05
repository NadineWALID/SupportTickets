from django.urls import path
from .views import register_user,create_ticket,view_ticket, update_ticket, delete_ticket,view_my_assigned_tickets,fetch_and_assign_tickets,close_ticket
urlpatterns = [
    path('createUser/', register_user, name='createUser'),
    path('createTicket/', create_ticket, name='createTicket'),
    path('viewTickets/', view_ticket, name='viewTickets'),
    path('updateTicket/', update_ticket, name='updateTicket'),
    path('deleteTicket/', delete_ticket, name='deleteTicket'),
    path('viewMyAssignedTickets/', view_my_assigned_tickets, name='viewMyAssignedTickets'),
    path('fetchAndAssignTickets/', fetch_and_assign_tickets, name='fetchAndAssignTickets'),
    path('closeTicket/', close_ticket, name='closeTicket'),
]