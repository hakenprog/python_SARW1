import numpy as np
import matplotlib.pyplot as plt
simulate = 200


class Grid:
    def __init__(self, size=9):
        self.matrix = []
        self.size = size
        self.edges = []
        self.generate_matrix()

    def generate_matrix(self):
        x_grid = np.floor(self.size / 2)+1
        for x in range(self.size):
            x_grid -= 1
            y_grid = np.floor(self.size / 2) + 1
            for y in range(self.size):
                y_grid -= 1
                self.matrix.append(np.array([x_grid, y_grid]))
        self.matrix = np.array(self.matrix)

    def is_coordinate_in_matrix(self, coordinate):
        for vector in self.matrix:
            if np.array_equal(vector, coordinate):
                return True
        return False


class Trajectory:
    def __init__(self):
        self.visited_coordinates = [np.array([0, 0])]

    def add_coordinate(self, coordinate):
        self.visited_coordinates.append(coordinate)

    def is_coordinate_visited(self, coordinate):
        for vector in self.visited_coordinates:
            if np.array_equal(vector, coordinate):
                return True
        return False


class Node:
    def __init__(self, grid = Grid()):
        self.position = np.array([0, 0])
        self.directions = {'up': np.array([0, 1]),
                           'down': np.array([0, -1]),
                           'right': np.array([1, 0]),
                           'left': np.array([-1, 0]),
                           }
        self.grid = grid
        self.trajectory = Trajectory()

    def move(self):
        temp = self.position + self.random_direction()
        while self.trajectory.is_coordinate_visited(temp) or not self.grid.is_coordinate_in_matrix(temp):
            temp = self.position + self.random_direction()
        self.position = temp
        self.trajectory.add_coordinate(self.position)

    def random_direction(self):
        direction_ = ['up', 'down', 'right', 'left']
        np.random.shuffle(direction_)
        return self.directions[direction_[0]]

    def can_continue(self):
        for keys in self.directions.keys():
            temp = self.position + self.directions[keys]
            if self.grid.is_coordinate_in_matrix(temp):
                if not self.trajectory.is_coordinate_visited(temp):
                    return True
        return False


def is_origin(node):
    return np.array_equal(node.position, node.initial_position)


def self_avoiding_random_walk(node, count):
    if node.can_continue():
        node.move()
        return self_avoiding_random_walk(node, count+1)
    return count

steps = 0
grid1 = Grid()
for i in range(simulate):
    steps += self_avoiding_random_walk(Node(grid=grid1), 0)
node1 = Node()
self_avoiding_random_walk(node1, 0)
trajectory = np.array(node1.trajectory.visited_coordinates)
print(trajectory)
plt.figure(1)
plt.title("Ejemplo de SARW")
plt.plot(trajectory[0][0], trajectory[0][1], 'x')
plt.plot(trajectory[len(trajectory)-1][0], trajectory[len(trajectory)-1][1], 'o')
plt.plot(trajectory[:, 0], trajectory[:, 1])
plt.grid()
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.show()
print("Promedio: ", steps/simulate)



