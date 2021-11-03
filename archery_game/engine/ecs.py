import uuid
from typing import List
from dataclasses import dataclass as component
from abc import ABC, abstractmethod

@component
class Component:
    pass

class Entity:
    # These are shared among all entity classes
    entity_index = {}
    component_index = {}

    def __init__(self, components : List[Component] = []):
        self.id = uuid.uuid4().int
        self.entity_index[self.id] = self

        self.components = []
        for c in components:
            self.attach(c)

    def attach(self, component):
        self.components.append(component)

        if hasattr(component, 'namespace'):
            self.__dict__[component.namespace] = component

        name = component.__class__.__name__
        if name not in self.component_index:
            self.component_index[name] = []

        self.component_index[name].append(self)

    def dettach(self, component):
        if self.has(component):
            self.component_index[component.__name__].remove(self)
            del self.__dict__[component.namespace]

            idx = -1
            for i, c in enumerate(self.components):
                if isinstance(c, component):
                    idx = i

            self.components.pop(idx)

    def getC(self, component: Component) -> Component:
        for c in self.components:
            if isinstance(c, component):
                return c
        return None

    @classmethod
    def filter(cls, component: Component) -> List['Entity']:
        entities = cls.component_index.get(component.__name__)
        return entities if entities is not None else []

    @classmethod
    def get(cls, id) -> 'Entity':
        return cls.entity_index.get(id, None)

    def has(self, component: Component) -> bool:
        for c in self.components:
            if isinstance(c, component):
                return True
        return False

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

class System(ABC):

    def __init__(self):
        self.requires = []

    def subscribe(self, component: Component):
        self.requires.append(component)

    def get(self) -> List['Entity']:
        res = []
        
        # need to return components that have all of these 
        for component in self.requires:
            res += [ set(Entity.filter(component)) ]

        return list(set.intersection(*res))

    @abstractmethod
    def update(self, **kwargs):
        pass

class Observer(ABC):
    watchers = []

    def __init__(self):
        self.watchers.append(self)
        self.callbacks = {}

    def watch(self, event_name, callback):
        if not event_name in self.callbacks:
            self.callbacks[event_name] = []

        self.callbacks[event_name] += [ callback ]

class Event(ABC):
    def __init__(self, name):
        self.name = name

    def fire(self, **kwargs):
        for observer in Observer.watchers:
            if self.name in observer.callbacks:
                for c in observer.callbacks[self.name]:
                    c(**kwargs)