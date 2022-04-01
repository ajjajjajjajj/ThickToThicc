CREATE TABLE IF NOT EXISTS login(
email VARCHAR(256) NOT NULL UNIQUE,
password VARCHAR(256) NOT NULL,
type VARCHAR(64) NOT NULL CONSTRAINT type CHECK( type = 'member' OR type = 'trainer' OR type = 'gym'),
PRIMARY KEY (email,type)
);

CREATE TABLE IF NOT EXISTS focus(
focus VARCHAR(256) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS trainer(
email VARCHAR(256) PRIMARY KEY,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
gender VARCHAR(16) NOT NULL CONSTRAINT gender CHECK(gender = 'M' OR gender = 'F'),
upper_price_range NUMERIC NOT NULL CHECK(upper_price_range > 0),
lower_price_range NUMERIC NOT NULL CHECK(lower_price_range > 0),
experience NUMERIC NOT NULL CHECK(experience >= 0),
focus1 VARCHAR(64) NOT NULL,
focus2 VARCHAR(64) NOT NULL,
focus3 VARCHAR(64) NOT NULL,
level VARCHAR(64) NOT NULL CONSTRAINT level CHECK(level = 'Beginner' OR level = 'Intermediate' OR level = 'Advanced'),
FOREIGN KEY (email) 
    REFERENCES login(email)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS member(
email VARCHAR(256) PRIMARY KEY,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
gender VARCHAR(16) NOT NULL CONSTRAINT gender CHECK(gender = 'M' OR gender = 'F'),
level VARCHAR(64) NOT NULL CONSTRAINT level CHECK(level = 'Beginner' OR level = 'Intermediate' OR level = 'Advanced'),
preferred_gym_location VARCHAR(256) NOT NULL,
budget NUMERIC NOT NULL,
focus1 VARCHAR(64) REFERENCES focus(focus),
focus2 VARCHAR(64) REFERENCES focus(focus),
focus3 VARCHAR(64) REFERENCES focus(focus),
FOREIGN KEY (email) 
    REFERENCES login(email)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gym(
name VARCHAR(256) NOT NULL,
email VARCHAR(256) PRIMARY KEY,
address VARCHAR(256) NOT NULL,
upper_price_range NUMERIC NOT NULL CHECK(upper_price_range > 0),
lower_price_range NUMERIC NOT NULL CHECK(lower_price_range > 0),
capacity NUMERIC NOT NULL CHECK(capacity > 0),
level VARCHAR(64) NOT NULL CONSTRAINT level CHECK(level = 'Beginner' OR level = 'Intermediate' OR level = 'Advanced'),
region VARCHAR(16) NOT NULL CONSTRAINT region CHECK(region = 'North' OR region = 'South' OR region = 'East' OR region = 'West' OR region = 'Central'),
FOREIGN KEY (email) 
    REFERENCES login(email)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gymfocus(
gym_email VARCHAR(256),
focus VARCHAR(64) REFERENCES focus(focus) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (gym_email) REFERENCES gym(email),
PRIMARY KEY (gym_email,focus)
);


CREATE TABLE IF NOT EXISTS member_trainer(
member_email VARCHAR(256) REFERENCES member(email),
trainer_email VARCHAR(256) REFERENCES trainer(email),
trainer_rating NUMERIC CONSTRAINT trainer_rating CHECK(trainer_rating <= 5),
UNIQUE(member_email, trainer_email)
);

CREATE TABLE IF NOT EXISTS member_gym(
member_email VARCHAR(256) REFERENCES member(email),
gym_email VARCHAR(256) REFERENCES gym(email),
gym_rating NUMERIC CONSTRAINT gym_rating CHECK(gym_rating <= 5),
UNIQUE(member_email, gym_email)
);

