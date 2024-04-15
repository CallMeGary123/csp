sensor_connections = [
 [1, 0, 1, 1, 1, 1],
 [0, 1, 1, 0, 0, 0],
 [1, 1, 1, 1, 0, 0],
 [1, 0, 1, 1, 0, 0],
 [1, 0, 0, 0, 1, 1],
 [1, 0, 0, 0, 1, 1]]

visibility = [
 [1, 1, 1],
 [1, 0, 1],
 [1, 0, 1],
 [1, 1, 1],
 [1, 1, 0],
 [1, 1, 0]]

import enum
from itertools import combinations
import numpy as np

def generate_unique_groupings(matrix):
    all_groupings = []
    for row in matrix:
        ones_indices = [i for i, val in enumerate(row) if val == 1]
        row_combinations = list(combinations(ones_indices, 3))
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
    min_length = min(len(sublist) for sublist in groupings)
    indices = [index for index, sublist in enumerate(groupings) if len(sublist) == min_length]

    return indices

def conflict_score(item1, item2):
    return len(set(item1) & set(item2))

def valid_choices(sublists,main_list):
    filtered_sublists = []
    for sublist in sublists:
        valid_options = [item for item in sublist if item in main_list]
        if valid_options:
            filtered_sublists.append(valid_options)
    return filtered_sublists

def min_conflict(choices):
    min_conflict_score = float("inf")
    for i,list in enumerate(choices):
        for j,other_list in enumerate(choices):
            if i != j and i<j:
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
            if i != j and i<j:
                for item1 in list:
                    other_list = choices[j]
                    for item2 in other_list:
                        score = conflict_score(item1, item2)
                        if score == min_conflict_score == 0 and (i,item1) not in optimal_choices and (j,item2) not in optimal_choices:
                            optimal_choices.append((i,item1))
                            optimal_choices.append((j,item2))
                        elif score == min_conflict_score != 0 and (i,item1) not in optimal_choices:
                            print(item1, item2, score)
                            optimal_choices.append((i,item1))
    return(optimal_choices)
def identify_targets(visibility, sensor_connections):
    possible_solutins = []
    target_sensor_index = []
    row, col = np.shape(visibility)
    optimal = int(row / 3)
    print("opt:", optimal)
    visibility_t = np.transpose(visibility)
    assignement = np.zeros_like(visibility)
    sesnor_groups = generate_unique_groupings(sensor_connections)
    candidate_groups = generate_groupings(visibility_t)
    candidates = generate_candidates(candidate_groups)
    valid = valid_choices(candidate_groups, sesnor_groups)
    mini = min_conflict(valid)
    optimal = optimal_choices(valid, candidates, mini)
    print(optimal)
identify_targets(visibility, sensor_connections)
