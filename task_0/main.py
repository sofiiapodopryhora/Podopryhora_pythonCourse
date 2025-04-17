from collections import defaultdict


MATRIX = [
    [3, 2, 1, 0],
    [0, 0, 0, 0],
    [7, 8, -9, 0],
    [1, 0, 2, 0],
    [-4, 4, 5, 0]
]

def count_rows_without_zero(matrix):
    return sum(0 not in row for row in matrix)

def find_max_repeated_number(matrix):
    num_counts = defaultdict(int)

    for row in matrix:
        for num in row:
            num_counts[num] += 1

    return max((num for num, count in num_counts.items() if count > 1), default=None)

def sum_elements_with_negatives(matrix):
    return sum(sum(row) for row in matrix if any(x < 0 for x in row))

def find_saddle_points(matrix):
    saddle_points = []
    rows = len(matrix)

    for i, row in enumerate(matrix):
        min_in_row = min(row)
        min_cols = [j for j, x in enumerate(row) if x == min_in_row]

        for j in min_cols:
            column = [matrix[k][j] for k in range(rows)]
            max_in_col = max(column)
            if matrix[i][j] == max_in_col:
                saddle_points.append((i, j))

    return saddle_points

def compress_matrix(matrix):
    non_zero_rows = [row for row in matrix if any(element != 0 for element in row)]
    print(non_zero_rows)

    non_zero_cols = [col for col in range(len(non_zero_rows[0])) 
                    if any(row[col] != 0 for row in non_zero_rows)]
    print(non_zero_cols)

    return [[row[col] for col in non_zero_cols] for row in non_zero_rows]

def find_first_row_with_positive(matrix):
    first = None
    for i, row in enumerate(matrix):
        if any(x > 0 for x in row):
            first = i
            break
    return first

def main():
    print('1.1) Number of rows without 0:', count_rows_without_zero(MATRIX))
    print('1.2) Max repeated number:', find_max_repeated_number(MATRIX))
    print('6.1) Sum of elements in rows with negatives:', sum_elements_with_negatives(MATRIX))
    print('6.2) Saddle points:', find_saddle_points(MATRIX))
    print('12.1) Compressed matrix:', compress_matrix(MATRIX))
    print('12.2) First row with positive element:', find_first_row_with_positive(MATRIX))

if __name__ == "__main__":
    main()