#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournaments")

def have_not_played_before(winner, loser):
    """This function takes in two players and checks to see if they have been
       matched up in a game before. It returns true if they have never played
       before. If they have played before it returns false.
       """
    dbconnect = connect()
    dbcursor = dbconnect.cursor()

    view_command = "CREATE VIEW players_games AS SELECT * \
                   FROM matches WHERE matches.winner=%s \
                   OR matches.loser=%s"%(winner[0], winner[0])

    previous_games = "SELECT * FROM players_games \
                     WHERE players_games.winner = %s \
                     OR players_games.loser = %s;"%(loser[0], loser[0])

    dbcursor.execute(view_command)
    dbcursor.execute(previous_games)
    any_matches = dbcursor.fetchall()

    dbconnect.close()

    if any_matches:
        # there was data in the previous games table
        return False  # they have played before
    else:
        return True   # they have not played before

def deleteMatches():
    """Remove all the match records from the database."""
    dbconnect = connect()
    dbcursor = dbconnect.cursor()

    #drop_command = "DROP TABLE IF EXISTS matches CASCADE;"
    del_command = "TRUNCATE TABLE matches CASCADE" #"DELETE FROM MATCHES;"
    create_command = "CREATE TABLE matches ( \
	winner int REFERENCES players(id), \
	loser int REFERENCES players(id), \
	id serial PRIMARY KEY);"
    dbcursor.execute(del_command)
    dbconnect.commit()
##    #dbcursor.execute(create_command)
##    dbconnect.commit()
    dbconnect.close()


def deletePlayers():
    """Remove all the player records from the database."""
    dbconnect = connect()
    dbcursor = dbconnect.cursor()

    #drop_command = "DROP TABLE IF EXISTS players CASCADE;"
    del_command = "TRUNCATE TABLE players CASCADE" #"DELETE FROM players;"

    create_command = "CREATE TABLE players ( \
	name text, \
	id serial PRIMARY KEY );"
    dbcursor.execute(del_command)
    dbconnect.commit()
##    dbcursor.execute(create_command)
##    dbconnect.commit()
    dbconnect.close()
    


def countPlayers():
    """Returns the number of players currently registered."""
    dbconnect = connect()
    dbcursor = dbconnect.cursor()
    sql_command = "select count(*) as num_rows from players;"
    dbcursor.execute(sql_command)
    num_players = dbcursor.fetchall()[0][0]
    dbconnect.close()
    return num_players



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    dbconnect = connect()
    dbcursor = dbconnect.cursor()
    # this way doesn't work: reg_player_command = "INSERT INTO players (name) VALUES (%s);",(name,)
    dbcursor.execute("INSERT INTO players (name) VALUES (%s);",(name,))
    dbconnect.commit()
    dbconnect.close()    


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    dbconnect = connect()
    dbcursor = dbconnect.cursor()
    # get the number of matches played. This is to work around problems with the player
    # standing view. When there are no matches played it still returns 1 for number of games.
    dbcursor.execute("SELECT COUNT(*) AS num_matches FROM MATCHES")
    num_matches = dbcursor.fetchall()[0][0]
    if num_matches == 0:
        # manually create return list
        dbcursor.execute("SELECT * FROM players;")
        player_list = dbcursor.fetchall()
        player_standings = []
        for person in player_list:
            player_standings.append((person[1], person[0], 0, 0))
    else: # there are matches so use the view to get the player standings
        sql_command = "SELECT * FROM player_standing;"
        dbcursor.execute(sql_command)
        player_standings = dbcursor.fetchall()
        
    dbconnect.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbconnect = connect()
    dbcursor = dbconnect.cursor()
#   this way doesn't work: report_command = "INSERT INTO matches(winner, loser) values (%s, %s);",(winner, loser)
    dbcursor.execute("INSERT INTO matches(winner, loser) values (%s, %s);",(winner, loser))
    dbconnect.commit()
    dbconnect.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    player_standings = playerStandings()

    standings = {}

    # separating players into different ranks based on the number of wins
    for player in player_standings:
        if player[2] not in standings.keys():
            # rank does not exist yet
            standings[player[2]] = [player]
        else:
            # add to existing rank
            standings[player[2]].append(player)


    swisspairs = []

    #match up players within the same rank. Initial version will assume that
    # the ranks are even.
    # TODO: test for an overall winner.
    for rank in standings.keys():
        possible_players = standings[rank]
        while possible_players != []:
            winner = possible_players[0]
            for loser in possible_players[1:]:
                if have_not_played_before(winner, loser):
                    swisspairs.append((winner[0], winner[1], loser[0], loser[1]))
                    possible_players.remove(winner)
                    possible_players.remove(loser)
                    break #break out of for loser loop to while possile_players loop
    return swisspairs



