from heat_solver.solver import BoxHeatSolver



def test_boundary_conditions():
    solver = BoxHeatSolver(plate_length=10, max_iter_time=100, alpha=1, delta_x=1, init_t=100, boundary_T=[True, True, False, False], boundary_condition="dirichlet")
    assert solver.grid[0,0] == 100
    assert solver.grid[0,-1] == 100
    assert solver.grid[-1,0] == 100
    assert solver.grid[-1,-1] == 100
    assert solver.grid[1,1] == 0
    assert solver.grid[1,0] == 0