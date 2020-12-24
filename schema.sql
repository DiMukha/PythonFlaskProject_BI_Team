DROP TABLE IF EXISTS users;

CREATE TABLE "users" (
	"id" INTEGER NOT NULL,
	"firstname" text NOT NULL,
	"lastname" text NOT NULL,
	"username" text NOT NULL UNIQUE,
	"email" text NOT NULL UNIQUE,
	"password" text NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)