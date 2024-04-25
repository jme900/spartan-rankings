import sqlite3
import os

sqlite_conn_str = os.getenv('SQLITE_DB')


# Connect to the SQLite database
conn = sqlite3.connect(sqlite_conn_str)
# Create a cursor object
cur = conn.cursor()


def _convert_to_seconds(time_string):
    hours, minutes, seconds = map(int, time_string.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def _execute_query(query, data):
    cur.execute(query, data)
    conn.commit()


def _select_query(query, data):
    cur.execute(query, data)
    return cur.fetchall()


def get_all_elites(series, race_name):
    query = ("SELECT athlete_user_id, rank_gender "
             "FROM elite_series "
             "WHERE race_name = ? AND series = ? "
             "ORDER BY gender ASC, rank_gender ASC;")
    return _select_query(query, (race_name, series))


def get_top_ag_athletes(series, race_name):
    query = ("SELECT age_group, gender, completion_time "
             "FROM national_series "
             "WHERE rank_age_group=1 AND race_name = ? AND series = ? "
             "ORDER BY age_group ASC, gender ASC;")
    return _select_query(query, (race_name, series))


def get_all_ag_athletes(series, race_name, age_group, gender):
    query = ("SELECT athlete_user_id, completion_time "
             "FROM national_series "
             "WHERE age_group = ? AND race_name = ? AND gender = ? AND series = ?;")
    return _select_query(query, (age_group, race_name, gender, series))


def update_ag_race_points(series, race_name, user_id, rank):
    update = ("UPDATE national_series "
              "SET race_points = ? "
              "WHERE series = ? AND race_name = ? AND athlete_user_id = ?;")
    _execute_query(update, (rank, series, race_name, user_id))


def update_elite_race_points(series, race_name, user_id, rank):
    update = ("UPDATE elite_series "
              "SET race_points = ? "
              "WHERE series = ? AND race_name = ? AND athlete_user_id = ?;")
    _execute_query(update, (rank, series, race_name, user_id))


def _valid_ag_ranking(rank):
    keys = ['completion_time', 'athlete_user_id', 'athlete_name', 'age_group',
            'gender', 'count_age_group', 'count_gender', 'count_overall',
            'rank_age_group', 'rank_gender', 'rank_overall']

    return all(rank.get(key) is not None for key in keys)


def _valid_elite_ranking(rank):
    keys = ['completion_time', 'athlete_user_id', 'athlete_name', 'gender',
            'count_gender', 'count_overall', 'rank_gender', 'rank_overall']

    return all(rank.get(key) is not None for key in keys)


def insert_elite_rankings(series, race_name, rankings):
    query = ("INSERT INTO elite_series ("
             "  'athlete_user_id', "
             "  'athlete_name', "
             "  'race_name', "
             "  'completion_time', "
             "  'gender', "
             "  'count_gender', "
             "  'count_overall', "
             "  'rank_gender', "
             "  'rank_overall', "
             "  'race_points', "
             "  'series'"
             ") VALUES(?,?,?,?,?,?,?,?,?,?,?)")
    for rank in rankings:
        if _valid_elite_ranking(rank):
            seconds_completed = _convert_to_seconds(rank.get('completion_time'))
            _execute_query(query, (
                rank.get('athlete_user_id'),
                rank.get('athlete_name'),
                race_name,
                seconds_completed,
                rank.get('gender'),
                rank.get('count_gender'),
                rank.get('count_overall'),
                rank.get('rank_gender'),
                rank.get('rank_overall'),
                rank.get('points'),
                series
            ))


def insert_ag_rankings(series, race_name, rankings):
    query = ("INSERT INTO national_series ("
             "  'athlete_user_id', "
             "  'athlete_name', "
             "  'race_name', "
             "  'age_group', "
             "  'completion_time', "
             "  'gender', "
             "  'count_age_group', "
             "  'count_gender', "
             "  'count_overall', "
             "  'rank_age_group', "
             "  'rank_gender', "
             "  'rank_overall', "
             "  'series'"
             ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)")
    for rank in rankings:
        if _valid_ag_ranking(rank):
            seconds_completed = _convert_to_seconds(rank.get('completion_time'))
            _execute_query(query, (
                rank.get('athlete_user_id'),
                rank.get('athlete_name'),
                race_name,
                rank.get('age_group'),
                seconds_completed,
                rank.get('gender'),
                rank.get('count_age_group'),
                rank.get('count_gender'),
                rank.get('count_overall'),
                rank.get('rank_age_group'),
                rank.get('rank_gender'),
                rank.get('rank_overall'),
                series
            ))
