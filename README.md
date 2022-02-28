### Objective

Your assignment is to build an internal API for a fake financial institution using Python and any framework.

### Brief

While modern banks have evolved to serve a plethora of functions, at their core, banks must
 provide certain basic features. Today, your task is to build the basic HTTP API for one of those banks!
 Imagine you are designing a backend API for bank employees. It could ultimately be consumed by multiple
 frontends (web, iOS, Android etc).

### Tasks

- Implement assignment using:
  - Language: **Python**
  - Framework: **any framework**
- There should be API routes that allow them to:
  - Create a new bank account for a customer, with an initial deposit amount. A
    single customer may have multiple bank accounts.
  - Transfer amounts between any two accounts, including those owned by
    different customers.
  - Retrieve balances for a given account.
  - Retrieve transfer history for a given account.
- Write tests for your business logic

Feel free to pre-populate your customers with the following:

```json
[
  {
    "id": 1,
    "name": "Arisha Barron"
  },
  {
    "id": 2,
    "name": "Branden Gibson"
  },
  {
    "id": 3,
    "name": "Rhonda Church"
  },
  {
    "id": 4,
    "name": "Georgina Hazel"
  }
]
```

You are expected to design any other required models and routes for your API.

### Evaluation Criteria

- **Python** best practices
- Completeness: did you complete the features?
- Correctness: does the functionality act in sensible, thought-out ways?
- Maintainability: is it written in a clean, maintainable way?
- Testing: is the system adequately tested?
- Documentation: is the API well-documented?

### CodeSubmit

Please organize, design, test and document your code as if it were going into production 
- then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The SaltPay Team

#### Deployment
Install Mysql(windows env)- Assumption already have python 3 plus already installed
1. open the project root

	pipenv install	djano,
	pipenv install	djangorestframework,
	pipenv install	mysqlclient,
	pipenv install	djoser,
	pipenv install	djangorestframework_simplejwt,
	# Testing tools
	pipenv install --dev pytest
	pipenv install --pytest-django 
> pipenv install
> 

2. Db configuration project_root>settings.py 
   search DATABASES make the required changes depending on your local db configuration
3. On project root directory open cmd and run> python manage.py makemigrations
4. On project root directory open cmd and run> python manage.py migrate
5. > python manage.py createsuperuser - optional
  - create a user with password to access the admin portal
  - this is where you will also interact with the api
6. Run the app on local  (app route directory)>python manage.py runserver

### AUTHENTICATION


1. /auth/users/   	  - Create user
2. /auth/jwt/	  	  - Get JWT Token
3. /auth/jwt/refresh  - Use it to access a new token, when it expires(set to expire after one day)
4. /auth/users/me/    - Authenticated user details

# Use
To access the banking api (below end points) you need to be authenticated
#Testing Tools
1.Chrome browser install modheader Plugin->chrome plugin to modify headers - add jwt token
2. Use postman and set authorization to JWT Token

Authenticate
JWT access_token

### Banking End Points

# Start by  creating Transaction types. Atlest these 3 (REQUIRED!!!)(DEPOSIT, WITHDRAWL, TRANSFER)

# TransactionTypes
1. /api/transactiontypes   - show all transaction types i.e deposit, withdrawl, transfer 

2. /api/transactiontypes/	-  POST create transactiontype - unique - Upper case conversion before saving
	# create transaction type
	{
	"name":"Transfer"
	}

3. /api/transactiontypes/id	   - show details

# Customers

4. /api/customers	     - all customers

5. /api/customers/id	 - customer detalis

6. /api/customers/    	 - POST create a customer

7. /api/customers/id/	 - PUT update customer details
## Example
	# customers/create
		{
			"name": "Elson Musk",
			"dob": "1980-01-31",
			"location": "USA - Hawthorne, California ",
			"occupation": "CEO SpaceX"
		}
	# customers/{id}/update
	{
		"name": "Elson Musk",
		"dob": "1980-01-31",
		"location": "USA - Hawthorne, California , Austin Texas",
		"occupation": "CEO SpaceX, Tesla"
	}

8. /api/customer/id/accounts - get customer accounts
 
# Accounts NB: for simplicity the id is used as account number
9.  /api/accounts 	  - all accounts

10. /api/accounts/ 	  - POST create customer account - Note: initial_deposit(balance) SHOULD BE GREATOR OR EQUAL TO 500.00 DEFAULT CONFIG

	# create account sample
	{
		"name": "Test test2 account",
		"balance": 400,
		"customer_id": 1
	}

11.  /api/accounts/id   - show account details plus balance

# Transactions

12.  /api/accounts/id/history	 - all the transactions

13.  /api/transfer	 			 - POST transfer transactions - Note: amount SHOULD BE GREATOR OR EQUAL TO 500.00 DEFAULT CONFIG
								 -  Also minimum balance per account is configure to always be 500.00
								 - To Transfer the account need a minimum of 1000.00
		# transfer amount sample
		{
		  "from_account":2,
		   "destination_account":5,
		   "amount":500.00
		  
		}
# Unit Test( not 100 % coverage but have covered most import parts, no unit test for user-operations)
go to the root of the project and type >pytest





