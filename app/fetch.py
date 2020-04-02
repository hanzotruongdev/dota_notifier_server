from flask import jsonify, json
from .models import LiveMatch, User, Player
import requests
from .utils import process_new_match, push_msg_to_topic

def fetch_data(app, db):

    # fetch live matches from OpenDota api
    print("Fetching live matches from OpenDota api...")
    uri = "https://api.opendota.com/api/live"
    try: 
        res = requests.get(uri)
    except:
        print("Fetch live match error!")
        return 
    
    jres = res.text
    current_live_matches = json.loads(jres)
    current_live_match_id_list = [str(m['match_id']) for m in current_live_matches]
    
    # get live match id saved in our dataset
    print("Fetching live matches saved in our db...")
    db_live_matches = LiveMatch.query.all()
    saved_live_match_id_list = [m.id for m in db_live_matches]

    # delete ended matches in db
    ended_matches = []
    for m in db_live_matches:
        if not m.id in current_live_match_id_list:
            ended_matches.append(m.id)
            db.session.delete(m)

    print("Ended match: ", ended_matches)

    # calculate ended matches and new matches to update our db
    new_matches = []

    for id in current_live_match_id_list:
        if not id in saved_live_match_id_list:
            new_matches.append(id)

    print("new matches: ", new_matches)

    # add new matches to database
    for id in new_matches:
        m = LiveMatch(id = id)
        db.session.add(m)

    db.session.commit()


    # send new match to FCM
    print ("Push notification")
    for id in new_matches:
        for match in current_live_matches:
            if id == str(match['match_id']):
                # process for new match
                process_new_match(match)
                break

    print("Done!")


def fetch_players(app, db):

    # fetching Pro Player list from Open Dota API
    print("fetching Pro Players list from OpenDota api...")
    uri = "https://api.opendota.com/api/proPlayers"

    try:
        response = requests.get(uri)
    except:
        print("error in the fect_players function")
        return

    jres = json.loads(response.text) # jres contain a list of players
    total = len(jres)
    if (total == 0):
        print("No Pro Players info optained")
        return

    # delete all player in table player
    try:
        num_rows_deleted = db.session.query(Player).delete()
        db.session.commit()
        print("deleted rows: ", num_rows_deleted)
    except:
        db.session.rollback()

    # parse the responded json result and add to the player table
    for i, p in enumerate(jres):
        player = Player(id = p['account_id'], steam_id = p['steamid'], name = p['name'], team_tag = p['team_tag'])
        db.session.add(player)
        if i%100 == 0:
            db.session.commit()
            print("number of inserted rows: %d/%d" % (i, total))
    
    db.session.commit()
    print("Total inserted rows: ", )

    print("Done!")



def test_firebase(topic="test"):
    from firebase_admin import messaging

    push_msg_to_topic('496.KilluaA has just started a new match!', '496.KilluaA is starting a new match with Abed, and 6 others!', 'all', '123')


def test_process_user():
    new_matches = [{"activate_time":1585022592,"deactivate_time":1585025212,"server_steam_id":"90133738413893643","lobby_id":"26591888796882004","league_id":11806,"lobby_type":1,"game_time":1698,"delay":300,"spectators":323,"game_mode":2,"average_mmr":0,"match_id":5310580505,"series_id":0,"sort_score":8323,"last_update_time":1585024896,"radiant_lead":34718,"radiant_score":36,"dire_score":8,"players":[{"account_id":247001423,"hero_id":46},{"account_id":293529846,"hero_id":84,"name":"dw","country_code":"","fantasy_role":0,"team_id":0,"team_name":"Team Max","team_tag":"MAX","is_locked":False,"is_pro":True,"locked_until":None},{"account_id":147488585,"hero_id":128},{"account_id":857500404,"hero_id":11},{"account_id":1016905725,"hero_id":126},{"account_id":316126139,"hero_id":88},{"account_id":446624286,"hero_id":12},{"account_id":128660724,"hero_id":110,"name":"Rico","country_code":"it","fantasy_role":2,"team_id":7453020,"team_name":"Aster.Aries","team_tag":"Aries","is_locked":True,"is_pro":True,"locked_until":None},{"account_id":139189820,"hero_id":56}],"building_state":16711817}]
    process_new_match(new_matches[0])