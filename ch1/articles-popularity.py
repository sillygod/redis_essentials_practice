import redis


class RedisClient:

    """
    a simple wrapper for redis function
    """

    def __init__(self, *args, **kwargs):
        self._client = redis.StrictRedis(host='localhost', port=6379, *args, **kwargs)

    def upVote(self, id):
        key = "article:{}:votes".format(id)
        self._client.incr(key)

    def downVote(self, id):
        key = "article:{}:votes".format(id)
        self._client.decr(key)

    def showResults(self, id):
        headlineKey = "article:" + str(id) + ":headline"
        voteKey = "article:" + str(id) + ":votes"

        res = self._client.mget([headlineKey, voteKey])
        print("The article {} has {} votes".format(res[0], res[1]))

    def saveLink(self, id, author, title, link):
        self._client.hmset("link:" + str(id), {'author': author, 'title': title, 'link': link, 'score': 0})

    def upVoteLink(self, id):
        self._client.hincrby("link:"+str(id), 'score', 1)

    def downVoteLink(self, id):
        self._client.hincrby('link:'+str(id), 'score', -1)

    def showDetails(self, id):
        res = self._client.hgetall('link:'+str(id))
        print('title: {}'.format(res['title']))
        print('Author: {}'.format(res['author']))
        print('Link: {}'.format(res['link']))
        print('Score: {}'.format(res['score']))
        print('--------------------------')

if __name__ == "__main__":
    client = RedisClient(decode_responses=True) # note python3 get string from redis will be byte object so, give decode_response=True,
    # make it auto decode for us

    client.upVote(12345)
    client.upVote(12345)
    client.upVote(12345)
    client.upVote(10001)
    client.upVote(10001)
    client.downVote(10001)
    client.upVote(60056)

    client.saveLink(123, "lovestory", "travel to janpan", "https://www.cc.com")
    client.upVoteLink(123)

    client.showResults(12345)
    client.showResults(10001)
    client.showResults(60056)

    client.showDetails(123)
