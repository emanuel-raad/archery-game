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
        self.id = str(uuid.uuid4())
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

    def getC(self, component: Component) -> 'Component':
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