# SupportTickets

# Notes
Kindly note that JWT authentication is used to authenticate users, and access token must be used in header to access any of the APIs.
The postman collection contains an API to get a token, when starting the application, a superadmin can be created manually, then the postman collection contains the token API to obtain token.
Using this token other users[Admin/Agent] can be created using create user API using created superadmin, or any Admin created after that
Built in User model is used for created users, where is_staff = True[for Admins]/False[For Agents]

# Contains:
# API 1: To create user

 API to create a new user either Agent or Admin
 Premission to create new users is only granted to admins
 is_staff user in built in User Model in django to differentiate an Admin from an Agent

# API 2: To create ticket

 API to create a new Ticket 
 Premission to create new tickets is only granted to Admins
 Validations on input are done through serializer

# API 3: View all tickets
Kindly note that get tickets APIs are crucial in the implementation to be used by frontend, to fetch ticket id be able to edit tickets 
 API to view all tickets 
 Premission to view all tickets is only granted to Admins

# API 4: Edit Ticket

 API to edit a ticket
 Premission  is only granteded to Admins
 Request input required is Ticket id

# API 5: Delete Ticket

 API to delete a ticket 
 Premission is only granted to Admins
 Request input required is Ticket id

# API 6: 
 API get Agent's assigned tickets

# API 7: Fetch unassigned Tickets

 API to fetch tickets and assign them to Agent
 It counts number of tickets assigned to Agent with status 'Assigned', 'Closed' tickets are ignored 
 Gets from DB ID list of tickets with null user, null ticketAgentUID and status "New"
 Updates rows obtained from previous step with user id, new status "Assigned" with unique id in ticketAgentUID

 Kindly note that to insure "Concurrency Handling" the plan was to update the required number of row with UID in column 'ticketAgentUID',
 Then fetch the rows with certain UID to assign to user, this is already implemented where I am currently working but it is not supported by SQLite since it doesn't support Limit
 Or use select_for_update(skip_locked=True) in case of posgresql


# API 8: 

 API to set ticket status to "closed" 
 Request input required is Ticket id



