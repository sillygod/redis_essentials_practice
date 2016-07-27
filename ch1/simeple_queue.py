import redis


class RedisQueue:

    """first in first out simple queue
    """

    def __init__(self, name):
        self._client = redis.StrictRedis(host='localhost', port=6369)
        self._qname = name
        self._qkey = "queues:" + self._qname
        self.timeout = 0

    @property
    def size(self):
        length = self._client.llen(self._qkey)
        return length

    def push(self, data):
        self._client.lpush(self._qkey, data)

    def pop(self):
        ele = self._client.brpop(self._qkey, self.timeout)  # use brpop instead of rpop, we can have no worry about empty lists
        return ele


if __name__ == '__main__':
    # a producer worker
    logQueue = RedisQueue('logs')

    log_length = 5
    for i in range(log_length):
        logQueue.push("hello world #{}".format(i))

    print("Created {} logs".format(log_length))

    # a consumer worker

    for _ in range(logQueue.size):
        ele = logQueue.pop()
        print('[consumer] Got log: {}'.format(ele))

        print('{} logs left'.format(logQueue.size))

