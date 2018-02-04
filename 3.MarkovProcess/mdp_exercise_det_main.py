# Import your implementations
from gridworld_det_cls import NORTH, SOUTH, WEST, EAST, Gridworld_det
from value_iteration_det import value_iteration, extract_deterministic_policy

import svgwrite
import numpy

def render_policy (env, ofile, Q = None):
    """
    Function to render a given gridworld object. If a Q-function
    is provided, e.g. calculated using the 'extract_policy_greedily'
    function, than also the optimal policy is rendered.

    :param env: Gridworld_det class object

    :param ofile: string, path to the output file.

    :param Q: array-like, shape = (nSp, nA) (default = None)
              If Q is None, than only the world is rendered,
              but not the optimal policy.
    """
    dwg = svgwrite.Drawing (ofile, profile = 'full')

    ssize = 101
    strokec = "black"
    strokew = 2.5

    # Cell colors
    termic = "gray"
    fieldc = "white"
    obstac = "black"
    dustc = "red"

    # First build up the world
    for state in range (env.nSp):
        x, y = env._state2coord (state)
        x, y = int(x), int(y)

        if env.world[y, x] == "T":
            # Terminal state
            cellc = termic
            textc = "black"
        elif env.world[y, x] == ".":
            # Normal state
            cellc = fieldc
            textc = "black"
        elif env.world[y, x] == "o":
            # Obstacle state (actually the robot will never be here)
            cellc = obstac
            textc = "white"
        elif env.world[y, x] == "x":
            cellc = dustc
            textc = "black"
        else:
            raise ValueError ("Unsupported world field: %s." % env.world[y, x])

        dwg.add (dwg.rect (insert = (x * ssize, y * ssize),
                           size = (ssize, ssize),
                           stroke = strokec,
                           stroke_width = strokew,
                           fill = cellc))

        if not Q is None:
            # If an action-value function Q is given we output the optimal policy
            # - using a greedy approach - based on Q.
            if env.world[y, x] in ["T", "o"]:
                continue

            hssize = numpy.ceil (ssize / 2.0)
            cx = x * ssize + hssize
            cy = y * ssize + hssize

            # As it can be that at a given state, two actions have the same value, i.e.
            # that they are both equally good, we display all actions having the same
            # "goodness".
            for best_action in numpy.where (Q[state] == numpy.max (Q[state]))[0]:
                if best_action == NORTH:
                    dwg.add (dwg.polyline ([(cx, cy), (cx, cy - 45)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx + 10, cy - 35), (cx, cy - 45)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx - 10, cy - 35), (cx, cy - 45)], stroke = strokec, stroke_width = strokew, fill = "none"))

                elif best_action == SOUTH:
                    dwg.add (dwg.polyline ([(cx, cy), (cx, cy + 45)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx + 10, cy + 35), (cx, cy + 45)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx - 10, cy + 35), (cx, cy + 45)], stroke = strokec, stroke_width = strokew, fill = "none"))

                elif best_action == WEST:
                    dwg.add (dwg.polyline ([(cx - 45, cy), (cx, cy)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx - 35, cy + 10), (cx - 45, cy)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx - 35, cy - 10), (cx - 45, cy)], stroke = strokec, stroke_width = strokew, fill = "none"))

                elif best_action == EAST:
                    dwg.add (dwg.polyline ([(cx + 45, cy), (cx, cy)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx + 35, cy + 10), (cx + 45, cy)], stroke = strokec, stroke_width = strokew, fill = "none"))
                    dwg.add (dwg.polyline ([(cx + 35, cy - 10), (cx + 45, cy)], stroke = strokec, stroke_width = strokew, fill = "none"))
        else:
            # Output the index of each state.
            hssize = numpy.ceil (ssize / 2.0)
            cx = x * ssize + hssize
            cy = y * ssize + hssize

            dwg.add (dwg.text (str (state), insert = (cx, cy), fill = textc))

    dwg.save()

if __name__ == '__main__':
    discount_factor = 0.9

    # Output directory of the rendered worlds. The rendered outputs SVG-files.
    # Those you can view for example using a browser like Firefox.
    sdir = "./"

    for type in ["4x4_world", "obstacles"]:
        gworld = Gridworld_det._create_example_world (type)
        env = Gridworld_det (gworld)

        render_policy (env, ofile = sdir + type + "_world_det.svg")

        V = value_iteration (env, discount_factor = discount_factor)
        policy, Q = extract_deterministic_policy (env, V, discount_factor = discount_factor)

        print ("World: ")
        print (numpy.array (env.world).reshape (env.shape))
        print ("Optimal deterministic policy: ")
        print (policy.reshape (env.shape))
        print ("Actions: NORTH=0, SOUTH=1, WEST=2, EAST=3")

        render_policy (env, ofile = sdir + type + "_world_optimal_policy_det.svg", Q = Q)