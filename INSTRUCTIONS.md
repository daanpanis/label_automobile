Installation
----
Most of the instructions will be the same as in the README.md

#### Setup python environment
```shell script
# Change directory into your newly created project.
cd label_automobile

# Create a Python virtual environment.
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Upgrade packaging tools.
pip install --upgrade pip setuptools

# Install the project in editable mode with its testing requirements.
pip install -e ".[testing]"
```

#### Setup database
```shell script
# Change your settings
development.ini -> Database settings and possibly application port

# Or alternatively start up a docker PostgreSQL docker container:
docker-compose up -d

# Configure the database.
init_mob_db development.ini

# Add test data to the database
mock_mob_db development.ini
```

#### Start server
```shell script
pserve development.ini
```
<br>

Authentication
----
I implemented a very basic authentication system which uses the `Authorization` header to pass send specify the user id of the current request. This is obviously very insecure since no login is required and you only need to know someone's user id in order to send requests on their account.
<br>
<br>
Make sure that the `Authorization` is always set to an existing user id or you will receive a `404 Unauthorized` response for certain requests. 
I would recommend setting the value to `cece8926-2856-485e-8095-7c7a63f7997f` since that is the default user that will be added when running the `init_mob_db development.ini` command

<br>

Requests
----
####`GET /products`
Lists all products in the database.
<br>
<br>
####`GET /products/{id}`
Gets details of a product by the product id

- `id:` UUID of the product  
<br>
####`GET /cart`
Lists all products currently in the user's cart **(Requires authentication)**
<br>
<br>
####`[POST,PUT] /cart/{id}`
Adds a product to your shopping cart, or increases the amount of the product currently in your cart by 1. **(Requires authentication)**

- `id:` UUID of the product
<br>
####`DELETE /cart/{id}`
Decreases the amount of a specific product in your shopping cart by 1. **(Requires authentication)**

- `id:` UUID of the product

<br>

####`DELETE /cart/{id}/all`
Removes the entire product from your shopping cart, even if amount is higher than 1. **(Requires authentication)**
- `id:` UUID of the product

<br>

####`GET /orders`
Gets all the orders for the current user **(Requires authentication)**
<br>
<br>
####`GET /orders/{id}`
Gets the details of an order by the order id **(Requires authentication)**

- `id:` UUID of the order

<br>

####`[POST,PUT] /orders`
Orders all the current contents of your shopping cart. **(Requires authentication)**

**Request body:**
```json
{
  "address": "<address>",
  "houseNumber": "<house number>",
  "postalCode": "<postal code>",
  "deliveryDate": "date formatted as: <year>-<month>-<day>"
}
```