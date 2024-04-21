from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def close(self) -> None:
        pass
