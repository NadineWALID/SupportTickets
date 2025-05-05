from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializer import RegisterSerializer,TicketSerializer
from .models import Ticket
from rest_framework import status, generics, permissions
from .permissions import IsStaffUser
import uuid
from django.db import connection
from django.db import transaction

# API to create a new user either Agent or Admin
# Premission to create new users is only granted to admins
# is_staff user in built in User Model in django to differentiate an Admin from an Agent

@api_view(['POST'])
@permission_classes([IsStaffUser])  
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to create a new Ticket 
# Premission to create new users is only granted to Admins
# Validations on input are done through serializer

@api_view(['POST'])
@permission_classes([IsStaffUser])  
def create_ticket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save()
        return Response({"message": "Ticket created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to view all tickets 
# Premission to create new users is only granted to Admins

@api_view(['GET'])
@permission_classes([IsStaffUser])
def view_ticket(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)

    ticket_data = serializer.data
    return Response({
        "tickets": ticket_data
    }, status=status.HTTP_200_OK)

# API to edit a ticket
# Premission to create new users is only granted to Admins
# Request input required is Ticket id

@api_view(['PUT'])
@permission_classes([IsStaffUser])
def update_ticket(request):
    ticketId = request.data.get("ticketId")
    if not ticketId:
        return Response({"error": "Ticket ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        ticket = Ticket.objects.get(pk=ticketId)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TicketSerializer(ticket, data=request.data, partial=True)  # partial=True for partial updates
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Ticket updated successfully.",
            "ticketId": ticket.id,
            "updatedData": serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to delete a ticket 
# Premission to create new users is only granted to Admins
# Request input required is Ticket id

@api_view(['DELETE'])
@permission_classes([IsStaffUser])
def delete_ticket(request):
    ticketId = request.data.get("ticketId")
    if not ticketId:
        return Response({"error": "Ticket ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        ticket = Ticket.objects.get(pk=ticketId)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    ticket.delete()
    return Response({
        "message": "Ticket deleted successfully."
    }, status=status.HTTP_200_OK)


# API get Agent's assigned tickets 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def view_my_assigned_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(assignedUser=user)  # Only tickets assigned to this user
    serializer = TicketSerializer(tickets, many=True)

    return Response({
        "user_id": user.id,
        "tickets": serializer.data
    }, status=status.HTTP_200_OK)

# API to fetch tickets and assign them to Agent
# It counts number of tickets assigned to Agent with status 'Assigned', 'Closed' tickets are ignored 
# Gets from DB ID list of tickets with null user, null ticketAgentUID and status "New"
# Updates rows obtained from previous step with user id, new status "Assigned" with unique id in ticketAgentUID

# Kindly note that to insure "Concurrency Handling" the plan was to update the required number of row with UID in column 'ticketAgentUID',
# Then fetch the rows with certain UID to assign to user, this is already implemented where I am currently working but it is not supported by SQLite since it doesn't support Limit
# Or use select_for_update(skip_locked=True) in case of posgresql

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def fetch_and_assign_tickets(request):
    user = request.user
    unique_claim_id = str(uuid.uuid4())


    assigned_count = Ticket.objects.filter(
        assignedUser=user,
        status='assigned'
    ).count()

    remaining_slots = 15 - assigned_count
    if remaining_slots <= 0:
        return Response({"message": "User already has 15 or more assigned tickets."}, status=200)
    
   

    ticket_ids = list(
        Ticket.objects.filter(
            assignedUser__isnull=True,
            status='new',
            ticketAgentUID__isnull=True
        ).order_by('id').values_list('id', flat=True)[:remaining_slots]
    )

    if not ticket_ids:
        return Response({"message": "No unassigned 'new' tickets available."}, status=200)


    id_list = ','.join(str(tid) for tid in ticket_ids)
    raw_update_query = f"""
        UPDATE api_ticket
        SET ticketAgentUID = %s,
            status = 'assigned',
            assignedUser_id = %s
        WHERE id IN ({id_list})
    """

    with connection.cursor() as cursor:
        cursor.execute(raw_update_query, [unique_claim_id, user.id])

    
    updated_tickets = Ticket.objects.filter(ticketAgentUID=unique_claim_id)
    serializer = TicketSerializer(updated_tickets, many=True)

    return Response({
        "message": f"{len(ticket_ids)} tickets assigned to user."
    }, status=200)


# API to set ticket status to "closed" 
# Request input required is Ticket id

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])  
def close_ticket(request):

    ticketId = request.data.get("ticketId")
    if not ticketId:
        return Response({"error": "Ticket ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        ticket = Ticket.objects.get(pk=ticketId)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    ticket.status = 'closed'
    ticket.save()

    return Response({"message": f"Ticket {ticket.ticketNumber} has been closed."}, status=status.HTTP_200_OK)

