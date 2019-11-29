import PySimpleGUI as sg
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.layout_base import LayoutBase

matplotlib.use('TkAgg')


class ClickPlotter(LayoutBase):
    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [sg.Canvas(key='click_plot')],
                [sg.Text("", key='unique_click_points', size=(50, 1))],
                [sg.Button('Refresh', key='refresh_click_plot')]
            ],
            key='gui_tab_click_plot',
            size=cls.PRIMARY_COL_TAB_SIZE,
            visible=False
        )

    @classmethod
    def draw_plot(cls, window):
        if not plot.canvas:
            plot.create_canvas(window['click_plot'].TKCanvas)
        try:
            raw = np.load('click_matrix.npz')
            click_plot = raw['click_matrix']
            max_clicks = click_plot.max()
            window['unique_click_points'].Update(
                f"{np.count_nonzero(click_plot)} unique points clicked "
                f"(max click on point: {max_clicks})")
            plot.update(click_plot)
        except FileNotFoundError:
            pass

    @classmethod
    def update_gui(cls, window, event, values):
        if event in ('refresh_click_plot', 'tab_gui_click_plot'):
            cls.draw_plot(window)


class Plot(object):
    canvas = None
    colorbar = None

    def __init__(self):
        self.fig = plt.gcf()
        plt.axis('off')
        plt.tight_layout()

    def create_canvas(self, canvas):
        self.canvas = FigureCanvasTkAgg(self.fig, canvas)

    def update(self, data):
        plt.imshow(data, cmap='hot', interpolation='none')
        if not self.colorbar:
            self.colorbar = plt.colorbar(
                orientation='horizontal', pad=0, shrink=0.8, aspect=40)
            self.colorbar.ax.tick_params(labelsize=7)
        self.colorbar.mappable.set_clim(data.min(), data.max())
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


plot = Plot()
