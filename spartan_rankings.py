import spartan_db as db
ELITE_PTS = [
    300,
    264,
    236,
    216,
    204,
    192,
    180,
    168,
    156,
    144,
    132
]


def _generate_rank_for_age_groupers(series, race_name, age_group, gender, best_time):
    athletes = db.get_all_ag_athletes(series, race_name, age_group, gender)
    for u_id, completed_in in athletes:
        points = (best_time/completed_in) * 1000
        db.update_ag_race_points(series, race_name, u_id, points)


def rank_age_groupers(series, race_name):
    for ag, gender, secs in db.get_top_ag_athletes(series, race_name):
        print(f"Generating ranks for {race_name} | {ag}:{gender}")
        _generate_rank_for_age_groupers(series, race_name, ag, gender, secs)


def _generate_rank_for_elites(series, race_name):
    elites = db.get_all_elites(series, race_name)
    for u_id, rank_gender in elites:
        if rank_gender > 11:
            points = 132 - rank_gender - 11
        else:
            points = ELITE_PTS[rank_gender - 1]
        db.update_elite_race_points(series, race_name, u_id, points)


def rank_elites(series, race_name):
    for gender in ['male', 'female']:
        print(f"Generating ranks for {race_name} | {gender}")
        _generate_rank_for_elites(series, race_name)
