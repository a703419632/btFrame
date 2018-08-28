# -*- coding: utf-8 -*-
from EventNotifier import DataEvent
import inspect

class EventBase(object):

    def __init__(self):
        self.init_data_listeners()

    def init_data_listeners(self):
        """为所有标有@data_listener的成员函数注册事件监听器"""
        for listener_name, listener in inspect.getmembers(self, lambda f: hasattr(f, 'events')):
            for event in listener.events:
                event += listener
                print(event)

    def destroy(self):
        print('%s.destroy' % self.__class__.__name__)
        DataEvent.clear()
