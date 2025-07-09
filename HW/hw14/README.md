## Running postgress from Docker
docker run --name hil-pg-17.5 -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=hilleldb -e PGDATA=/var/lib/postgresql/data/pgdata -d -v "D:\Development\Python\hillel_2025_04_backend\HW\hw14\data":/var/lib/postgresql/data postgres:17.5
docker start hil-pg-17.5
docker exec -it hil-pg-17.5 /bin/bash
psql --username=admin --dbname=hilleldb

create table users (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
phone TEXT NOT NULL UNIQUE,
role TEXT NOT NULL CHECK (role IN ('ADMIN', 'USER', 'SUPPORT'))
);

create table dishes (
id serial primary key,
name text not null,
price numeric(8, 2) not null check (price >= 0)
);

create table orders(
id serial primary key,
date DATE not null,
total numeric(10, 2) not null check (total >= 0),
status text not null check (status in ('PENDING', 'PROCESSING', 'DELIVERED')),
user_id integer not null REFERENCES users(id)
);

create table order_items(
id serial primary key,
order_id integer not null references orders(id),
dish_id integer not null references dishes(id),
quantity integer not null check (quantity > 0)
);



"""
1. Why not add create to constructor?
2. Should delete raise exception if no such id
3. How to implement filter with >,<,like etc
4. What if several items will be returned in get? We use only first
5. Order has price > 0, and OrderItem has order_id not null. What should be created first?
"""