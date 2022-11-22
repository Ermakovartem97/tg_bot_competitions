import sqlite3 as sl
from os import listdir

db_path = 'competitions'

def create_persons(con):
    sql_create_table_person = f"""
        CREATE TABLE PERSONS (
            person_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            company_name TEXT,
            person_tg TEXT
        );
    """
    with con:
        con.execute(sql_create_table_person)


def create_team(con):
    sql_create_table_person = f"""
        CREATE TABLE TEAMS (
            team_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            person_id_1 INTEGER,
            person_id_2 INTEGER,
            team_name TEXT
        );
    """
    with con:
        con.execute(sql_create_table_person)


def create_game(con):
    sql_create_table_person = f"""
        CREATE TABLE GAMES (
            game_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            team_id_1 INTEGER,
            team_id_2 INTEGER,
            score TEXT
        );
    """
    with con:
        con.execute(sql_create_table_person)


def create_new_conpetition(name):
    con = sl.connect(f'{db_path}\{name}.db')
    create_persons(con)
    create_team(con)
    create_game(con)
    return True


def insert_person(name_conpetition, data):
    con = sl.connect(f'{db_path}\{name_conpetition}.db')
    sql_insert_person = """
    INSERT INTO PERSONS (full_name, company_name, person_tg) values (?, ?)
    """
    with con:
        con.executemany(sql_insert_person, data)


def insert_team(con, data):
    sql_insert_person = """
    INSERT INTO TEAMS (person_id_1, person_id_2) values (?, ?)
    """
    with con:
        con.executemany(sql_insert_person, data)


def insert_game(con, data):
    sql_insert_person = """
    INSERT INTO GAMES (team_id_1, team_id_2) values (?, ?)
    """
    with con:
        con.executemany(sql_insert_person, data)


def sql_print(con, table):
    with con:
        data = con.execute(f'SELECT * FROM {table}')
        for row in data:
            print(row)


import pandas as pd


def take_all_persons(name_conpetition):
    con = sl.connect(f'{db_path}\{name_conpetition}.db')
    all_persons_df = pd.read_sql('SELECT * FROM PERSONS', con)
    return all_persons_df


def take_all_teams(name_conpetition):
    con = sl.connect(f'{db_path}\{name_conpetition}.db')
    all_teams_df = pd.read_sql('SELECT * FROM TEAMS', con)
    return all_teams_df

def take_all_games(name_conpetition):
    con = sl.connect(f'{db_path}\{name_conpetition}.db')
    all_games_df = pd.read_sql('SELECT * FROM GAMES', con)
    return all_games_df


def take_team_composition(name_conpetition, team_id):
    con = sl.connect(f'{db_path}\{name_conpetition}.db')
    take_team_composition = pd.read_sql(
        f'SELECT * FROM TEAMS tm LEFT JOIN PERSONS ps ON tm.person_id_1 = ps.person_id or tm.person_id_2 = ps.person_id WHERE team_id = {team_id}',
        con)
    return take_team_composition

def take_team_opponent(name_conpetition, team_id):
    con = sl.connect(f'{db_path}\{name_conpetition}.db')
    take_team_opponent = pd.read_sql(
        f'SELECT * FROM GAMES gs LEFT JOIN TEAM tm WHERE team_id_1 = {team_id} or team_id_2 = {team_id}',
        con)
    return take_team_opponent

def take_all_competitions():
    all_competitions = [_.split('.')[0] for _ in listdir('competitions/')]
    return all_competitions

def check_person_in_competition(competition_name, person_tg):
    all_persons = take_all_persons(competition_name)
    print(all_persons)
    if person_tg in all_persons['person_tg']:
        person_in_competition = True
    else:
        person_in_competition = False
    return person_in_competition


if __name__ == '__main__':
    create_new_conpetition_text = 1  # Ввод на создание соревнования
    if create_new_conpetition_text == 1:
        name_conpetition = 'ping-pong_11_2022'
        create_new_conpetition(name_conpetition)
    setting_team = 0  # Настройка количества игроков в команде (позже)
    if setting_team == 1:
        team_count = 2

    name_conpetition = 'ping-pong_11_2022'
    con = sl.connect(f'{name_conpetition}.db')

    #insert_person(con, [('Ермаков Артем Александрович', 'GPN'), ('San', 'GPN'), ('Megan', 'GPN'), ('Petr', 'GPN')])
    #insert_team(con, [(1, 2), (3, 4)])
    #insert_game(con, [(1, 2)])

    all_persons_df = take_all_persons(name_conpetition)
    # print(all_persons_df)
    all_teams_df = take_all_teams(name_conpetition)
    # print(all_teams_df)
    all_games_df = take_all_games(name_conpetition)
    #print(all_games_df)
    all_competitions = take_all_competitions()
    print(all_competitions)
    take_team_composition(name_conpetition, 1)
