\# ShopEase User Management Microservice



\## Project Overview



The ShopEase User Management Microservice is an independent backend service responsible for managing customer profiles and delivery addresses in the ShopEase e-commerce platform.



It is built using FastAPI and MySQL and integrates with the ShopEase Authentication Microservice for JWT-based authentication.



\## Features



\### User Profile Management

\- Create user profiles.

\- Retrieve authenticated user profiles.

\- Update complete profiles.

\- Partially update profile information.

\- Delete user profiles.

\- Prevent duplicate profiles for the same authentication account.



\### Address Management

\- Create delivery addresses.

\- Retrieve all addresses belonging to the authenticated user.

\- Retrieve individual addresses.

\- Update and delete addresses.

\- Set a default delivery address.

\- Enforce address ownership.



\### Security

\- JWT-based authentication.

\- Integration with the ShopEase Authentication Microservice.

\- Protection against unauthorized access.

\- User-specific data access and ownership validation.



\## Technology Stack



\- Python 3.12

\- FastAPI

\- MySQL 8

\- SQLAlchemy

\- Alembic

\- Pydantic

\- JWT Authentication

\- Docker

\- Docker Compose

\- Uvicorn

\- Swagger UI



\## Project Structure



```text

shopease-user-service/

│

├── app/

│   ├── core/

│   │   ├── config.py

│   │   └── security.py

│   │

│   ├── database/

│   │   └── connection.py

│   │

│   ├── models/

│   │   ├── user\_model.py

│   │   └── address\_model.py

│   │

│   ├── schemas/

│   │   ├── user\_schema.py

│   │   └── address\_schema.py

│   │

│   ├── services/

│   │   ├── user\_service.py

│   │   └── address\_service.py

│   │

│   ├── routers/

│   │   ├── user\_routes.py

│   │   └── address\_routes.py

│   │

│   └── main.py

│

├── alembic/

├── .dockerignore

├── .gitignore

├── alembic.ini

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

└── README.md

```



\## Microservice Configuration



The service uses its own MySQL database:



\- Database: `shopease\_user\_db`

\- API port: `8005`

\- MySQL host port: `3308`

\- Authentication Service port: `8004`



Configure your local `.env` file using the required environment variable names from `app/core/config.py` and `docker-compose.yml`.



Do not commit `.env` or any real credentials to GitHub.



\## Running with Docker



\### 1. Clone the repository



```bash

git clone https://github.com/YOUR\_GITHUB\_USERNAME/shopease-user-service.git

cd shopease-user-service

```



\### 2. Configure environment variables



Create a `.env` file and configure your database credentials and authentication service settings.



\### 3. Build Docker containers



```bash

docker compose build

```



\### 4. Start services



```bash

docker compose up -d

```



\### 5. Run database migrations



```bash

docker compose exec user-api alembic upgrade head

```



\### 6. Check containers



```bash

docker compose ps

```



\### 7. Stop services



```bash

docker compose down

```



To remove containers and the database volume, use `docker compose down -v` only when you intentionally want to delete the stored database data.



\## API Documentation



Once the service is running, open:



\*\*Swagger UI:\*\* http://localhost:8005/docs



\*\*Root endpoint:\*\* http://localhost:8005/



\*\*Health endpoint:\*\* http://localhost:8005/health



\## API Endpoints



\### User Profile



| Method | Endpoint | Description |

|---|---|---|

| POST | `/api/users/profile` | Create profile |

| GET | `/api/users/profile` | Get profile |

| PUT | `/api/users/profile` | Update profile |

| PATCH | `/api/users/profile` | Partially update profile |

| DELETE | `/api/users/profile` | Delete profile |



\### Address Management



| Method | Endpoint | Description |

|---|---|---|

| POST | `/api/users/addresses` | Create address |

| GET | `/api/users/addresses` | List addresses |

| GET | `/api/users/addresses/{address\_id}` | Get address |

| PUT | `/api/users/addresses/{address\_id}` | Update address |

| DELETE | `/api/users/addresses/{address\_id}` | Delete address |

| PATCH | `/api/users/addresses/{address\_id}/default` | Set default address |



\## Database Migrations



Alembic is used to manage database schema changes.



Create a migration:



```bash

alembic revision --autogenerate -m "migration description"

```



Apply migrations:



```bash

alembic upgrade head

```



Check the current migration:



```bash

alembic current

```



\## Testing



API endpoints can be tested using Swagger UI or Postman.



The implemented API functionality includes profile management, address management, JWT authentication, duplicate profile handling, and address ownership checks.



\## Integration



The User Management Microservice communicates with the ShopEase Authentication Microservice to validate JWT tokens.



It is designed to operate independently and can be integrated with other ShopEase services, including Product and Order Management.



\## Author



ShopEase User Management Microservice Project



