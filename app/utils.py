import re
import firebase_admin
from firebase_admin import credentials, messaging



# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for 
# for validating an Email 
def validate_email(email):  
  
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True 
          
    else:  
        return False


# for process live match on dota tv

def _format_notification_message(player, players):
    n = len(players)
    if (n == 8):
        return player['name'] + ' is playing a new Dota2 game with ' + ', '.join([p['name'] for p in players])
    if (n > 0 and n < 8):
        return player['name'] + ' is playing a new Dota2 game with ' + ', '.join([p['name'] for p in players]) + ', and ' + str(8-n) + ' others'
    else:
        return player['name'] + ' is playing a new Dota2 game'



    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)

def _get_player_name(player):
    if not "is_pro" in player:
        return "Unknown"
    
    if not "name" in player:
        return "Unknown"
    
    if "team_tag" in player and player['team_tag'] != None:
         return (player["team_tag"]+"."+player["name"])
    else: 
        return player["name"]
    

def process_new_match(new_match):
    proplayers = [{"id":str(m['account_id']), "name": _get_player_name(m)} for m in new_match['players'] if ('is_pro' in m and m['is_pro'] == True)]
    print("===> list pro player in this new match: ", proplayers)

    title = "A New match has started on DotaTV"
    topic_all = "all"

    for p in proplayers:
        
        message = _format_notification_message(p, [pp for pp in proplayers if pp["id"] != p["id"]])
        print("===> message for subscribers subscribing %s: " % p["name"], message)

        topic = p["id"]

        push_msg_to_topic(title, message, topic, new_match['lobby_id'])
    
    if len(proplayers) > 0:
        message = _format_notification_message(proplayers[0], proplayers[1:] if len(proplayers) > 1 else [])
        print("===> message for channel all: ", message)
        push_msg_to_topic(title, message, topic_all, new_match['lobby_id'])
    else:
        print("New match has no proplayer")


def push_msg_to_topic(title, message, topic, extra_data = ''):
    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        data={
            'matchid': extra_data
        },
        topic=topic,
    )

    res = messaging.send(message)

    print("Push notification return: ", res)