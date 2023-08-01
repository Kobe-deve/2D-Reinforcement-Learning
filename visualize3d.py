# used for displaying the 3D model of the world when toggled
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class CubePlotter:
    def __init__(self, center_coords, edge_length=1, colors={}, alphas={}, world=None):
        self.center = center_coords
        self.edge_length = edge_length
        self.colors = colors
        self.alphas = alphas
        self.world = world
        self.fig = plt.figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect([2, 2, 3])
        self.ax.set_xlim(0, 6)
        self.ax.set_ylim(0, 6)
        self.ax.set_zlim(0, 12)
        self.ax.set_axis_off()
        self.gap = 3
        self.coords = [(z, x, y) for z in range(3) for x in range(world.rows) for y in range(world.cols)]
        for coord in self.coords:
            color = self.get_color(coord)
            alpha = self.get_alpha(coord)
            poly = Poly3DCollection(self.cube(coord), alpha=alpha, linewidths=1, edgecolors='black')
            poly.set_facecolor(color)
            self.ax.add_collection3d(poly)
        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

    def cube(self, center):
        half_length = self.edge_length / 2
        z, x, y = center
        z = z * (1 + self.gap)
        return [
        [(x - half_length, y - half_length, z - half_length), (x - half_length, y + half_length, z - half_length), (x + half_length, y + half_length, z - half_length), (x + half_length, y - half_length, z - half_length)],
        [(x - half_length, y - half_length, z + half_length), (x - half_length, y + half_length, z + half_length), (x + half_length, y + half_length, z + half_length), (x + half_length, y - half_length, z + half_length)],
        [(x - half_length, y - half_length, z - half_length), (x - half_length, y + half_length, z - half_length), (x - half_length, y + half_length, z + half_length), (x - half_length, y - half_length, z + half_length)],
        [(x + half_length, y - half_length, z - half_length), (x + half_length, y + half_length, z - half_length), (x + half_length, y + half_length, z + half_length), (x + half_length, y - half_length, z + half_length)],
        [(x - half_length, y - half_length, z - half_length), (x + half_length, y - half_length, z - half_length), (x + half_length, y - half_length, z + half_length), (x - half_length, y - half_length, z + half_length)],
        [(x - half_length, y + half_length, z - half_length), (x + half_length, y + half_length, z - half_length), (x + half_length, y + half_length, z + half_length), (x - half_length, y + half_length, z + half_length)]

        ]
    
    def get_color(self, coord):
        if self.world is not None:
            z, x, y = coord
            state = self.world.map[z][x][y]

            if state.pickup:
                return 'blue'
            elif state.dropoff:
                return 'green'
            elif state.risk:
                return 'red'
            
        return self.colors.get(coord, 'white')

    def get_alpha(self, coord):
        if self.world is not None:
            z, x, y = coord
            state = self.world.map[z][x][y]
            if state.pickup:
                if state.blocks > 0:
                 return 0.7
            if state.dropoff:
                return 1
            if state.risk:
                return 1
        return self.alphas.get(coord, 0)

    def show(self):
        plt.show()