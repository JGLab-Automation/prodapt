__author__ = 'JG'

from requests import Session
from lib import utility as util
from tinydb import TinyDB, Query, where
from config import environment as env
from json import dumps, loads


class Test:

    def __init__(self):
        self.log = util.Log()
        self.session = Session()
        self.db_posts = TinyDB(f"{env.suite['workspace']}/artefacts/posts.json")
        self.db_comments = TinyDB(f"{env.suite['workspace']}/artefacts/comments.json")
        self.pcount = 0

    @staticmethod
    def collaborate(posts, comments):
        post = dict()
        for i in posts:
            comment = dict()
            for j in comments:
                if i['id'] == j['postId']:
                    post[f"post_{i['id']}"] = dict()
                    post[f"post_{i['id']}"]['post_title'] = i['title']
                    post[f"post_{i['id']}"]['post_body'] = i['body']
                    comment[f"comment_{j['id']}"] = dict()
                    comment[f"comment_{j['id']}"]['user_name'] = j['name']
                    comment[f"comment_{j['id']}"]['user_email'] = j['email']
                    comment[f"comment_{j['id']}"]['user_comment'] = j['body']
                    if 'post_comments' not in post[f"post_{i['id']}"]:
                        post[f"post_{i['id']}"]['post_comments'] = list()
                        post[f"post_{i['id']}"]['post_comments'].append(comment)
                    else:
                        post[f"post_{i['id']}"]['post_comments'].append(comment)
        return post

    def fetch_from_source(self):
        posts_url = 'https://jsonplaceholder.typicode.com/posts'
        comments_url = 'https://jsonplaceholder.typicode.com/comments'

        posts = util.HTTP(url=posts_url).get()
        comments = util.HTTP(url=comments_url).get()

        if isinstance(posts, list) and isinstance(comments, list):
            for post in posts:
                self.db_posts.insert(post)
                self.pcount += 1
            self.log.info(f"{self.pcount} posts successfully updated in the database")

            self.pcount = 0
            for comment in comments:
                self.db_comments.insert(comment)
                self.pcount += 1
            self.log.info(f"{self.pcount} comments successfully updated in the database")
            return 'success', None
        if (not isinstance(posts, list) and posts.find('error')) and (not isinstance(comments, list) and comments.find('error')):
            return 'failure', {'posts': posts, 'comments': comments}
        if not isinstance(posts, list) and posts.find('error'):
            return 'failure', {'posts': posts}
        if not isinstance(comments, list) and comments.find('error'):
            return 'failure', {'comments': comments}

    def view_post_details(self, post_id):
        posts = self.db_posts.all()
        if post_id == 'all':
            comments = self.db_comments.all()
        elif int(post_id) in range(1, len(posts)+1):
            posts = self.db_posts.search(Query()['id'] == int(post_id))
            comments = self.db_comments.search(Query()['postId'] == int(post_id))
        else:
            return 'failure', 'post_not_found'
        result = self.collaborate(posts, comments)
        return 'success', result

