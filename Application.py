import tkinter as tk

class PathfindingApp:
    def __init__(self, master):
        self.master = master
        master.title("Pathfinding Algorithms")

        # Create start and reset buttons
        self.start_button = tk.Button(master, text='Start', command=self.start)
        self.start_button.pack(side='top', pady=10)

        self.reset_button = tk.Button(master, text='Reset', command=self.reset)
        self.reset_button.pack(side='top', pady=10)

        # Create left-hand menu with table for algorithm times
        self.menu_frame = tk.Frame(master, width=200, bg='lightgray')
        self.menu_frame.pack(side='left', fill='y')

        self.table_label = tk.Label(self.menu_frame, text='Algorithm Times', font=('Helvetica', 16))
        self.table_label.pack(pady=10)

        self.table = tk.Frame(self.menu_frame, width=200, height=200)
        self.table.pack()

        # Example table data
        algorithms = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3']
        times = [10.2, 12.3, 9.1]

        for i, algorithm in enumerate(algorithms):
            algorithm_label = tk.Label(self.table, text=algorithm, font=('Helvetica', 12))
            algorithm_label.grid(row=i, column=0, padx=10, pady=5)

            time_label = tk.Label(self.table, text=str(times[i]) + 's', font=('Helvetica', 12))
            time_label.grid(row=i, column=1, padx=10, pady=5)

        # Create grids to visualize algorithm progress
        self.grid_frame = tk.Frame(master, width=500, height=500)
        self.grid_frame.pack(side='right')

        self.grid_size = 20
        self.grid1 = self.create_grid()
        self.grid2 = self.create_grid()
        self.grid3 = self.create_grid()
        self.grid4 = self.create_grid()

        self.grids = [[self.grid1, self.grid2], [self.grid3, self.grid4]]

    def create_grid(self):
        grid = tk.Frame(self.grid_frame, width=240, height=240, bg='white')
        grid.pack(side='left', padx=5, pady=5)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                square = tk.Canvas(grid, width=10, height=10, bg='white', highlightthickness=1)
                square.grid(row=i, column=j)

        return grid

    def start(self):
        # Start algorithm progress visualization
        pass

    def reset(self):
        # Reset algorithm progress visualization
        pass

root = tk.Tk()
app = PathfindingApp(root)
root.mainloop()
