import redis


class RedisClient:

    """
    a simple wrapper for redis function
    """

    def __init__(self):
        self._client = redis.StrictRedis(host='localhost', port=6379)

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


if __name__ == "__main__":
    client = RedisClient()

    client.upVote(12345)
    client.upVote(12345)
    client.upVote(12345)
    client.upVote(10001)
    client.upVote(10001)
    client.downVote(10001)
    client.upVote(60056)

    client.showResults(12345)
    client.showResults(10001)
    client.showResults(60056)


