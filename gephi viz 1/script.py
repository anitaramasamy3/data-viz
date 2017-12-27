import csv
import json
import time
import tweepy
import urllib2 as u2
#from pprint import pprint


# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
    with open(key_file)as data_file:
    	data=json.load(data_file)
#    print data["token"]
   # data[]
    # Load keys here and replace the empty strings in the return statement with those keys

    return data["api_key"],data["api_secret"],data["token"],data["token_secret"]

# Q1.b.(i) - 5 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    user=api.get_user(root_user)
    print user.screen_name
    for friend in user.friends(count=no_of_friends):
	primary_friends.append((root_user,friend.screen_name))
    print "no of friends of %s is %d"%(root_user,len(primary_friends))
    # Add code here to populate primary_friends
    return primary_friends
def getPrimaryFollowers(api, root_user, no_of_followers):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_followers = []
    user=api.get_user(root_user)
    print user.screen_name
    for follower in user.followers(count=no_of_followers):
        primary_followers.append((root_user,follower.screen_name))
    print "no of followers of %s is %d"%(root_user,len(primary_followers))
    # Add code here to populate primary_followers
    g=[(t[1],t[0]) for t in primary_followers]
    return g

# Q1.b.(ii) - 7 points
def getNextLevelFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    nlf=[]
    flist=[x[1] for x in friends_list]
    for f in flist:
	nlf.append(getPrimaryFriends(api,f,no_of_friends))
#    print f
#    print  "nlf   ",nlf    
    next_level_friends = []
    # Add code here to populate next_level_friends
    next_level_friends=sublistIt(nlf)
    return next_level_friends
#    return nlf

# Q1.b.(iii) - 7 points
def getNextLevelFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])    
    nlf=[]
    flist=[x[1] for x in followers_list]
    for f in flist:
        nlf.append(getPrimaryFollowers(api,f,no_of_followers))
#    print f
#    print  "nlf   ",nlf
    next_level_followers = []
    # Add code here to populate next_level_friends
    next_level_followers=sublistIt(nlf)
#    g=[(t[1],t[0]) for t in next_level_followers]
#    print "g",g
    return next_level_followers

    # Add code here to populate next_level_followers
#    return next_level_followers
def sublistIt(flist):
    q=[]
    for sublist in flist:
	for item in sublist:
		q.append(item)
    return q
# Q1.b.(i),(ii),(iii) - 4 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the 
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends. 
    pf=getPrimaryFriends(api, root_user, no_of_neighbours)
    nlf=getNextLevelFriends(api,pf,no_of_neighbours)
    nlfl=getNextLevelFollowers(api,pf,no_of_neighbours)
    pf.extend(nlf)
    pf.extend(nlfl)
    print "final pf",pf
    all_edges = pf 
    #Add code here to populate all_edges
    return all_edges


# Q1.b.(i),(ii),(iii) - 5 Marks
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file,'wb')as fp:
	csv_fp=csv.writer(fp)
	csv_fp.writerow(['source','target'])
	for row in data:
		csv_fp.writerow(row)
#	fp.write('%s %s\n'%str(edge) for edge in data)
    pass




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)
    #pf=getPrimaryFriends(api, root_user, no_of_friends)
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    pf=getPrimaryFriends(api, ROOT_USER, NO_OF_NEIGHBOURS)
#    print "test code "
#    print "primary fr",pf
#    pfl=getPrimaryFollowers(api,ROOT_USER,NO_OF_NEIGHBOURS)
#    print "test code "
#    print "primary fl",pfl
    nlf=getNextLevelFriends(api,pf,NO_OF_NEIGHBOURS)
#    nlf1=[]
#    nlf1=sublistIt(nlf)
#    print "next lvl friends ",nlf
    nlfl=getNextLevelFollowers(api,pf,NO_OF_NEIGHBOURS)
#    print "next lvl followers ",nlfl
    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)
#    print "edges",edges
    writeToFile(edges, OUTPUT_FILE_GRAPH)
    

if __name__ == '__main__':
    testSubmission()

