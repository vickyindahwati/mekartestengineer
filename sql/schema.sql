DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
	"customer_number" varchar(10) NOT NULL PRIMARY KEY,
	"name" varchar NOT NULL
);

CREATE TABLE account (
	"account_number" varchar(10) NOT NULL PRIMARY KEY,
	"customer_number" varchar(10) NOT NULL,
	"balance" integer NOT NULL,
	FOREIGN KEY (customer_number) REFERENCES customer(customer_number)
);

SELECT version();
