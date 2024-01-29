# <a style="text-decoration: none"><center>**API USERS**</center></a>
## <center>**API for Creation and Administration of Users**</center>

## <a style="text-decoration: none">Description :</a>
<p style="text-align: justify">API for the creation and administration of users, thus having four different levels of users where each has different permissions from the other. Being the zero level user a basic user and level 1 onwards are administrative profiles. </p>
<br>
<p>Summary of permissions by level:</p>
<ul>
    <li>0 - Level zero users sees your data, login, logout, create your own account, inactivate or delete your account and change your data.</li>
    <li>1 - Level one user does the same as level zero, but can see all users' data and change user zero's nv_user to level 1 and inactivate zero users.</li>
    <li>2 - Level two user can do the same as level one on a prorated basis and can delete or inactivate any level 1 and 0 user.</li>
    <li>3 - User level three is the master, he can do everything.</li>
</ul>
<br>
<p>To configure the database, if it is under development you can create a SQLite file, but if you want to use a database as PostgreSQL you must first create the database in your system, create the .env file and enter the information of connection through environmental variables as shown in project/settings.py</p>

## Installation

```bash
# Enter the environment in linux S.O
$ source venv/bin/activate
```
```bash
# Install all dependencies
$ pip install -r requirements.txt
```

```bash
# To configure the database
$ python manage.py makemigrations
$ python manage.py migrate 
```

## Running the app

```bash
# development
$ python manage.py runserver
```

## <a style="text-decoration: none">Model and endpoints :</a>

## CustomUser

## Fields:
```bash
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, unique=True, blank=True)
    picture = models.ImageField(upload_to='pictures/%Y/%m/%d', blank=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    nv_user = models.IntegerField(choices=NivelUsuario.choices, default=NivelUsuario.ZERO)
    is_logged_in = models.BooleanField(default=False)
    login_erro = models.IntegerField(choices=LoginError.choices, default=LoginError.ZERO)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    last_login_sistem = models.DateTimeField(blank=True, null=True)
```

### BaseUrl:
```bash
http://127.0.0.1:8000/api/users
```

## Endpoints:
- `{BaseUrl}/`: Used to register the user - method post.
- `{BaseUrl}/login/`: Login endpoint - method post.
- `{BaseUrl}/logout/`: Endpoint to log out - method post.
- `{BaseUrl}/<uuid:id>/`: Endpoint to retrieve data from a user - method get.
- `{BaseUrl}/`: Endpoint to collect data from all users - method get.
- `{BaseUrl}/<uuid:id>/`: Endpoint used to partial update a user's data - method patch.
- `{BaseUrl}/<uuid:id>/`:  Endpoint used to delete user from the database - method delete.
- `{BaseUrl}/rescue_password/before_login/`: Endpoint to send code to the email that will be necessary to authorize password rescue/change before logging in - method post.
- `{BaseUrl}/rescue_password/before_login/<email>`: Endpoint used to verify code sent by email - method patch.
- `{BaseUrl}/rescue_password/before_login/<email>/`: Endpoint used to change the user's password after checking the code sent by email - method delete.
- `{BaseUrl}/change_password/settings/`:  Endpoint to send code to the email that will be necessary to authorize password changes after login - method post.
- `{BaseUrl}/change_password/settings/<pk>`: Endpoint used to verify code sent by email, after login - method patch.
- `{BaseUrl}/change_password/settings/<pk>`: Endpoint used to change the user's password after checking the code sent by email, after login - method delete.

### Nota:
For the first five endpoints, no token is required

## Swagger

You can access the Swagger documentation at `http://127.0.0.1:8000/swagger/`.

## ReDoc

You can access the ReDoc documentation at `http://127.0.0.1:8000/redoc/`.

### Method: POST
### Endpoint
```bash
{BaseUrl}/
```

### Body  <span style="color: red">[required]</span>
```bash
{
    first_name: "john",
    last_name: "doe",
    email: "john.doe@gmail.com",
    phone: "+55 086 999999999",
    password: "S@bad0591",
}
```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 201
```
```bash
{
	user_id: {uuid4 id},
	register: "john.doe@gmail.com"
}
```

<p style="font-weight: 900"> Error </p>
<p> Situation in which you forgot to send fields that cannot be empty.</p>

```bash
Status code - 400
```

```bash
{
	first_name: [
		"This field is required."
	],
	last_name: [
		"This field is required."
	],
	password: [
		"This field is required."
	]
}
```

<p style="font-weight: 900"> Error </p>
<p> I try to use a unique value that is already being used by a user.</p>

```bash
Status code - 400
```

```bash
{
	email: [
		"custom user with this email already exists."
	],
}
```

### Method: POST
### Endpoint
```bash
{BaseUrl}/login/
```

### Body  <span style="color: red">[required]</span>
```bash
{
	email: "john.doe@gmail.com",
	password: "S@bad0591"
}
```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
	token: {
		access: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MTQ1OTk2LCJpYXQiOjE3MDQxNDIzOTYsImp0aSI6IjFiODIwYzk0ZjE5NTQyN2Y5OGRhODBjMzJhZDU0Zjg5IiwidXNlcl9pZCI6ImFjMjRhYzcyLTQzODItNGQyOS05YTVkLTczOWZjZjJkYzMyNCJ9.iGvyEOIaWMz_srrIrd9dK7lyeqihTmE86QxXYnjnfdQ",
		refresh: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNDIyODc5NiwiaWF0IjoxNzA0MTQyMzk2LCJqdGkiOiJlYTMyZmIyNjRlNmY0Y2VjYjAyNDgwODhlMDRjYTU5OCIsInVzZXJfaWQiOiJhYzI0YWM3Mi00MzgyLTRkMjktOWE1ZC03MzlmY2YyZGMzMjQifQ.sK_hfYcLq4vNAWsHAb8gBekxqhwTbE_gzBf4E3-Qpkw"
	},
	user: {
		id: "ac24ac72-4382-4d29-9a5d-739fcf2dc324",
		first_name: "john",
		last_name: "doe",
		email: "john.doe@gmail.com",
		phone: "+55 086 999999999",
		picture: null,
		login_erro: 0,
		is_logged_in: true,
		is_active: true
	}
}
```
<p style="font-weight: 900"> Errors </p>
<p> User tries to log in after having the wrong password 3 or more times</p>

```bash
Status code - 403
```
```bash
{
    error: Account blocked due to excessive login errors. Contact an administrator.',
}
```

<p> User gets the password wrong the third time</p>

```bash
Status code - 403
```
```bash
{
    error: Account blocked due to excessive login errors. Contact an administrator.',
}
```

<p> User is not active</p>

```bash
Status code - 403
```
```bash
{
    error: User is inactive.',
}
```

<p> User got the password wrong up to two times</p>


```bash
Status code - 400
```
```bash
{
    error: Incorrect password or email. Three login errors lead to account lockout.',
}
```

### Method: POST
### Endpoint
```bash
{BaseUrl}/rescue_password/before_login/
```

### Body
```bash

```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
 {
   message: 'Code sent successfully.'
}
```

<p style="font-weight: 900"> Error </p>
<p> Try to recover a user password with a non-existent email address at the bank</p>

```bash
Status code - 404
```
```bash
{
	"detail": "Not found."
}
```

### Method: PATCH
### Endpoint
```bash
{BaseUrl}/rescue_password/before_login/<email>
```

### Body  <span style="color: red">[required]</span>
```bash
{
	code: 957763
}
```
### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    message: 'Code verified successfully.'
}
```

<p style="font-weight: 900"> Error </p>
<p> Sending a code with an expired time</p>

```bash
Status code - 400
```
```bash
{
	detail: "The code has expired. Submit a new code."
}
```

<p> sending non-existent code</p>

```bash
Status code - 400
```
```bash
{
    detail: 'Not found',
}
```

### Method: DELETE
### Endpoint
```bash
{BaseUrl}/rescue_password/before_login/<email>
```

### Body  <span style="color: red">[required]</span>
```bash
{
	password: "S@bad0591"
}
```
### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
	message: "Change password"
}
```
<p style="font-weight: 900"> Error </p>
<p> If the email does not exist in the bank or does not have a code attached to it</p>

```bash
Status code - 404
```
```bash
{
    message: 'Not found',
}
```
<p> If the user code has not yet been verified</p>

```bash
Status code - 403
```
```bash
{
    error: 'No authorization for this procedure.',
}
```

### Method: POST
```bash
{BaseUrl}/change_password/settings/
```

### Bearer Token  <span style="color: red">[required]</span>

### Body
```bash

```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    message: 'Code sent successfully.'
}
```

### Method: PATCH
### Endpoint
```bash
{BaseUrl}/change_password/settings/<pk>
```
### Bearer Token  <span style="color: red">[required]</span>
### Body  <span style="color: red">[required]</span>
```bash
{
	code: 957763
}
```
### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    message: 'Code verified successfully.'
}
```

<p style="font-weight: 900"> Error </p>
<p> Sending a code with an expired time</p>

```bash
Status code - 400
```
```bash
{
	detail: "The code has expired. Submit a new code."
}
```

<p> sending non-existent code</p>

```bash
Status code - 400
```
```bash
{
    detail: 'Not found',
}
```

### Method DELETE
### Endpoint
```bash
{BaseUrl}/change_password/settings/<pk>
```
### Bearer Token  <span style="color: red">[required]</span>
### Body  <span style="color: red">[required]</span>
```bash
{
	password: "123456789"
}
```
### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
	message: "Change password"
}
```
<p style="font-weight: 900"> Error </p>
<p> User does not have a code attached</p>

```bash
Status code - 404
```
```bash
{
    message: 'Not found',
}
```
<p> If the user code has not yet been verified</p>

```bash
Status code - 403
```
```bash
{
    error: 'No authorization for this procedure.',
}
```

### Method: PATCH
### Endpoint
```bash
{BaseUrl}/logout/
```
### Bearer Token  <span style="color: red">[required]</span>
### Body
```bash

```
### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    user: "john.doe@gmail.com",
    message: 'logout'
}
```

<p style="font-weight: 900"> Error </p>
<p> Different user logout attempt</p>

```bash
Status code - 403
```
```bash
{
    message: 'No authorization for this procedure.',
}
```

<p> Non-existent user id</p>

```bash
Status code - 404
```
```bash
{
    message: 'Not found',
}
```

### Method: GET
### Endpoint
```bash
{BaseUrl}/<uuid:id>/
```

### Bearer Token  <span style="color: red">[required]</span>
### Body
```bash

```
### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
	user: {
		id: "ac24ac72-4382-4d29-9a5d-739fcf2dc324",
		first_name: "john",
		last_name: "doe",
		email: "john.doe@gmail.com",
		phone: "+55 086 999999999",
		picture: null,
		login_erro: 0,
		is_logged_in: true
        is_active: true
	}
}
```
<!-- <p style="font-weight: 900"> Error </p>
<p> Not Found</p>

```bash
{
    status code: 404,
    message: 'App not found',
}
```
<p> Internal server error</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
``` -->
### Method: GET
### Endpoint
```bash
{BaseUrl}/
```
### Bearer Token  <span style="color: red">[required]</span>
### Body
```bash

```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
	users: [
            {
                id: "ac24ac72-4382-4d29-9a5d-739fcf2dc324",
                first_name: "john",
                last_name: "doe",
                email: "john.doe@gmail.com",
                phone: "+55 086 999999999",
                picture: null,
                login_erro: 0,
                is_logged_in: true
            },
        ...
    ]
}
```

<!-- <p style="font-weight: 900"> Error </p>
<p> Situations where the body was not sent correctly.</p>

```bash
{
    status code: 400,
    message content: [ Description of unmet requirements],
    error - 'Bad request',
}
``` -->

### Method: PATCH
### Endpoint
```bash
{BaseUrl}/<uuid:id>/
```

### Bearer Token  <span style="color: red">[required]</span>
### Body  <span style="color: red">[required]</span>
```bash
{
    first_name: "john",
    last_name: "doe",
    email: "john.doe@gmail.com",
    phone: "+55 086 999999999",
},
```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
	user: {
		id: "ac24ac72-4382-4d29-9a5d-739fcf2dc324",
		first_name: "john",
		last_name: "doe",
		email: "john.doe@gmail.com",
		phone: "+55 086 999999999",
		picture: null,
		login_erro: 0,
		is_logged_in: true
        is_active: true
	}
}
```
<!-- <p style="font-weight: 900"> Error </p>
<p> Internal server error</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
``` -->

### Method DELETE
### Endpoint
```bash
{BaseUrl}/<uuid:id>/
```
### Bearer Token  <span style="color: red">[required]</span>
### Body
```bash

```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 204
```
```bash

```

<!-- <p style="font-weight: 900"> Error </p>
<p> Not Found</p>

```bash
{
    status code: 404,
    message: 'App not found',
}
```
<p> Internal server error</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
``` -->