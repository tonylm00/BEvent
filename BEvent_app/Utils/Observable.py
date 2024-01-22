from abc import ABC, abstractmethod


class Observable:
    def __init__(self):
        self.observers = []

    def __init__(self, observers):
        self.observers = observers

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
