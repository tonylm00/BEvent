from abc import ABC, abstractmethod


class Observer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def update(self, observable):
        pass
