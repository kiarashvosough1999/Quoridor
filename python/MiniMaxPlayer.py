from AStarState import AStar
from Player import Player


class MiniMaxPlayer(Player):
    MAX_DEPTH = 2
    INFINITY = 9999

    def bfs(self, opponent: Player):
        for player in [self, opponent]:
            destination = (
                self.board.get_white_goal_pieces()
                if player.color == "white"
                else self.board.get_black_goal_pieces()
            )
            visited = {}
            distances = {}
            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for i in self.board.get_piece_neighbors(piece):
                    if visited[i] == False:
                        distances[i] = distances[piece] + 1
                        visited[i] = True
                        queue.append(i)

            min_distance = self.INFINITY
            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance

        return self_distance, opponent_distance

    def bfs_with_move(self, opponent: Player, move):
        global self_distance, opponent_distance
        for player in [self, opponent]:
            player.play(move, is_evaluating=True)
            destination = (
                self.board.get_white_goal_pieces()
                if player.color == "white"
                else self.board.get_black_goal_pieces()
            )
            visited = {}
            distances = {}
            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for neighboor_piece in self.board.get_piece_neighbors(piece):
                    if visited[neighboor_piece] is False:
                        distances[neighboor_piece] = distances[piece] + self.score_piece_distance(neighboor_piece)
                        visited[neighboor_piece] = True
                        queue.append(neighboor_piece)

            min_distance = self.INFINITY
            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance
            player.undo_last_action()

        return self_distance, opponent_distance

    def evaluate(self, opponent):
        self_distance, opponent_distance = self.bfs(opponent)
        total_score = (5 * opponent_distance - self_distance) * (
                1 + self.walls_count / 2
        )
        return total_score

    def evaluate_with_move(self, opponent, move, move_evaluation_dict):
        self_distance, opponent_distance = self.bfs_with_move(opponent, move)

        total_score = (5 * opponent_distance - self_distance) * (
                1 + self.walls_count / 2
        )

        move_evaluation_dict[move] = self_distance
        return self_distance

    def evaluation_heuristic(self, opponent):
        result = 0

        if self.color == "black":
            player_one_distance = self.get_position()[1] // 2
            player_two_distance = (9 - opponent.get_position()[1]) // 2
            opponent_path_len, player_path_len = player_two_distance, player_one_distance

            if self.walls_count != 10 and opponent.walls_count != 10:
                player_path_len = AStar.astar(self, opponent, False)

            result += opponent_path_len
            result -= player_one_distance
            num = 100
            if player_path_len != 0:
                num = player_path_len
            result += round(100 / num, 2)

            num_1 = 50
            if player_two_distance != 0:
                num_1 = player_two_distance
            result -= round(50 / num_1, 2)

            result += (self.walls_count - opponent.walls_count)
            if self.get_position()[1] == 0:
                result += 100
            if player_path_len == 0 and self.get_position()[1] != 0:
                result -= 500
            return result

        else:
            player_one_distance = (9 - opponent.get_position()[1]) // 2
            player_two_distance = self.get_position()[1] // 2
            opponent_path_len, player_path_len = player_two_distance, player_one_distance

            if self.walls_count != 10 and opponent.walls_count != 10:
                player_path_len = AStar.astar(self, opponent, False)

            result -= opponent_path_len
            result += player_two_distance
            num = 100
            if player_path_len != 0:
                num = player_path_len
            result += round(100 / num, 2)

            num_1 = 50
            if player_one_distance != 8:
                num_1 = player_one_distance
            result -= round(50 / num_1, 2)

            result += (opponent.walls_count - self.walls_count)
            if opponent.get_position()[1] == 0:
                result += 100
            if opponent_path_len == 0 and opponent.get_position()[1] != 0:
                result -= 500
            return result

    def get_best_action(self, opponent, maximizingPlayer=False):

        value = -self.INFINITY if maximizingPlayer else self.INFINITY

        # we should apply pruning here
        best_action = None

        # min max and pruning happen after making move and before undoing it
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            print(self.board.print_map())
            if self.is_winner():
                self.undo_last_action()
                return action

            if not maximizingPlayer:
                temp = self.minimizer(opponent, self.MAX_DEPTH, -self.INFINITY, self.INFINITY)
                print("min: ", temp)
            else:
                temp = self.maximizer(opponent, self.MAX_DEPTH, -self.INFINITY, self.INFINITY)
                print("max: ", temp)

            if self.is_winner():
                value = max(value, self.evaluation_heuristic(opponent)) if self.color == "white" else min(value,
                                                                                                          self.evaluation_heuristic(
                                                                                                                    opponent))
                if maximizingPlayer:
                    if temp >= value:
                        value = temp
                        best_action = action
                else:
                    if temp <= value:
                        value = temp
                        best_action = action

                self.undo_last_action()
                continue

            if maximizingPlayer:
                if temp >= value:
                    value = temp
                    best_action = action
            else:
                if temp <= value:
                    value = temp
                    best_action = action
            self.undo_last_action()

        return best_action

    def minimizer(self, opponent, depth, alpha, beta):
        if depth == 0 or self.is_winner():
            return self.evaluation_heuristic(opponent)

        value = self.INFINITY

        legal_moves, move_evaluation_dict = self.order_nodes(opponent, maximizingPlayer=False)
        # legal_moves = self.get_legal_actions(opponent)
        for move in legal_moves:
            # if min_move_evaluation_dict[move] - min_move_evaluation_dict[legal_moves[0]] >= 1500:
            #     break
            # if value < move_evaluation_dict[move]:
            #     break
            self.play(move, is_evaluating=True)
            value = min(value, self.maximizer(opponent, depth - 1, alpha, beta))
            if value <= alpha:
                self.undo_last_action()
                return value
            beta = min(value, beta)
            self.undo_last_action()
        return value

    def maximizer(self, opponent, depth, alpha, beta):
        if depth == 0 or self.is_winner():
            return self.evaluation_heuristic(opponent)

        value = -self.INFINITY

        legal_moves, move_evaluation_dict = self.order_nodes(opponent, maximizingPlayer=True)
        # legal_moves = self.get_legal_actions(opponent)
        for move in legal_moves:
            # if max_move_evaluation_dict[legal_moves[0]] - max_move_evaluation_dict[move] >= 1500:
            #     break
            # if value > move_evaluation_dict[move]:
            #     break
            self.play(move, is_evaluating=True)
            value = max(value, self.minimizer(opponent, depth - 1, alpha, beta))
            if value >= beta:
                self.undo_last_action()
                return value
            alpha = max(alpha, value)
            self.undo_last_action()
        return value

    def order_nodes(self, opponent, maximizingPlayer):
        raw_moves = self.get_legal_actions(opponent)
        # sort far walls from opponent

        def order_lambda(move, opponent):
            self.play(move,is_evaluating=True)
            cost = self.evaluation_heuristic(opponent)
            self.undo_last_action()
            return cost

        move_evaluation_dict = {}
        if maximizingPlayer:
            raw_moves.sort(key=lambda move: order_lambda(move, opponent),
                           reverse=True)
        else:
            raw_moves.sort(key=lambda move: order_lambda(move, opponent))
        return raw_moves, move_evaluation_dict
