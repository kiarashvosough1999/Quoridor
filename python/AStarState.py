from copy import copy
from queue import PriorityQueue
from PriorityQueueItem import PriorityQueueItem


class AStar:

    @staticmethod
    def path_heuristic(player):
        if player.color == "white":
            return 100 * abs(player.get_position()[1])
        else:
            return 100 * (abs(player.get_position()[1] - 16))

    @staticmethod
    def cost_evaluator(path, player):
        current_cost = 0
        for state in path:
            current_cost += state.cost
        current_cost += AStar.path_heuristic(player)
        return current_cost

    @staticmethod
    def astar(player, opponent, check_blockage):
        # set of tuple (x, y, move, cost)
        visited = set()

        queue = PriorityQueue()
        pos_x, pos_y = player.get_position()

        queue.put(PriorityQueueItem(priority=0, move_array_tuple=[(pos_x, pos_y, 0, "")]))

        while not queue.empty():
            item = queue.get()

            path = item.move_array_tuple

            move = path[-1][2]  # last item move
            player.play(move, is_evaluating=True)

            if player.is_winner():
                if check_blockage:
                    return True
                final_path = []
                for tuple in path:
                    final_path.append(tuple[-1])  # append move
                player.undo_last_action()
                return len(final_path[1:])

            if path[-1] not in visited:
                not_vis = (path[-1][0], path[-2][1], -path[-1][2], path[-1][3])
                visited.add(not_vis)
                # returns array of (move:str, cost: int)
                for move_with_cost in player.get_legal_actions_with_cost(opponent):
                    # check if this basic state not in visited states
                    new_pos_x, new_pos_y = player.get_position()
                    new_path = (new_pos_x, new_pos_y, -move_with_cost[1], move_with_cost[0])
                    if new_path not in visited:
                        successor_path = copy(path)
                        successor_path.append(new_path)
                        print("dsddsasd")
                        queue.put(PriorityQueueItem(abs(AStar.cost_evaluator(successor_path, player)), successor_path))
            player.undo_last_action()
        if check_blockage:
            return False
        return 0
