import json

metadata_Blued = {
    "number_users": 1,
    "users": {
        'user_blued': {
            "user_id": 'user_blued',
            "number_meters": 1,
            "meters": {
                'meter_blued': {
                    "user_id": 'user_blued',
                    "meter_id": 'meter_blued',
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
