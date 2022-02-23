"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View # imports from Django instead of rest_framework

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT u.id AS gamer_id, u.first_name || " " || u.last_name as full_name, e.id, e.date, e.time, g.title AS game_name
                FROM levelupapi_game AS g
                JOIN levelupapi_event AS e
                    ON g.id = e.game_id
                JOIN levelupapi_eventgamer AS egr
                    ON e.id = egr.event_id
                JOIN levelupapi_gamer AS gr
                    ON egr.gamer_id = gr.id
                JOIN auth_user AS u
                    ON u.id = gr.user_id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the event_id, date, time, and game_name from the row dictionary
                event = {
                    'id': row['id'],
                    'date': row['date'],
                    'time': row['time'],
                    'game_name': row['game_name'],
                }
                
                # This is using a generator comprehension to find the user_dict in the events_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_event in events_by_user:
                #     if user_event['gamer_id'] == row['gamer_id']:
                #         user_dict = user_eevnt
                
                user_dict = next(
                    (
                        user_event for user_event in events_by_user
                        if user_event['gamer_id'] == row['gamer_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'], # f"{row['first_name']} {row['last_name']}",
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)