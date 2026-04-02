import glob, json,urllib.request

# all_match_ids = []
# for f in glob.glob("../matches/*.json"):
#     matches = json.load(open(f))
#     for m in matches:
#         all_match_ids.append(m["match_id"])

# print(f"Found {len(all_match_ids)} matches to download events for")

# for mid in all_match_ids:
#     url = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{mid}.json"
#     out = f"{mid}.json"
#     print(f'Downloading events for {mid}')
#     urllib.request.urlretrieve(url,out)

events = json.load(open('3888706.json'))
shots = [e for e in events if e['type']['name'] =='Shot']
print(f'Total shots is {len(shots)}')
import pprint
pprint.pprint(shots[0])