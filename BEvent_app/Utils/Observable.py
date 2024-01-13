from abc import ABC, abstractmethod

class Observable:
    def init(self):
        self.observers = []


    def register_observer(self, observer):
        self.observers.append(observer)


    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
