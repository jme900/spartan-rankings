import spartan_api as sp_api
from spartan_rankings import rank_age_groupers, rank_elites

series = 'North American'
race_name = 'Poconos, PA'
start_at = 0
api_url = "https://cerberus.spartan.com/api/v1/races/7853/rankings?search=&page_size=15&id=7853&heat=Friday+3K+Elite+Series+-+Elite&event_id=9734&token=ts:1692689564114,context:race_7853,hash:ii438RSKUW3Lj5K0NnsUzVRSbN_vKtvLS4w84bwabiI%3D"
# sp_api.save_rankings_from_api(api_url, series, race_name, start_at)
# print(f'{race_name}: Finished saving rankings from API.')
# rank_age_groupers(series, race_name)
# print(f'{race_name}: Finished adding scores for all athletes.')
sp_api.save_elite_rankings_from_api(api_url, series, race_name)
print(f'{race_name}: Finished saving rankings from API.')
rank_elites(series, race_name)
print(f'{race_name}: Finished adding scores for the elites.')

