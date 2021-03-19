from resurse.constants import *


class Movement:

    def __init__(self):
        self.x = round(np.random.rand() * MAP_SIZE, 2)
        self.y = round(np.random.rand() * MAP_SIZE, 2)

        self.momentum = np.asarray([0, 0],dtype=float)
        self.max_speed = np.random.randint(MIN_SPEED, MAX_SPEED)

    def update_momentum(self, target=None):
        if target is None:
            self.momentum = self.momentum + np.random.rand(2) - 0.5
        else:
            target[0] = target[0] - self.x
            target[1] = target[1] - self.y

            self.momentum += target

        np.clip(self.momentum, - self.max_speed, self.max_speed, out=self.momentum)

    def move(self, target=None):
        self.update_momentum(target)

        self.x += self.momentum[0]
        self.y += self.momentum[1]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if 0 <= value <= MAP_SIZE:
            self._x = value
        else:
            self.momentum[0] = 0

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if 0 <= value <= MAP_SIZE:
            self._y = value
        else:
            self.momentum[1] = 0

    def __repr__(self):
        return f"Movement({self.x}\t{self.y}\t{self.momentum})"

    pass
