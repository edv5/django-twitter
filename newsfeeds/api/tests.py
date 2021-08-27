from rest_framework.test import APIClient
from testing.testcases import TestCases
from friendships.models import Friendship
from newsfeeds.models import NewsFeed

NEWSFEEDS_URL = '/api/newsfeeds/'
POST_TWEETS_URL = '/api/tweets/'
FOLLOW_URL = '/api/friendships/{}/follow/'


class NewsFeedApiTests(TestCases):
    def setUp(self):
        self.linghu = self.create_user('linghu')
        self.linghu_client = APIClient()
        self.linghu_client.force_authenticate(self.linghu)

        self.dongxie = self.create_user('dongxie')
        self.dongxie_client = APIClient()
        self.dongxie_client.force_authenticate(self.dongxie)

        # create followings and followers for dongxie
        for i in range(2):
            follower = self.create_user('dongxie_follower{}'.format(i))
            Friendship.objects.create(from_user=follower, to_user=self.dongxie)
        for i in range(3):
            following = self.create_user('dongxie_following{}'.format(i))
            Friendship.objects.create(from_user=self.dongxie, to_user=following)

    def test_list(self):
        # 需要登录
        response = self.anonymous_client.post(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 403)
        # 不能post
        response = self.dongxie_client.post(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 405)
        # 一开始没东西
        response = self.linghu_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['newsfeed'], 0)
        # 自己发东西可以看到
        self.linghu_client.post(POST_TWEETS_URL, {'content': 'hello world'})
        response = self.linghu_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['newsfeed'], 1)
        # 关注之后可以看到别人发的
        self.linghu_client.post(FOLLOW_URL.format(self.dongxie.id))
        self.dongxie_client.post(POST_TWEETS_URL, {'content': 'hello linghu'})
        posted_tweet_id = response.data['id']
        response = self.linghu_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.data['newsfeed'], 2)
        self.assertEqual(response.data['newsfeed'][0]['tweet']['id'], posted_tweet_id)