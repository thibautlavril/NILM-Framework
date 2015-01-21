import json

metadata_Blued = {
    "number_users": 1,
    "users": {
        'user1': {
            "user_id": 'blued',
            "number_meters": 1,
            "meters": {
                'meter1': {
                    "user_id": 1,
                    "meter_id": 1,
                    "number_datasets": 2,
                    "measurements": [('A', 'P'), ('A', 'Q'),
                                     ('B', 'P'), ('B', 'Q')],
                    "tz": "US/Eastern"
                }
            }
        }
    }
}

outputfilename = 'blued.json'
with open(outputfilename, 'wb') as outfile:
    json.dump(metadata_Blued, outfile)
