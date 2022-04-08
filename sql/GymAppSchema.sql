CREATE TABLE IF NOT EXISTS login(
email VARCHAR(256) NOT NULL UNIQUE
password VARCHAR(256) NOT NULL,
type VARCHAR(64) NOT NULL CONSTRAINT type CHECK( type = 'member' OR type = 'trainer' OR type = 'gym'),
PRIMARY KEY (email,type)
);

CREATE TABLE IF NOT EXISTS focus(
focus VARCHAR(256) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS trainer(
id INT GENERATED ALWAYS AS IDENTITY,
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
level VARCHAR(64) NOT NULL,
FOREIGN KEY (email) REFERENCES login(email) 
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS member(
id INT GENERATED ALWAYS AS IDENTITY,
email VARCHAR(256) PRIMARY KEY,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
gender VARCHAR(16) NOT NULL CONSTRAINT gender CHECK(gender = 'M' OR gender = 'F'),
level VARCHAR(64) NOT NULL,
preferred_gym_location VARCHAR(256) NOT NULL,
budget NUMERIC NOT NULL,
focus1 VARCHAR(64) REFERENCES focus(focus),
focus2 VARCHAR(64) REFERENCES focus(focus),
focus3 VARCHAR(64) REFERENCES focus(focus),
FOREIGN KEY (email) REFERENCES login(email) 
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED
);



CREATE TABLE IF NOT EXISTS gym(
id INT GENERATED ALWAYS AS IDENTITY,
name VARCHAR(256) NOT NULL,
email VARCHAR(256) PRIMARY KEY,
address VARCHAR(256) NOT NULL,
upper_price_range NUMERIC NOT NULL CHECK(upper_price_range > 0),
lower_price_range NUMERIC NOT NULL CHECK(lower_price_range > 0),
capacity NUMERIC NOT NULL CHECK(capacity > 0),
level VARCHAR(64) NOT NULL CONSTRAINT level CHECK(level = 'Beginner' OR level = 'Intermediate' OR level = 'Advanced'),
region VARCHAR(16) NOT NULL CONSTRAINT region CHECK(region = 'North' OR region = 'South' OR region = 'East' OR region = 'West' OR region = 'Central'),
FOREIGN KEY (email) REFERENCES login(email) 
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED
);


CREATE TABLE IF NOT EXISTS member_trainer(
member_email VARCHAR(256) REFERENCES member(email)
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
trainer_email VARCHAR(256) REFERENCES trainer(email)
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
trainer_rating NUMERIC,
UNIQUE(member_email, trainer_email)
);


CREATE TABLE IF NOT EXISTS member_gym(
member_email VARCHAR(256) REFERENCES member(email)
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
gym_email VARCHAR(256) REFERENCES gym(email)
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
gym_rating NUMERIC CONSTRAINT gym_rating CHECK(gym_rating<=5),
UNIQUE(member_email, gym_email)
);

CREATE TABLE IF NOT EXISTS gymfocus(
gym_email VARCHAR(256),
focus VARCHAR(64) REFERENCES focus(focus)
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
FOREIGN KEY (gym_email) REFERENCES gym(email)
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
PRIMARY KEY (gym_email,focus)
);

CREATE TABLE trainer_ratings( 
trainer_email VARCHAR(64) REFERENCES trainer(email),
	ON UPDATE CASCADE ON DELETE CASCADE
	DEFERRABLE INITIALLY DEFERRED,
rating NUMERIC CONSTRAINT rating CHECK(rating<=5)
);

CREATE OR REPLACE FUNCTION insert_trainer()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
-- trainer automatically added to trainer_ratings if not inside
    INSERT INTO trainer_ratings VALUES(NEW.email, NULL);
	
	RETURN NEW;
END;
$$;

-- inserting into trainer_rating table once new trainer
CREATE OR REPLACE TRIGGER insert_trainer
AFTER INSERT
ON trainer
FOR EACH ROW
EXECUTE PROCEDURE insert_trainer();

-- Trigger Function
CREATE OR REPLACE FUNCTION train_ratings()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
DECLARE 
	num NUMERIC;
	sum1 numeric;
BEGIN
-- if new trainer rating is null, no need do anything
	IF NEW.trainer_rating ISNULL THEN
		RAISE NOTICE'Rating is null';
	ELSE
		SELECT COUNT(DISTINCT mt.member_email), SUM(mt.trainer_rating)
		INTO num, sum1
		FROM member_trainer mt
		WHERE mt.trainer_email = NEW.trainer_email
		GROUP BY mt.trainer_email;
		
	-- if trainer rating was null
		IF num = 0 THEN
			UPDATE trainer_ratings
        	SET rating = NEW.trainer_rating
       		WHERE trainer_email = NEW.trainer_email;
		ELSIF (TG_OP = 'UPDATE') THEN
	-- trainer email and new rating not null, existing relation
			UPDATE trainer_ratings
        	SET rating = ROUND((sum1 - OLD.trainer_rating + NEW.trainer_rating)/num,2)
        	WHERE trainer_email = NEW.trainer_email;
		ELSE
	-- if trainer rating and new rating not null, insert new relation
        	UPDATE trainer_ratings
        	SET rating = ROUND(( sum1 + NEW.trainer_rating)/(num+1),2)
        	WHERE trainer_email = NEW.trainer_email;
		END IF;
    END IF;

    RETURN NEW;
END;
$$;


-- TRAINER trigger
CREATE OR REPLACE TRIGGER calc_trainer
BEFORE UPDATE OR INSERT
ON member_trainer
FOR EACH ROW
EXECUTE PROCEDURE train_ratings();

CREATE TABLE gym_ratings( 
    gym_email VARCHAR(64) REFERENCES gym(email),
    rating NUMERIC CONSTRAINT rating CHECK(rating<=5)
);

CREATE OR REPLACE FUNCTION insert_gym()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
-- trainer automatically added to trainer_ratings if not inside
    INSERT INTO gym_ratings VALUES(NEW.email, NULL);
	RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER insert_gym
AFTER INSERT
ON gym
FOR EACH ROW
EXECUTE PROCEDURE insert_gym();

-- Trigger Function
CREATE OR REPLACE FUNCTION gym_ratings()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
DECLARE 
	num NUMERIC;
	sum1 NUMERIC;
BEGIN
-- if trainer email dont exists in trainer_ratings
    IF NEW.gym_rating ISNULL THEN
		RAISE NOTICE'Rating is null';
	ELSE
		SELECT COUNT(DISTINCT mg.member_email), SUM(mg.gym_rating)
		INTO num, sum1
		FROM member_gym mg
		WHERE mg.gym_email = NEW.gym_email
		GROUP BY gym_email;
		
	-- if trainer rating is null
		IF num = 0 THEN
			UPDATE gym_ratings
        	SET rating = NEW.gym_rating
       		WHERE gym_email = NEW.gym_email;
		ELSIF (TG_OP = 'UPDATE') THEN
			UPDATE gym_ratings
        	SET rating = ROUND((sum1 - OLD.gym_rating + NEW.gym_rating)/num,2)
        	WHERE gym_email = NEW.gym_email;
	-- if trainer rating and new rating not null
		ELSE
        	UPDATE gym_ratings
        	SET rating = ROUND((sum1+ NEW.gym_rating)/(num+1),2)
        	WHERE gym_email = NEW.gym_email;
		END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER calc_gym
BEFORE UPDATE OR INSERT
ON member_gym
FOR EACH ROW
EXECUTE PROCEDURE gym_ratings();
