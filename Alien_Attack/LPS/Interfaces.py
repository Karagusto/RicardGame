from abc import ABC, abstractmethod

class background(ABC):
    @abstractmethod
    def __init__(self, screenwidth, screenheight):
        pass

    @abstractmethod
    def drawBackground(self):
        pass

class player(ABC):
    @abstractmethod
    def __init__(self, x, y, width, height):
        pass

    @abstractmethod
    def draw(self, win):
        pass

    @abstractmethod
    def hit(self):
        pass

    def score(self):
        pass


class projectile(ABC):
    @abstractmethod
    def __init__(self, x, y, radius, color):
        pass

    @abstractmethod
    def draw(self, win):
        pass


class enemy(ABC):
    @abstractmethod
    def __init__(self, x, y, width, height, end):
        pass

    @abstractmethod
    def draw(self, win):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def hit(self):
        pass


class collision(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def isCollidingEnemy(self):
        pass

    @abstractmethod
    def  isCollidingBullet(self):
        pass


# Classe que implementa a variabilidade dos meus jogos
class regras(ABC):
    @abstractmethod
    def __init__(self):
        pass