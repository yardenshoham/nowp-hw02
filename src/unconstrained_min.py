import math
import utils
import numpy as np


def line_search(dir_selection_method, f, x0, step_size, obj_tol, param_tol, max_iter, init_step_len, slope_ratio, back_track_factor):
    x_prev = x0
    f_prev, df_prev, hessian_prev = f(x0)
    path = [x_prev]
    i = 0
    success = False
    while i < max_iter:
        if dir_selection_method == 'gd':
            selected_dir = -df_prev
        elif dir_selection_method == 'nt':
            selected_dir = newton_dir(hessian_prev, df_prev)
        elif dir_selection_method == 'bfgs':
            pass
        x_next = x_prev + step_size * selected_dir
        step_length = np.linalg.norm(x_next - x_prev)
        if step_length < param_tol:
            success = True
            print(
                f"Success! A small enough distance (<{param_tol}) between two consecutive iteration locations was achieved.")
            break
        f_next, df_next, hessian_next = f(x_next)
        path.append(x_next)
        change = abs(f_next - f_prev)
        if change < obj_tol:
            success = True
            print(
                f"Success! A small enough change (<{obj_tol}) in objective function values, between two consecutive iterations was achieved.")
            break
        i += 1
        utils.report(i, x_next, f_next, step_length, change)
        f_prev = f_next
        df_prev = df_next
        x_prev = x_next
        hessian_prev = hessian_next
    return x_next, success, path


def newton_dir(hessian_prev, df_prev):
    return np.linalg.solve(hessian_prev, -df_prev)