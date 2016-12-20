# a deal tracking system
#  - mark a deal as sent to a user
#  - check whether a user received a group of deals
#  - gather metrics from the sent deals
import redis
import logging


class RedisClient:

    """
    a simple wrapper for redis function
    """

    def __init__(self, *args, **kwargs):
        self._client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, *args, **kwargs)

    def markDealAsSent(self, dealId, userId):
        # add user to deal set
        self._client.sadd(dealId, userId)

    def sendDealIfNotSent(self, dealId, userId):
        ismember = self._client.sismember(dealId, userId)
        if ismember:
            logging.info('Deal {} was already sent to user {}'.format(dealId, userId))
        else:
            logging.info('Sending {} to user {}'.format(dealId, userId))
            self.markDealAsSent(dealId, userId)

    def showUsersThatReceivedAllDeals(self, dealIds):
        res = self._client.sinter(dealIds)
        logging.info('{} received all of dealIds: {}'.format([x for x in res], dealIds))

    def showUsersThatReceiveAtLeastOneOfTheDeals(self, dealIds):
        pass


