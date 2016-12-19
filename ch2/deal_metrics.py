# a deal tracking system
#  - mark a deal as sent to a user
#  - check whether a user received a group of deals
#  - gather metrics from the sent deals

class RedisClient:

    """
    a simple wrapper for redis function
    """

    def __init__(self, *args, **kwargs):
        self._client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, *args, **kwargs)

    def markDealAsSent(self, dealId, userId):
        # add user to deal set
        self._client.sadd(dealId, userId)

