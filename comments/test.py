from testing.testcases import TestCases


class CommentModelTests(TestCases):

    def test_comment(self):
        user = self.create_user('linghu')
        tweet = self.create_tweet(user)
        comment = self.create_comment(user, tweet)
        self.assertNotEqual(comment.__str__(), None)