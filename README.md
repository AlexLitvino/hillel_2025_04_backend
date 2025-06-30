# hillel_2025_04_backend

## Lesson 01
- Descriptors
- Inheritance, MRO, C3 algorythm
- __name__ == '__main__'
- Python translation
- Linter
- Formatter
- Static types checkers
- LSP (Language Server Protocol)


## Lesson 02
- Iterators
- Loops
- Functions
- `DIGITAL JOURNALS` project discussion/implementation


##
- pipenv
- poetry - useful for publishing to PyPI
- uv


## Lesson 14
\c uc - connect to db uc
\d table_name - get table description
\x - show table data in vertical view
\q - quit
\l - all database
\dt - ???

CREATE DATABASE catering;
\c catering
CREATE TABLE users(
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
phone TEXT NOT NULL UNIQUE,
role TEXT NOT NULL CHECK (role IN ('ADMIN', 'USER', 'SUPPORT'))
)

nextval?
CURRENT_DATE function

CQRS and CQS

Transactions:
BEGIN
ROLLBACK

LIKE vs ILIKE ???

Client TablePlus