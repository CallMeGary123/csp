from itertools import combinations
import numpy as np

def generate_unique_groupings(matrix):
    all_groupings = []
    for row in matrix:
        #print(row)
        ones_indices = [i for i, val in enumerate(row) if val == 1]
        #print(ones_indices)
        row_combinations = list(combinations(ones_indices, 3))
        #print(row_combinations)
        all_groupings.extend(row_combinations)  # Extend the list instead of appending
    # Remove duplicates by converting to a set and back to a list
    unique_groupings = list(set(all_groupings))
    return unique_groupings


def generate_groupings(matrix):
    all_groupings = []
    for row in matrix:
        ones_indices = [i for i, val in enumerate(row) if val == 1]
        row_combinations = list(combinations(ones_indices, 3))
        all_groupings.append(row_combinations)
    return all_groupings


def generate_candidates(groupings):
    min_length = float("inf")
    for sublist in groupings:
        if len(sublist) < min_length and len(sublist) != 0:
            min_length = len(sublist)
    indices = [
        index for index, sublist in enumerate(groupings) if len(sublist) == min_length
    ]

    return indices


def conflict_score(item1, item2):
    return len(set(item1) & set(item2))


def valid_choices(sublists, main_list):
    # print(sublists)
    filtered_sublists = []
    for sublist in sublists:
        if sublist == []:
            filtered_sublists.append(sublist)
        else:
            valid_options = [item for item in sublist if item in main_list]
            if valid_options:
                filtered_sublists.append(valid_options)
    return filtered_sublists


def min_conflict(choices):
    min_conflict_score = float("inf")
    for i, list in enumerate(choices):
        for j, other_list in enumerate(choices):
            if i != j and i < j:
                for item1 in list:
                    for item2 in other_list:
                        score = conflict_score(item1, item2)
                        min_conflict_score = min(min_conflict_score, score)
    return min_conflict_score


def optimal_choices(choices, indexes, min_conflict_score):
    optimal_choices = []
    for i in indexes:
        list = choices[i]
        for j in indexes:
            if i != j and i < j:
                for item1 in list:
                    other_list = choices[j]
                    for item2 in other_list:
                        score = conflict_score(item1, item2)
                        if (
                            score == min_conflict_score == 0
                            and (i, item1) not in optimal_choices
                            and (j, item2) not in optimal_choices
                        ):
                            optimal_choices.append((i, item1))
                            optimal_choices.append((j, item2))
                        elif (
                            score == min_conflict_score != 0
                            and (i, item1) not in optimal_choices
                        ):
                            optimal_choices.append((i, item1))
            elif i == j and len(indexes) == 1:
                for item in list:
                    optimal_choices.append((i, item))
    return optimal_choices


def get_choices(visibility, sesnor_groups):
    visibility_t = np.transpose(visibility)
    candidate_groups = generate_groupings(visibility_t)
    #print(candidate_groups)
    candidates = generate_candidates(candidate_groups)
    #print("cand:",candidates)
    valid = valid_choices(candidate_groups, sesnor_groups)
    #print("valid:",valid)
    mini = min_conflict(valid)
    #print("mini:", mini)
    optimal = optimal_choices(valid, candidates, mini)
    #print(optimal)
    return optimal


def generate_array_with_ones(x, positions):
    # Create an array of zeros with length x
    result = np.zeros(x)

    # Set the specified positions to 1
    if type(positions) == int:
        result[positions] = 1
    else:
        for i in positions:
            result[i] = 1

    return result


def transition(matrix, choice):
    rows, cols = np.shape(matrix)
    new_matrix = np.array(matrix)
    for row in choice[1]:
        new_matrix[row] = generate_array_with_ones(cols, choice[0])
    new_matrix = np.transpose(new_matrix)
    new_matrix[choice[0]] = 0
    return np.transpose(new_matrix)


def update_solution(matrix, choice):
    rows, cols = np.shape(matrix)
    new_matrix = np.array(matrix)
    new_matrix = np.transpose(new_matrix)
    new_matrix[choice[0]] = generate_array_with_ones(rows, choice[1])
    return np.transpose(new_matrix)


class Node:
    def __init__(
        self,
        parent=None,
        visibility_matrix=None,
        sensor_groups=None,
        depth=None,
        solution=None,
    ):
        self.parent = parent
        self.visibility_matrix = visibility_matrix
        self.sensor_groups = sensor_groups
        self.optimal_choices = get_choices(visibility_matrix, sensor_groups)
        self.depth = depth
        self.solution = solution

def solve_csp(current_node, depth, opt, answer):
    while True:
        if current_node.optimal_choices != []:
            updated_sensor_groups = list(current_node.sensor_groups)
            updated_sensor_groups.remove(current_node.optimal_choices[0][1])
            new_node = Node(parent=current_node, visibility_matrix=transition(current_node.visibility_matrix, current_node.optimal_choices[0]), sensor_groups= updated_sensor_groups, depth=current_node.depth + 1,solution= update_solution(current_node.solution, current_node.optimal_choices[0]))
            current_node.optimal_choices.remove(current_node.optimal_choices[0])
            current_node = new_node
            if current_node.depth > depth:
                answer = current_node.solution
                depth = current_node.depth
                if depth == opt:
                    break 
        elif current_node.optimal_choices == [] and current_node.parent is not None:
            current_node = current_node.parent
        else:
            break
    return answer
