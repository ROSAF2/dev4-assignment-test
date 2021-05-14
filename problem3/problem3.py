from collections import deque
from random import randrange
from abc import ABC,abstractmethod

class Queue:
    def __init__(self):
        self._queue = deque([])

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        return self._queue.popleft()

    def peek(self):
        return self._queue[0]
    
    def empty(self):
        return not self._queue
    
    def length(self):
        return len(self._queue)

class Shopper:
    def __init__(self):
        self._checkout_time = randrange(60,500)

    @property
    def checkout_time(self):
        return self._checkout_time

    @checkout_time.setter
    def checkout_time(self,checkout_time):
        self._checkout_time = checkout_time

class SuperMarket:
    def __init__(self,num_queues,num_eQueues):
        self._queues = self.appendQueues(num_queues)
        self._eQueues = self.appendQueues(num_eQueues)
    
    def appendQueues(self,num_queues):
        queues = list()
        for i in range(num_queues): 
            queues.append(Queue())
        return queues

    @property
    def queues(self):
        return self._queues

    @queues.setter
    def queues(self,queues):
        self._queues = queues

    @property
    def eQueues(self):
        return self._eQueues

    @eQueues.setter
    def eQueues(self,eQueues):
        self._eQueues = eQueues

class IVersion(ABC):
    @abstractmethod
    def enqueueShopper(self):
        pass

class Version1(IVersion):
    @staticmethod
    def enqueueShopper(SM, shopper):
        SM.queues[randrange(len(SM.queues))].enqueue(shopper) # Enqueue a shopper to a random queue
        

class Version2(IVersion):
    @staticmethod
    def enqueueShopper(SM, shopper):
        shortestQueueIndex = getShortestQueueIndex(SM.queues) # Get shortest queue index
        SM.queues[shortestQueueIndex].enqueue(shopper) # Enqueue a shopper to a shortest queue

           
class Version3(IVersion):
    @staticmethod
    def enqueueShopper(SM, shopper):
        if shopper.checkout_time <= 90: # Express queue
            SM.eQueues[randrange(len(SM.eQueues))].enqueue(shopper) # Pick random express queue and enqueue shopper
        else: # Normal queue
            SM.queues[randrange(len(SM.queues))].enqueue(shopper) #  Pick random queue and enqueue shopper

class Version4(IVersion):
    @staticmethod
    def enqueueShopper(SM, shopper):
        if shopper.checkout_time <= 90: # Express queue
            shortestQueueIndex = getShortestQueueIndex(SM.eQueues) # Get shortest queue index
            SM.eQueues[shortestQueueIndex].enqueue(shopper) # Enqueue a shopper to a shortest queue
        else: # Normal queue
            shortestQueueIndex = getShortestQueueIndex(SM.queues) # Get shortest queue index
            SM.queues[shortestQueueIndex].enqueue(shopper) # Enqueue a shopper to a shortest queue
        

def getShortestQueueIndex(list_of_queues):
    shortestLength = min([ queue.length() for queue in list_of_queues ])
    for i in range(len(list_of_queues)):
        if list_of_queues[i].length() == shortestLength:
            return i

def checkAllQueuesEmpty(SM):
    return all([ queue.empty() for queue in SM.queues ]) and all([ queue.empty() for queue in SM.eQueues ])

def checkShoppersTime(list_of_queues):
    """ Decrements and removes shopper if checkout_time is 0 """
    for queue in list_of_queues:
        if not queue.empty():
            queue.peek().checkout_time -= 1
            if queue.peek().checkout_time == 0: # If a shopper's time reaches zero, remove that shopper from their queue
                queue.dequeue()

def runShopping(SM, new_shopper_rate, max_shopper_number, enqueueShopper):
    seconds = 0 # counts the seconds it takes to complete the run
    while True:
        # Adds a shopper every 10 seconds
        if seconds % new_shopper_rate == 0 and seconds < (new_shopper_rate)*(max_shopper_number): 
            enqueueShopper(SM,Shopper())
            
        # Decrement the checkout time for all shoppers at the front
        for i in [SM.queues, SM.eQueues]:
            checkShoppersTime(i)

        seconds += 1
        if checkAllQueuesEmpty(SM):
            return seconds

def main():
    
    SM_12 = SuperMarket(num_queues = 8, num_eQueues= 0)
    SM_34 = SuperMarket(num_queues = 6, num_eQueues= 2)

    print(f'It took {runShopping(SM_12, new_shopper_rate = 10, max_shopper_number = 1000, enqueueShopper = Version1.enqueueShopper)} times to complete the run.')
    print(f'It took {runShopping(SM_12, new_shopper_rate = 10, max_shopper_number = 1000, enqueueShopper = Version2.enqueueShopper)} times to complete the run.')
    print(f'It took {runShopping(SM_34, new_shopper_rate = 10, max_shopper_number = 1000, enqueueShopper = Version3.enqueueShopper)} times to complete the run.')
    print(f'It took {runShopping(SM_34, new_shopper_rate = 10, max_shopper_number = 1000, enqueueShopper = Version4.enqueueShopper)} times to complete the run.')
    

    
if __name__ == '__main__':
    main()
    