#! python3
import praw
import requests

from PIL import Image
from io import BytesIO
from tqdm import tqdm

# praw constants
client_id = ''
client_secret = ''
redditHeaders = 'windows10:meme_delivery_axillv:v0.0.1a (by /u/AxillV)'

# setup headers for downloading images off of reddit and imgur etc.
headers = {'user-agent': 'windows10:meme_delivery_axillv:v0.0.1a (by /u/AxillV) www.reddit.com'}


# create a new reddit instance so we can start requesting information off of subreddits
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=redditHeaders)

# get the first 5 stickies of our dank memes subreddit and clear out duplicates
stickies = [reddit.subreddit('dankmemes').sticky(i).id for i in range(2)]
stickies = list(set(stickies))

# opens the text file that contains all submission id's that I have already fetched
submissionFile = open('submissionid.txt', 'a')

# for the first 20 + stickies hot submissions, get submission url, download and name each meme
# this ignores stickies, since they might contain text etc.
# TODO: Create a notepad and check if I've already downloaded each picture.
# TODO: Sort memes by week

for j, submission in enumerate(tqdm(reddit.subreddit('dankmemes').hot(limit=20 + len(stickies)))):
    if submission.id not in stickies:
        r = requests.get(submission.url, headers)
        i = Image.open(BytesIO(r.content))
        i.save('meme' + str(j - len(stickies) + 1) + '.png')
        submissionFile.write(submission.id + '\n')

# closes the text file with all the submission id's
submissionFile.close()
