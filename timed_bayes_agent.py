import agent
import world
import math
import time

class SavedArrangement:
    
    def __init__(self, arrangement, hunt):
        self.arrangement = arrangement
        self.hunt = hunt


class SavedPaths:

    def __init__(self, path, agent):
        self.path = path
        self.cost = 0
        hunt = []
        for h in range(len(agent.hunt)):
            if not agent.found[h]:
                hunt.append(agent.hunt[h])
        saved_arrs = []
        for arr in range(0, len(agent.arrangement_space.arrangements)):
            if agent.arrangement_space.valid_arrangements[arr]:
                saved_arrs.append(SavedArrangement(agent.arrangement_space.arrangements[arr], hunt))
        self.saved_arrangements = saved_arrs


class TimedBayesianAgent(agent.Agent):
    """The Timed Bayesian agent evaluates solutions in a breadth-first search
    given a time delimiter using Bayesian search theory. It visits the first
    node in the path with the lowest expected cost given the current arrangement
    space and saved path costs.
    """
    # track these as you go, can choose one after time is up
    global best_path
    global best_path_cost
    global paths
    global saved_paths

    def init_saved_paths(self):
        global paths
        global saved_paths
        saved_paths = []
        for path in paths:
            saved_paths.append(SavedPaths(path, self))


    def expected_path_cost(self, step):
        global best_path 
        global best_path_cost
        global saved_paths
        global paths
        best_path = None
        best_path_cost = math.inf
        for p in range(0, len(paths)):
            step_cost = 0
            # check if first path up to steps is the same, if so copy val and done TODO
            # for each valid arrangement
            valid_index = 0
            for i in range(0, len(self.arrangement_space.arrangements)):
                if not self.arrangement_space.valid_arrangements[i]:
                    continue
                # restore old hunt from last step
                arrangement = saved_paths[p].saved_arrangements[valid_index].arrangement
                last_hunt = saved_paths[p].saved_arrangements[valid_index].hunt

                # If hunt complete, don't calculate cost
                if len(last_hunt) == 0:
                    valid_index += 1
                    continue
                # Move along path
                n_to, n_from = paths[p][step], paths[p][step-1]
                travel_distance = 0
                travel_distance += \
                    self.world.graph.shortest_path(n_to, n_from).cost
                # Collect objects
                new_hunt = last_hunt.copy()
                for obj in last_hunt:
                    if arrangement.contains(obj, n_to):
                        new_hunt.remove(obj)

                saved_paths[p].saved_arrangements[valid_index].hunt = new_hunt 
                # Factor in expected contribution
                saved_paths[p].cost += travel_distance * arrangement.prob()
                print(">>> travel distance = ", travel_distance)
                print("cost of arrangement ", arrangement, " is ", travel_distance * arrangement.prob())
                valid_index += 1 

            # update cost if better
            if saved_paths[p].cost < best_path_cost:
                best_path_cost = saved_paths[p].cost
                best_path = saved_paths[p].path


            print("\n\t~~~~~cost of whole step of path ", saved_paths[p].path, " for step ",step," is ", saved_paths[p].cost)


    def run(self):
        global paths
        # Collect objects at current location and update the occurrence space
        super().run()

        if self.done():
            return

        paths = self.world.graph.permute_paths(self.loc)
        self.init_saved_paths()

        # Determine cost of path in breadth-first search for 5 seconds
        end_time = time.time() + 5  
        for i in range(1, len(paths[0])): 
            if (time.time() < end_time):
                self.expected_path_cost(i)
            else:
                break
        assert best_path is not None

        print("\nbest path for this step is ", best_path, "\n*******************************\n")
        # Convert to a traversable path of adjacent nodes
        path = self.world.graph.stitch_path(best_path)

        # Visit first loc in selected path
        self.go(path[1])
