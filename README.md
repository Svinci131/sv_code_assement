# Challenge:

Write an REST based API using API Gateway which takes name, email, password in JSON format from HTTP POST, calls a LAMBDA function which validates the format of that data and stores that in DB of your choice. Preferable Dynamo DB or Redis. This should take 45 minutes

## Features:
	* Create User Route
		* Creates a user
		* Unique email validation
		* Password validation
		* String and length field validation
	
	* List Users Route
		* Lists users
		* User friendly dates
		* Default sort by email

## Notes:

1. Email is the partition key, and the only field that is nessacerily unique, since we're using a DynamoDB is a key:value store to save our users.

2. Since it's a simple app, I put helper function directly underneath the handlers that use them instead of in a utils file.

## Routes

### POST /users 

Creates a new user with a unique email address.

#### Example Request:

```
curl -d '{"name": "sam", "email": "test@test.com", "password": "Test123676767"}' \
-H "Content-Type: application/json" \
-X POST https://st23564ow0.execute-api.us-east-1.amazonaws.com/dev/users
```

#### Example Response:

#### Success

```
{
	createdAt: timestamp,
	email: "",
	name: "",
	password: "",
	updatedAt: timestamp
}

```

## LIST /users

Lists all users, with their passwords encrypted.

This route mainly exists to make testing easier for the reviewer. Since this is a demo, there are no admins and this route is totally public.

#### Example Request:

_https://st23564ow0.execute-api.us-east-1.amazonaws.com/dev/users_

#### Example Response:

```
{
	count: 6,
	users: [{
		createdAt: timestamp,
		email: "",
		name: "",
		password: "",
		updatedAt: timestamp
	}]
}

```

## Set Up

### Develop Locally

_Note: You will need you're own set of AWS credentials_

_If the app fails to build for any locally for reason it can still be tested using the dev routes above._

```
cd [into_project]
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install local lambda dependencies &
# set up db
npm install
npm run build-dev
npm run dev

```

