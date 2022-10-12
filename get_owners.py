import requests
import json
import csv
import time
import datetime

now = datetime.datetime.now()
owners = 'owners_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'

with open(owners, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['name','username','address','created_date'])

headers = {
        'User-Agent':'Mozilla/5.0'
}

with open('assets', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    for asset in reader:
        name = asset[0]
        asset_contract_address = asset[1]
        token_id = asset[2]
        url = 'https://api.opensea.io/api/v1/asset/'+ asset_contract_address + '/' + token_id + '/owners?limit=50&order_by=created_date&order_direction=desc'

        response = requests.get(
            url=url,
            headers=headers)
        response_json = json.loads(response.text)

        owners_list = response_json['owners']
        owners_dict = owners_list[0]

        if owners_dict['owner']['user'] is None:
            username = None
        else:
            username = owners_dict['owner']['user']['username']
        address = owners_dict['owner']['address']
        created_date = owners_dict['created_date']

        with open(owners, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, username, address, created_date])

        time.sleep(4)
