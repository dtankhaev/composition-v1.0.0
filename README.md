# composition-v1.0.0
![yamdb_workflow](https://github.com/dtankhaev/composition-v1.0.0/actions/workflows/yamdb_workflow.yml/badge.svg)

composition-v1.0.0 project for the  service — collecting reviews of movies, books or music.

## Description

The composition-v1.0.0 project collects user reviews of works.
The works are divided into categories: "Books", "Films", "Music".
The list of categories can be expanded (for example, you can add the category "Fine Art" or "Jewelry").

### How to launch a project:

Everything described below applies to Linux OS.
Clone the repository and go to it:

```bash
git clone git@github.com:dtankhaev/composition-v1.0.0.git
```

Go to the folder with the docker-compose file.yaml:

```bash
cd infra
```

Lifting containers (infra_db_1, infra_web_1, infra_nginx_1):

```bash
docker-compose up -d --build
```

Performing migrations:

```bash
docker-compose exec web python manage.py migrate
```

Creating a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

Removing the static:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Stopping containers:

```bash
docker-compose down -v
```

### Filling template .env (not included in the current repository) located at the path infra/.env

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=key
```

### YaMDb API Documentation

Documentation is available at the endpoint: http://localhost/redoc/

### User roles

- **Anonymous** — can view descriptions of works, read reviews
and comments.
- **Authenticated user (user)** — can read everything, as well as Anonymous,
can publish reviews and rate works, can comment
reviews; can edit and delete their reviews and comments, edit
their ratings of works. This role is assigned by default to each new
user.
- **Moderator (moderator)** — the same rights as the Authenticated
the user, plus the right to delete and edit any reviews and comments.
- **Administrator (admin)** — full rights to manage all content
the project. Can create and delete works, categories and genres.
Can assign roles to users.
- **Django Superuser** must always have administrator rights,
a user with admin rights. Even if you change the user role
of the superuser, it will not deprive him of administrator rights. Superuser — always
an administrator, but an administrator is not necessarily a superuser.
