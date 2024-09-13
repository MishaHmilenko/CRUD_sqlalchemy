# API ChatRooms
ChatRooms - own pet project, a platform for communication in online chats.

Project stack:
```
-FastAPI
-SQLAlchemy
-PostgreSQL
-Alembic
-WebSocket
```

>the project is written to strengthen technical skills 

## Project Deployment
1. Clone repository

    ```bash
    git clone https://github.com/MishaHmilenko/ChatRooms
    ```

2. Create `.env` file

    ```
    APP_PORT=80

    DB_USER=your_db_user
    DB_PASSWORD=yor_db_password
    DB_NAME=your_db_name
    DB_HOST=your_db_host
    DB_PORT=5432
    ```

3. Launching a project in containers

    ```bash
    docker-compose up --build
    ```
    
4.The application is available at

```
127.0.0.1:8000/docs
```
