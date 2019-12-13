# This script is a minimum bfs module
# Author by lwl

__all__ = ["is_on_board", "move", "create_board_like", "vset", "vget", "shortest_paths"]

from typing import List, Tuple, Set, Any
from collections import deque


def is_on_board(board: List[List[int]], point: Tuple[int, int]) -> bool:
    """
    check if certain point is on board
    :param board: 2D list
    :param point: 2D index in form of (int, int)
    :return: bool
    """
    x_len, y_len = len(board), len(board[0])
    return 0 <= point[0] < x_len and 0 <= point[1] < y_len


def move(point: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[int, int]:
    """
    given point and direction, get the point of next step
    :param point: 2D index in form of (int, int)
    :param direction: vector in form of (int, int)
    :return: 2D index in form of (int, int)
    """
    return (point[0] + direction[0], point[1] + direction[1])


def create_board_like(board: List[List[int]], default_value=0) -> List[List[Any]]:
    """
    create 2D list of same shape as the given board
    :param board: 2D list
    :param default_value: any value
    :return: 2D list filled with default_value
    """
    return [[default_value] * len(board[0]) for _ in range(len(board))]


def vset(board: List[List[int]], point: Tuple[int, int], var) -> None:
    """
    easy method for setting value in 2D list
    :param board: 2D list
    :param point: 2D index in form of (int, int)
    :param var: any value
    :return: None
    """
    if not is_on_board(board, point):
        raise ValueError("{} is not on board".format(point))
    board[point[0]][point[1]] = var


def vget(board: List[List[int]], point: Tuple[int, int], default_value=None) -> Any:
    """
    easy method for getting value from 2D list
    :param board: 2D list
    :param point: 2D index in form of (int, int)
    :param default_value: if corresponding value on board is None, return default_value, else return value on board
    :return: corresponding value on board
    """
    if not is_on_board(board, point):
        raise ValueError("{} is not on board".format(point))
    if board[point[0]][point[1]] is None and default_value is not None:
        vset(board, point, default_value)
    return board[point[0]][point[1]]


def _trace(
    from_map: List[List[List[Tuple[int, int]]]], start: Tuple[int, int], end: Tuple[int, int]
) -> List[List[Tuple[int, int]]]:
    """
    private method used by shortest_paths. trace the path *from start to end*
    :param from_map: 2D list of (list of point), each point points to the last step point
    :param start: 2D index in form of (int, int)
    :param end: 2D index in form of (int, int)
    :return: list of tracing list
    """

    def trace_helper(cur_trace_list: List[Tuple[int, int]], results: List[Any]):
        if cur_trace_list[-1] == start:
            results.append(cur_trace_list)
            return
        for next_trace in vget(from_map, cur_trace_list[-1], []):
            trace_helper(cur_trace_list + [next_trace], results)

    results = []
    trace_helper([end], results)
    return [trace[::-1] for trace in results]


def shortest_paths(
    board: List[List[int]], start: Tuple[int, int], end: Tuple[int, int], roadblock: Any = None
) -> List[List[Tuple[int, int]]]:
    """
    given 2D board, start point and end point, (and roadblock maybe), return list of shortest path
    :param board: 2D list of value, with value {roadblock} as roadblock value
    :param start: 2D index in form of (int, int)
    :param end: 2D index in form of (int, int)
    :param roadblock: value that represents roadblock
    :return: list of tracing list, a tracing list is made up of point tuple
    """
    if len(board) == 0 or len(board[0]) == 0:
        return []  # empty paths

    if not (is_on_board(board, start) and is_on_board(board, end)):
        raise ValueError("{} or {} is out of board".format(start, end))

    steps_map: List[List[Any]] = create_board_like(board, default_value=-1)
    from_map: List[List[Any]] = create_board_like(board, default_value=None)

    vset(steps_map, start, 0)
    vset(from_map, start, [])
    queue = deque([start])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while queue:
        cur_point = queue.pop()
        for direction in directions:
            new_point = move(cur_point, direction)
            if not is_on_board(board, new_point) or vget(board, new_point) == roadblock:
                continue
            if vget(steps_map, new_point) < 0:  # never been here
                vset(steps_map, new_point, vget(steps_map, cur_point) + 1)
                vget(from_map, new_point, []).append(cur_point)
                if new_point != end:
                    queue.appendleft(new_point)
            elif vget(steps_map, new_point) == vget(steps_map, cur_point) + 1:
                vget(from_map, new_point, []).append(cur_point)
            elif vget(steps_map, new_point) > vget(steps_map, cur_point) + 1:
                vset(from_map, new_point, [cur_point])
    return _trace(from_map, start, end)


if __name__ == "__main__":
    ## hard test
    # test_board = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # ]
    # print(shortest_paths(test_board, (0, 0), (10, 9)))

    ## easy test
    test_board = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    print(shortest_paths(test_board, (0, 0), (2, 3), roadblock=1))
