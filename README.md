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
$ source venv/bin/
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
id = models.UUIDField(primary_key=True, default=uuid4)
first_name = models.CharField(max_length=50)
last_name = models.CharField(max_length=50)
email = models.EmailField(max_length=50, unique=True)
phone = models.CharField(max_length=20, unique=True)
picture = models.ImageField()
password = models.CharField(max_length=100)
is_active = models.BooleanField(default=True)
nv_user = models.IntegerField(default=NivelUsuario.ZERO)
is_logged_in = models.BooleanField(default=False)
login_erro = models.IntegerField(default=LoginError.ZERO)
created_at = models.DateTimeField(auto_now_add=True)
update_at = models.DateTimeField(auto_now=True)
last_login_sistem = models.DateTimeField(null=True)
```

### BaseUrl:
```bash
http://127.0.0.1:8000/api/users/
```

### Method: POST
### Endpoint
```bash
register/
```

### Body  <span style="color: red">[required]</span>
```bash
Schema
```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 201
```
```bash
{
    data: { Data saved },
    message: 'App settings created'
}
```

<p style="font-weight: 900"> Error </p>
<p> Situations where the body was not sent correctly.</p>

```bash
{
    status code: 400,
    message content: [ Description of unmet requirements],
    error - 'Bad request',
}
```



### Method: POST
### Endpoint
```bash
login/
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
    data: [
      {
        appId: string,
        paymentOptions: [string],
        shippingOptions: [string],
        currency: string,
        taxRate: number,
        invoiceIntegration: {
          enabled: boolean,
          provider: string,
          apiKey: string,
        },
        deliveryIntegration: {
          enabled: boolean,
          provider: string,
          apiKey: string,
        }
      },...
    ]
}
```
<p style="font-weight: 900"> Error </p>
<p> Erro interno do servidor</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
```
### Method: POST
### Endpoint
```bash
/send_code/<str:email>/
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
    data: {
      appId: string,
      paymentOptions: [string],
      shippingOptions: [string],
      currency: string,
      taxRate: number,
      invoiceIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      },
      deliveryIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      }
    }
}
```

<p style="font-weight: 900"> Error </p>
<p> Not Found</p>

```bash
{
    status code: 404,
    message: 'App settings not found',
}
```
<p> Erro interno do servidor</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
```

### Method: PATCH
### Endpoint
```bash
verify_code/
```

### Body
```bash
{
      appId: string,
      paymentOptions: [string],
      shippingOptions: [string],
      currency: string,
      taxRate: number,
      invoiceIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      },
      deliveryIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      }
    }
```
<p>Obs: All fields are optional.</p>

<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    data: {
      appId: string,
      paymentOptions: [string],
      shippingOptions: [string],
      currency: string,
      taxRate: number,
      invoiceIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      },
      deliveryIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      }
    }, 
    message: 'App settings updated'
}
```

<p style="font-weight: 900"> Error </p>
<p> Bad Request</p>

```bash
{
    status code: 400,
    message: 'Bad Request.',
}
```

<p> Not Found</p>

```bash
{
    status code: 404,
    message: 'App settings not found',
}
```

<p> Erro interno do servidor</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
```

### Method: PATCH
### Endpoint
```bash
/change_password/<str:email>/
```

### Body
```bash

```
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    data: {
      appId: string,
      paymentOptions: [string],
      shippingOptions: [string],
      currency: string,
      taxRate: number,
      invoiceIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      },
      deliveryIntegration: {
        enabled: boolean,
        provider: string,
        apiKey: string,
      }
    }, 
    message: 'App settings deleted'
}
```
<p style="font-weight: 900"> Error </p>
<p> Not Found</p>

```bash
{
    status code: 404,
    message: 'App settings not found',
}
```
<p> Erro interno do servidor</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
```
### Method: POST
```bash
settings/send_code/
```

### Body  <span style="color: red">[required]</span>
```bash
Schema
```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 201
```
```bash
{
    data: { Data saved },
    message: 'App settings registered'
}
```

<p style="font-weight: 900"> Error </p>
<p> Situations where the body was not sent correctly.</p>

```bash
{
    status code: 400,
    message content: [ Description of unmet requirements ],
    error - 'Bad request',
}
```
### Method: PATCH
### Endpoint
```bash
settings/verify_code/
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
    data: [
      {
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
      },...
    ]
}
```
<p style="font-weight: 900"> Error </p>
<p> Internal server error</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
```

### Method PATCH
### Endpoint
```bash
/settings/change_password/
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
    data: {
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
      }
}
```

<p style="font-weight: 900"> Error </p>
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
```

### Method: PATCH
### Endpoint
```bash
logout/<uuid:id>/
```

### Body
```bash
{
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
}
```
<p>Obs: All fields are optional.</p>

<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    data: {
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
      }, 
    message: 'App settings updated'
}
```

<p style="font-weight: 900"> Error </p>
<p> Bad Request</p>

```bash
{
    status code: 400,
    message: 'Bad Request.',
}
```

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
```

### Method: GET
### Endpoint
```bash
<uuid:id>/
```

### Body
```bash

```
<p style="font-weight: 900"> Success </p>

```bash
Status code - 200
```
```bash
{
    data: {
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
      }, 
    message: 'App settings deleted'
}
```
<p style="font-weight: 900"> Error </p>
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
```
### Method: GET
### Endpoint
```bash
list/
```

### Body  <span style="color: red">[required]</span>
```bash
Schema
```

### Responses
<p style="font-weight: 900"> Success </p>

```bash
Status code - 201
```
```bash
{
    data: { Data saved },
    message: 'Financial transactions registered'
}
```

<p style="font-weight: 900"> Error </p>
<p> Situations where the body was not sent correctly.</p>

```bash
{
    status code: 400,
    message content: [ Description of unmet requirements],
    error - 'Bad request',
}
```

### Method: PATCH
### Endpoint
```bash
update_user/<uuid:id>/
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
    data: [
      {
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
      },...
    ]
}
```
<p style="font-weight: 900"> Error </p>
<p> Internal server error</p>

```bash
{
    status code: 500,
    error: 'Internal server error.',
}
```

### Method DELETE
### Endpoint
```bash
/delete_user/<uuid:id>/
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
    data: {
        appId: string,
        name: string,
        description: string,
        apiKey: string,
        secretKey: string,
        stripeApiKey: string,
        stripeSecretKey: string,
        callbackUrl: string,
        jwtKay: string,
        outherSettings: string,
      }
}
```

<p style="font-weight: 900"> Error </p>
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
```