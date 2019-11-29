import numpy as np
import util.kca as kca_u
from constants import GAME_W, GAME_H


class ClickTracker(object):
    click_matrix = None

    def __init__(self):
        try:
            raw = np.load('click_matrix.npz')
            self.click_matrix = raw['click_matrix']
        except FileNotFoundError:
            self.click_matrix = np.zeros(shape=(GAME_H, GAME_W))

    def track_click(self, r, x, y):
        game_x = x - kca_u.kca.game_x
        game_y = y - kca_u.kca.game_y
        self.click_matrix[game_y][game_x] += 1

    def export(self):
        np.savez('click_matrix', click_matrix=self.click_matrix)


click_tracker = ClickTracker()
