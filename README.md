# Rollee Task - Backend Engineer, Coverage Team

**F. Can Mekikoglu** - June 2023

📧 Email: [fcanmekikoglu@gmail.com](mailto:fcanmekikoglu@gmail.com)

---
## Quick Start Guide

```shell
git clone https://github.com/fcanmekikoglu/rollee_task.git

cd rollee_task

docker compose up
```

After executing these commands, the server should be accessible at `localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Description | Request Body | Response |
| ------ | -------- | ----------- | ------------ | -------- |
| POST   | /auth    | Authenticate on comet.co with user credentials. | `{ "username": "user@example.com", "password": "examplepass" }` | `{ "id": "uuid" }` |
| POST   | /pull    | Retrieve freelancer details using authenticated user's ID. | `{ "id": "uuid" }` | `{ "freelancer_id": "..." }` |

### Example Requests 

**1. Authentication (POST /auth)**

![Example request on /auth](https://firebasestorage.googleapis.com/v0/b/personal-host-b7997.appspot.com/o/Screenshot%202023-06-26%20at%2020.15.25.png?alt=media&token=039b06f2-6a9c-45d6-9495-613f2eea133d)

**2. Retrieve Freelancer Details (POST /pull)**

![Example request on /pull](https://firebasestorage.googleapis.com/v0/b/personal-host-b7997.appspot.com/o/Screenshot%202023-06-26%20at%2020.15.37.png?alt=media&token=01555e1e-19a1-453c-9144-df922c98a029)

---

## API Flow

#### **Authentication (/auth)**
1. Check if request method is POST. If not, return an error.
2. Validate content type as `application/json`. Return an error if it's different.
3. Parse request body into JSON. If parsing fails, return an error.
4. Check for `username` and `password` fields in the request. If either is missing, return an error.
5. Authenticate user. If authentication fails, return an error.
6. Look up user in the database, or create a new record if not found.
7. Return user's unique ID with a `200 OK` status code.

#### **Pull Freelancer Details (/pull)**
1. Check if request method is POST. If not, return an error.
2. Validate content type as `application/json`. If it's different, return an error.
3. Parse request body into JSON and extract the user ID. If parsing fails or ID is missing, return an error.
4. Look up user in the database using the provided ID. If not found, return an error.
5. Retrieve freelancer data using the user's credentials. If this process fails, return an error.
6. Update the user's Freelancer instance with the newly fetched data.
7. Serialize and return the associated Freelancer instance.
8. Handle any unexpected exceptions by returning an error with the exception message.

---

## Data Models

#### User

This model stores basic authentication information for users, including their email and password. A unique UUID is also assigned to each user as an ID.

#### Freelancer

This model has a one-to-one relationship with the User model. It holds professional details about a freelancer, such as:

- first_name
- last_name
- full_name


- job_title
- picture
- phone_number
- slack_username
- linkedin_url
- kaggle_url
- github_url
- iban
- experience_in_years
- biography

#### Experience

This model is linked to the Freelancer model with a one-to-many relationship. It contains details about the freelancer's past experiences, including:

- start_date
- end_date
- company_name
- description
- location

#### Skill

This model has a one-to-many relationship with the Experience model. It represents skills acquired during a particular experience, specified by its name.

---

## Tech Stack

- Django
- Django Rest Framework
- PostgreSQL
- Docker
