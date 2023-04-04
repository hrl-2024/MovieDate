DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
	uid				    SERIAL PRIMARY KEY,
	uname 				TEXT,
	avatar				BLOB
);

