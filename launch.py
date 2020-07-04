from strava_api.data import get_activities

act = get_activities()[0]
print(act)

act.give_kudo()
