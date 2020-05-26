import numpy as np
import collections
import time


def calculation(arr: np.array):
    M = arr.shape[0]
    mat = arr.copy()

    # step 1: substract smallest element in rach row
    for i, row in enumerate(mat):
        mat[i, :] -= row.min()

    # step 2: substract smallest element in each col
    for i, col in enumerate(mat.transpose()):
        mat[:, i] -= col.min()

    # 步骤 3： 使用最少数量的划线覆盖矩阵中所有的0元素
    # 如果划线总数不等于矩阵的维度需要进行矩阵调整并重复循环此步骤
    total_covered = 0
    while total_covered < M:
        zero_mat = (mat == 0)

        # step 3:
        marked_zeros = []
        while True:
            # 循环直到所有零元素被处理
            if True not in zero_mat:
                break
            zero_mat, marked_zeros = row_scan(zero_mat, marked_zeros)

        # 2、无被标记0（独立零元素）的行打勾
        independent_zero_row_list = [pos[0] for pos in marked_zeros]
        ticked_row = list(set(range(M)) - set(independent_zero_row_list))

        zero_mat = (mat == 0)
        # 重复直到不能再打勾
        ticked_col = []
        TICK_FLAG = True
        while TICK_FLAG:
            TICK_FLAG = False
            # 3、对打勾的行中所含0元素的列打勾
            for row in ticked_row:
                # 找到此行
                row_array = zero_mat[row, :]
                # 找到此行中0元素的索引位置
                for i, ele in enumerate(row_array):
                    if ele == True and i not in ticked_col:
                        ticked_col.append(i)
                        TICK_FLAG = True

            # 4、对打勾的列中所含独立0元素的行打勾
            for row, col in marked_zeros:
                if col in ticked_col and row not in ticked_row:
                    ticked_row.append(row)
                    TICK_FLAG = True

        # 对打勾的列和没有打勾的行画线
        row_covered = list(set(range(M)) - set(ticked_row))
        col_covered = ticked_col

        total_covered = len(row_covered) + len(col_covered)
        # 如果划线总数不等于矩阵的维度需要进行矩阵调整（需要使用未覆盖处的最小元素）
        if total_covered < M:
            mat = adjust_matrix_by_min_uncovered_num(mat, row_covered, col_covered)

    # 元组形式结果对存放到列表
    value = 0
    for row, column in marked_zeros:
        value += arr[row, column]
    return marked_zeros, value


def adjust_matrix_by_min_uncovered_num(result_matrix, row_covered, col_covered):
    row_uncovered = list(set(range(result_matrix.shape[0])) - set(row_covered))
    col_uncovered = list(set(range(result_matrix.shape[1])) - set(col_covered))
    mat_uncovered = result_matrix[row_uncovered, :][:, col_uncovered]
    min_uncovered = mat_uncovered.min()

    # 未被覆盖元素减去最小值m
    for row_index, row in enumerate(result_matrix):
        if row_index not in row_covered:
            for index, element in enumerate(row):
                if index not in col_covered:
                    result_matrix[row_index, index] -= min_uncovered

    # 行列划线交叉处加上最小值m
    for row in row_covered:
        for col in col_covered:
            result_matrix[row, col] += min_uncovered

    return result_matrix


def row_scan(mat_input, marked_zeros):
    """
    Get marked zeros in the matrix
    :param mat_input: will be changed in-place
    :param marked_zeros: Index of marked zeros
    :return:
    """
    mat = mat_input.copy()

    row_num_zero = mat.sum(axis=1)
    valid_idx = np.where(row_num_zero > 0)[0]

    min_row_num = row_num_zero[valid_idx].min()
    min_row_pos = np.where(row_num_zero == min_row_num)[0][0]

    row_min = mat[min_row_pos, :]

    row_col_index, = np.where(row_min == True)  # get zero location
    marked_zeros.append((min_row_pos, row_col_index[0]))  # loc of zero

    # 划去该0元素所在行和列存在的0元素
    # 因为被覆盖，所以把二值矩阵_zero_locations中相应的行列全部置为false
    # clear row and col:
    mat[:, row_col_index[0]] = False
    mat[min_row_pos, :] = False
    return mat, marked_zeros


if __name__ == "__main__":
    profit_matrix = [
            [62, 75, 80, 93, 95, 97],
            [75, 80, 82, 85, 71, 97],
            [80, 75, 81, 98, 90, 97],
            [78, 82, 84, 80, 50, 98],
            [90, 85, 85, 80, 85, 99],
            [65, 75, 80, 75, 68, 96]]

    p = np.array(profit_matrix)

    m = calculation(p)
    print(m)
