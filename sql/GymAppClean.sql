/*******************

  Cleaning script

*******************/
DROP TRIGGER IF EXISTS calc_gym on member_gym;
DROP TRIGGER IF EXISTS calc_trainer on member_trainer;
DROP TRIGGER IF EXISTS insert_trainer on trainer;
DROP TRIGGER IF EXISTS insert_gym on gym;
DROP FUNCTION IF EXISTS gym_ratings();
DROP FUNCTION IF EXISTS train_ratings();
DROP FUNCTION IF EXISTS insert_gym();
DROP FUNCTION IF EXISTS insert_trainer();
DROP TABLE IF EXISTS gym_ratings;
DROP TABLE IF EXISTS trainer_ratings;
DROP TABLE IF EXISTS member_gym;
DROP TABLE IF EXISTS member_trainer;
DROP TABLE IF EXISTS gymfocus;
DROP TABLE IF EXISTS gym;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS trainer;
DROP TABLE IF EXISTS login;
DROP TABLE IF EXISTS focus;

