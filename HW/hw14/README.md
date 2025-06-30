## Running postgress from Docker
docker run --name hil-pg-17.5 -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=hilleldb -e PGDATA=/var/lib/postgresql/data/pgdata -d -v "D:\Development\Python\hillel_2025_04_backend\HW\hw14\data":/var/lib/postgresql/data postgres:17.5
