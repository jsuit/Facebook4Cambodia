# post = graph.get_object(id='post_id')
# print(post['message'])

import facebook
import pprint
import requests
import itertools
import json

# 10153718401628224
pp = pprint.PrettyPrinter(indent=4)
# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAACEdEose0cBAJilAD7QFLz2GNsWPqbNQyRW4dZCSzPtcdb9mHcGAPsmUkEBMJNZBjVZA8yLoZAXe8eoWikvjx08ef6oZCviw3bcVbbUl2OfNzyl5AYSI7ywaPxbgJoh5z4jHl48sPvqmbucm5NpcQwCPr4H2OANcjt8NxVCj4gZDZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
user = 'us.embassy.phnom.penh'

graph = facebook.GraphAPI(access_token, version='2.6')
profile = graph.get_object(user)
videos = graph.get_connections(profile['id'], 'videos')

keys = videos.keys()

print keys
res = []

while True: # this keeps paginating requests until all posts on the timeline have been pulled
# while count < 3:
    try:
        res.append(videos['data'])
        # Attempt to make a request to the next page of data, if it exists.
        videos = requests.get(videos['paging']['next']).json()
    except KeyError:
        break
res = [item for sublist in res for item in sublist]
videos = {}
length = {}
desc = {}
time = {}
for item in res:
	print item
	item_id = item['id']
	time_vid = item['updated_time']
	try: 
		desc_vid = item['description'].encode("utf8")
		details = graph.get_object(id=item_id, fields='length,permalink_url')
		length_vid = details['length']
		time_vid = time
		# print item_id, length, desc, time
		desc[item_id] = desc_vid
		length[item_id] = length_vid
		time[item_id] = time_vid

	except KeyError: pass
	
json.dump(length,open('LengthOfVideos.txt','w'))
json.dump(length,open('DescriptionOfVideos.txt','w'))
json.dump(length,open('DateOfVideos.txt','w'))