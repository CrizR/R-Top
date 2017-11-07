import requests
import json

class Reddit(object):

    def __init__(self):
        self.URL = "https://www.reddit.com"

    def build_url(self, args:[], limit)->str:
        """
        Builds the url given the arguments and limit
        :param args: Arguments to build the url with
        :return: String
        """
        res = self.URL + '/r/'
        for arg in args:
            res += str(arg) + '/'
        res += '.json?' + 'limit=' + str(limit)
        print(res)
        return res

    def get_type_post(self, subreddit, list_type, limit):
        """
        Retrieves the top posts, simplified for the Cisco API
        :param sub_reddit: The sub reddit to retrieve the top posts from
        :param list_type: The type of posts to retrieve (top, controversial.. etc)
        :param limit: The number of top posts to retrieve
        :return: JSON
        """
        payload = {"format": "json"}
        headers = {'User-agent': 'CiscoReddit'}
        args = [subreddit, list_type]
        response = requests.get(self.build_url(args, limit), data=payload, headers=headers)
        response = json.loads(response.text)
        return self.simplify_listing(response)

    def simplify_listing(self, jobject):
        """
        Removes unwanted json data from the JSON retrieved from the Reddit API
        :param jobject: Reddit Data
        :return: JSON
        """
        if 'error' in jobject:
            return jobject
        """
        Simplifies the JSON Object retrieved from the Reddit API into
        post title, url, score, gilded, and comments
        :param jobject:
        :param limit:
        :return:
        """
        listings = {
            "posts":[]
        }

        size = len(jobject["data"]["children"])
        for i in range(0, size):
            post_object = jobject["data"]["children"][i]["data"]
            title = ''
            link = ''
            upvotes = 0
            gilded = 0
            num_comments = 0
            if "title" in post_object:
                title = post_object["title"]
            if "url" in post_object:
                 link = post_object["url"]
            if "score" in post_object:
                upvotes = int(post_object["score"])
            if "gilded" in post_object:
                gilded = int(post_object["gilded"])
            if "num_comments" in post_object:
                num_comments = int(post_object["num_comments"])

            post = {
                    "title": title,
                    "link": link,
                    "upvotes": upvotes,
                    "num_comments": num_comments,
                    "gilded": gilded

            }
            listings["posts"].append(post)
        return listings


