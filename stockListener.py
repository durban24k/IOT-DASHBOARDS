#stockListener.py 
"""
     Visualizing a PubNub livestream
"""
from matplotlib import animation
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

companies=['Apple','Bespin Gas','Elerium','Google','Linen Cloth']

#DATAFRAME
companies_df=pd.DataFrame({'company':companies,'price':[0,0,0,0,0]})

class SensorSubscriberCallBack(SubscribeCallback):
     """SensorSubscriberCallback receives messages from PubNub"""
     def __init__(self,df,limit=1000):
          """"Create instances variables for tracking number of tweets"""
          self.df = df #dataframe for the last stock
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
          symbol=message.message['symbol']
          bid_price=message.message['bid_price']
          print(symbol,bid_price)
          self.df.at[companies.index(symbol),'price']=bid_price
          self.order_count +=1

          if self.order_count == self.max_orders:
               pubnub.unsubscribe_all()

def update(frame_number):
     """Configures Bar plot contents for each animation"""
     plt.cla()
     axes=sns.barplot(data=companies_df,x='company',y='price',palette='cool')
     axes.set(xlabel='Company',ylabel='Price')
     plt.tight_layout()

if __name__ == '__main__':
     sns.set_style('whitegrid')
     figure=plt.figure('Stock Prices')

     #configure and start the animation

     stock_animation=animation.FuncAnimation(figure,update,repeat=False,interval=33)
     plt.show(block=False) # display the window

     #set up thepubnub market order sensor stream key
     config=PNConfiguration()
     config.subscribe_key="sub-c-b134f796-87ee-11eb-88a7-4a59fc122af9"

     #create PubNub client and register a subscriberCallback
     pubnub=PubNub(config)
     pubnub.add_listener(SensorSubscriberCallBack(df=companies_df,limit=int(sys.argv[1] if len(sys.argv)>1 else 1000)))

     pubnub.subscribe().channels('pubnub-market-orders').execute()

     plt.show()