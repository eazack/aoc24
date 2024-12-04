import arguably
from solvers.solver import solver_registry

@arguably.command
def solve(day: int):
    """
    Load the correct solver class and print the solution to the main and bonus puzzles.

    Args:
        day: Integer of which day's puzzle to solve
    """
    solver = solver_registry[day]

    if solver.test():
        solution = solver.solve()
        bonus = solver.solve_bonus()

        print(solution, bonus)

if __name__ == "__main__":
    arguably.run()
