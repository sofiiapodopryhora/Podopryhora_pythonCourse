matrix = [
    [3, 2, 1, 0],
    [0, 0, 0, 0],
    [7, 8, -9, 0],
    [1, 0, 2, 0],
    [-4, 4, 5, 0]
]

def find_count_rows_without_zero(matrix):
    count = 0
    for row in matrix:
        if 0 not in row:
            count += 1
    return count

def find_max_repeated_number(matrix):
    dict = {}
    max_repeated = None

    for row in matrix:
        for num in row:
            if num in dict:
                dict[num] += 1
            else:
                dict[num] = 1

    for num, count in dict.items():
        if count > 1:
            if max_repeated is None or num > max_repeated:
                max_repeated = num

    return max_repeated

def sum_elements_with_negatives(matrix):
    total = 0
    for row in matrix:
        negative = any(x < 0 for x in row)
        if negative:
            total += sum(row)
    return total

def find_saddle_points(matrix):
    saddle_points = []
    rows = len(matrix)

    for i in range(rows):
        row = matrix[i]
        min_in_row = min(row)
        min_cols = [j for j, x in enumerate(row) if x == min_in_row]

        for j in min_cols:
            column = [matrix[k][j] for k in range(rows)]
            max_in_col = max(column)
            if matrix[i][j] == max_in_col:
                saddle_points.append((i, j))

    return saddle_points

def compress_matrix(matrix):
    non_zero_rows = []
    for row in matrix:
        if any(element != 0 for element in row):
            non_zero_rows.append(row)
    print(non_zero_rows)

    non_zero_cols = []
    for col in range(len(non_zero_rows[0])):
        if any(row[col] != 0 for row in non_zero_rows):
            non_zero_cols.append(col)
    print(non_zero_cols)

    result = []
    for row in non_zero_rows:
        result.append([row[col] for col in non_zero_cols])

    return result

def find_first_row_with_positive(matrix):
    first = None
    for i, row in enumerate(matrix):
        if any(x > 0 for x in row):
            first = i
            break
    return first

print('1.1) Nums of rows without 0:', find_count_rows_without_zero(matrix))
print('1.2) Max num, more than 1:', find_max_repeated_number(matrix))
print('6.1) Sum of elements in rows with negatives:', sum_elements_with_negatives(matrix))
print('6.2) Saddle points:', find_saddle_points(matrix))
print('12.1) Compressed matrix:', compress_matrix(matrix))
print('12.2) First row with positive element:', find_first_row_with_positive(matrix))
