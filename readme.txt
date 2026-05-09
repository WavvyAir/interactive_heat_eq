############################################################
#       INTERACTIVE 2D HEAT EQUATION SOLVER                #
############################################################

OVERVIEW

This programm provides a heat equation visualization with interactive GUI Boundary drawing,
simulation using finite difference method and visualization in plotly.


REQUIREMENTS
- Python 3.x
- NumPy (math engine)
- Matplotlib (interaction window)
- Plotly (3D visualization)


USAGE
1.  Start using by running heat_eq.py
2.  A Matplotlib window will popup. The Boundary conditions will be set here.

3.  Clicking on the outer edges to draw the currently selected boundary condition. 
    Pressing "d" will switch to a "Dirichlet" boundary condition.
    Use "+" or "-" to change Dirichlet temperature value. Press "i" to switch to a "Neumann" boundary condition (insulated walls).
    Press "r" to reset drawing board.
    Press "enter" to start visualization.

4.  A brower window with plotly should popup. The visualization can be started using the "Play" Button. 
    "Stop" will pause the simulation and allow free camera movement.


Instructions and feedback about currently selected boundary condition and value are also provided via terminal outputs.


TROUBLESHOOTING
-In case of long computation time or errors try reducing the plate_length and max_iter_time.
-Sometimes clicks won't register if you are too fast. Click registration also seems to be slightly left of the mouse cursor.



CREDITS

By WavvyAir

