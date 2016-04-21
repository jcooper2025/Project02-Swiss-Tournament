-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop the database if it exists to allow this file to be run multiple times.
-- then create and connect to the database.
DROP DATABASE IF EXISTS tournaments;
CREATE DATABASE tournaments;
\c tournaments

-- set up the tables and views that will be needed.

CREATE TABLE players (
	name text,
	id serial PRIMARY KEY );
	
CREATE TABLE matches (
	winner int REFERENCES players(id),
	loser int REFERENCES players(id),
	id serial PRIMARY KEY);

-- Views

CREATE VIEW number_wins AS
      SELECT players.id, players.name,COUNT(matches.winner) AS wins
      FROM players LEFT JOIN matches ON players.id=matches.winner
      GROUP BY players.id ORDER BY wins desc;

CREATE VIEW number_games AS
      SELECT players.id, players.name,COUNT(distinct(matches.winner, matches.loser)) AS games
      FROM players LEFT JOIN matches ON players.id=matches.winner OR players.id=matches.loser
      GROUP BY players.id ORDER BY games desc;

CREATE VIEW player_standing AS
      SELECT number_wins.id, number_wins.name, number_wins.wins, number_games.games
      FROM number_wins JOIN number_games ON number_wins.id = number_games.id;


INSERT INTO players (name) VALUES ('player01'), ('player02'), ('player03'), 
      ('player04'), ('player05'), ('player06'), ('player07'), ('player08'), 
      ('player09'), ('player10'), ('player11'), ('player12'), ('player13'), 
      ('player14'), ('player15'), ('player16');
      