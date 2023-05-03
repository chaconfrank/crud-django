import abc
import attr

from typing import Optional, List


class ValueObject(abc.ABC):
    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError


class EntityIdentity(ValueObject, abc.ABC):
    pass


class Entity(abc.ABC):
    def __init__(self, *args, entity_id: EntityIdentity = None, **kwargs):
        self.entity_id = entity_id
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if type(other) == self.__class__:
            return self.entity_id == other.entity_id
        return False

    def __hash__(self):
        return hash(self.entity_id)


@attr.s(eq=False, hash=False)
class RootEntity(Entity):
    version_id = attr.ib(type=int, default=0, eq=False, repr=False, kw_only=True)


class AbstractRepository(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: EntityIdentity) -> RootEntity:
        """
        Function used to get root entity by entity identity.
        :return: The root entity
        """
        pass

    @classmethod
    @abc.abstractmethod
    def search(cls, entity_ids: Optional[List[EntityIdentity]] = None, **kwargs) -> List[RootEntity]:
        """
        Function used to search multiple root entity (by entity identity for ex).
        :return: The list of root entities found
        """
        pass

    @classmethod
    @abc.abstractmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs) -> None:
        """
        Function used to delete a root entity via it's entity identity.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def save(cls, entity: RootEntity) -> None:
        """
        Function used to persist existing domain RootEntity (aggregate) into the database.
        :param entity: Any domain root entity.
        """
        pass
