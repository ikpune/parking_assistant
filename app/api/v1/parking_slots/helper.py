from flask import g


class UserParkingSlotsHelper(object):

    def __init__(self):
        self.data = {}

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def _get_data_object(self):

        self.data = {
            "id": "",
            "lat": "",
            "long": "",
            "is_reserved": False
        }

        return self.data

    def get_user_parking_slots_data(self, user_parking_slots=None):

        if user_parking_slots:
            user_parking_slots = user_parking_slots
        else:
            user_parking_slots = g.current_user.parking_slots

        response_data = []

        for ps in user_parking_slots:
            dict1 = self._get_data_object()

            dict1["id"] = ps.id
            dict1["lat"] = ps.lat
            dict1["long"] = ps.long
            dict1["is_reserved"] = ps.is_reserved
            response_data.append(dict1)

        return response_data
