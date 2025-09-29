import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation


class BoxHeatSolver:
    def __init__(self, plate_length, N, iter_time, alpha, init_T, boundary_T, boundary_condition = 'dirichlet'):
        self.plate_length = plate_length
        self.N = N
        self.iter_time = iter_time
        self.alpha = alpha

        self.delta_x = self.plate_length/(N-1)

        self.delta_t = 0.9*(self.delta_x ** 2)/(4 * alpha)

        self.gamma = self.alpha * self.delta_t / self.delta_x**2

        self.grid = np.zeros((self.N, self.N))

        self.init_T = init_T
        
        #* list [bool, bool, bool, bool] for top, bottom, left and/or right wall activation
        self.boundary_T: list[bool] = boundary_T

        self.apply_boundary_T()
        
        #* "dirichlet" or "neumann"
        self.boundary_condition: str = boundary_condition


    def apply_boundary_T(self):
        #* top
        if self.boundary_T[0]:
            self.grid[-1,:] = self.init_T
        #* bottom
        if self.boundary_T[1]:
            self.grid[0,:] = self.init_T
        #* left
        if self.boundary_T[2]:
            self.grid[:,0] = self.init_T
        #* right
        if self.boundary_T[3]:
            self.grid[:,-1] = self.init_T


    def update_grid(self):
        #* update interior points
        for i in range(1, self.N-1):
            for j in range(1, self.N-1):
                self.grid[i,j] += self.gamma * (self.grid[i+1,j] + self.grid[i-1,j] + self.grid[i,j+1] + self.grid[i,j-1] - 4*self.grid[i,j])
        
        #* update boundary points
        match self.boundary_condition:
            case "dirichlet":
                pass
            case "neumann":
                if not self.boundary_T[0]:
                    self.grid[-1,:] = self.grid[-2,:]
                if not self.boundary_T[1]:
                    self.grid[0,:] = self.grid[1,:]
                if not self.boundary_T[2]:
                    self.grid[:,0] = self.grid[:,1]
                if not self.boundary_T[3]:
                    self.grid[:,-1] = self.grid[:,-2]
            case _:
                raise ValueError("Specify correct boundary_condition")


    def generate_animation(self):
        def animate(i):
            plt.clf()
            plt.title(f"Temperature at t = {i*self.delta_t:.3f}s")
            plt.xlabel("x")
            plt.ylabel("y")
            
            plt.pcolormesh(self.grid, cmap=plt.cm.jet, vmin=0, vmax=100)
            plt.colorbar()
            self.update_grid()
            
            return plt
        
        anim = FuncAnimation(plt.figure(), animate, frames=self.iter_time, interval=1, blit=False, repeat=False)
        anim.save('heat_transfer.gif')


solver = BoxHeatSolver(plate_length=0.5, N=101, iter_time=200, alpha=149E-6, init_T=100, boundary_T=[True, False, False, False])
solver.generate_animation()