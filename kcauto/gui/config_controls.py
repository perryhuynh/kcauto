import os
import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from gui.config_methods import ConfigMethods
from util.json_data import JsonData


class ConfigControls(LayoutBase):
    DEF_PATH = os.path.join(os.getcwd(), 'configs', 'config.json')
    JSON_FILETYPE = ('JSON file', '*.json')
    INITIAL_CONFIG_FOLDER = 'configs'

    @classmethod
    def get_layout(cls):
        return [
            sg.Button(
                'save & overwrite',
                key='save',
                font=cls.FONT_10,
                pad=cls.PAD_BUTTON_CONTROLS),
            sg.FileSaveAs(
                'save as',
                key='save_as',
                font=cls.FONT_10,
                pad=cls.PAD_BUTTON_CONTROLS,
                target='save_cfg_path',
                file_types=(cls.JSON_FILETYPE, ),
                initial_folder=cls.INITIAL_CONFIG_FOLDER),
            sg.FileBrowse(
                'load',
                key='load',
                font=cls.FONT_10,
                pad=cls.PAD_BUTTON_CONTROLS,
                target='load_cfg_path',
                file_types=(cls.JSON_FILETYPE, ),
                initial_folder=cls.INITIAL_CONFIG_FOLDER),
            sg.InputText(
                key='save_cfg_path',
                enable_events=True,
                visible=False,
                disabled=True),
            sg.InputText(
                key='load_cfg_path',
                enable_events=True,
                visible=False,
                disabled=True),
            sg.InputText(
                cls.DEF_PATH,
                key='cfg_path',
                visible=False,
                disabled=True),
            sg.Text('loaded config:', pad=((5, 0), 0)),
            sg.Text(
                os.path.basename(cls.DEF_PATH),
                key='cfg_filename',
                font=('Courier New', 10),
                size=(30, 1)),
        ]

    @staticmethod
    def update_cfg_filename(window, path):
        window['cfg_filename'].Update(os.path.basename(path))

    @staticmethod
    def save_cfg(path, window, values):
        cfg = ConfigMethods.generate_config_dict(window, values)
        JsonData.dump_json(cfg, path, pretty=True)

    @staticmethod
    def load_cfg(path, window, event, values):
        cfg = JsonData.load_json(path)
        ConfigMethods.unpack_config_dict(window, cfg)
