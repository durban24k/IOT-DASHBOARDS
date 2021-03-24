"""
     Wikipedia Datastream DURBAN24K
"""
import sys
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

class SensorSubscriberCallBack(SubscribeCallback):
     """SensorSubscriberCallback receives messages from PubNub"""
     def __init__(self,limit=1000):
          """Create instances variables for tracking number of tweets"""
          self.order_count=0
          self.max_orders=limit #10000 by default
          super().__init__() #call to the superclass' init

     def status(self,pubnub,status):
          """checks for subscription"""
          if status.category == PNStatusCategory.PNConnectedCategory:
               print('Service Subscribed')
          elif status.category == PNStatusCategory.PNAcknowledgmentCategory:
               print('Service Unsubscribed')

     def message(self,pubnub,message):
          event=message.message['event']
          item=message.message['item']
          user=message.message['user']
          link=message.message['link']
          print(event)
          print(item)
          print(user)
          print(link)
          print('***************************************************************************')

          # Log the data into an log file
          f=open('log.txt','a')
          f.write(event+'\n'+item+'\n'+user+'\n'+link+'\n***************************************************************************\n')
          f.close()

          if self.order_count == self.max_orders:
               pubnub.unsubscribe_all()


if __name__ == '__main__':
     # setup thepubnub 
     pconfig=PNConfiguration()
     pconfig.subscribe_key='sub-c-b0d14910-0601-11e4-b703-02ee2ddab7fe'

     pubnub=PubNub(pconfig)
     pubnub.add_listener(SensorSubscriberCallBack(limit=int(sys.argv[1] if len(sys.argv)>1 else 1000)))
     pubnub.subscribe().channels('pubnub-wikipedia').execute()

"""
     Wikipedia Datastream DURBAN24K
"""