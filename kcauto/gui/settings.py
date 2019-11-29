import PySimpleGUI as sg
import subprocess

from gui.layout_base import LayoutBase
from util.json_data import JsonData


class Settings(LayoutBase):
    @classmethod
    def get_layout(cls):
        settings = cls.load_settings()
        chrome_path = (
            settings['chrome_path'] if 'chrome_path' in settings else '')
        python_cmd = (
            settings['python_command']
            if 'python_command' in settings
            else cls.autodetect_python())
        track_clicks = (
            settings['track_clicks'] if 'track_clicks' in settings else True)
        debug_output = (
            settings['debug_output'] if 'debug_output' in settings else False)
        return sg.Column(
            [
                [
                    sg.Text(f'Chrome path', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        chrome_path,
                        key=f'gui.chrome_path',
                        font=cls.FONT_10,
                        size=(50, 1),
                        enable_events=True),
                    sg.FileBrowse(
                        'browse',
                        key='browse_to_chrome',
                        font=cls.FONT_8,
                        button_color=cls.COLORS_STANDARD_BUTTON,
                        target='gui.chrome_path'),
                ],
                [
                    sg.Text(f'Python command', **cls.LABEL_SETTINGS),
                    sg.InputText(
                        python_cmd,
                        key=f'gui.python_command',
                        font=cls.FONT_10,
                        size=(20, 1),
                        enable_events=True),
                    sg.Button(
                        'autodetect',
                        key='autodetect_python',
                        font=cls.FONT_8,
                        button_color=cls.COLORS_STANDARD_BUTTON),
                ],
                [
                    sg.Text('', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Track Clicks',
                        default=track_clicks,
                        key='gui.track_clicks',
                        enable_events=True),
                    sg.Checkbox(
                        'Debug Console Output',
                        default=debug_output,
                        key='gui.debug_output',
                        enable_events=True),
                ],
                [
                    sg.Text('', **cls.LABEL_SETTINGS),
                    sg.Button(
                        'Save',
                        key='save_settings'),
                ]
            ],
            key='gui_tab_settings',
            size=cls.PRIMARY_COL_TAB_SIZE,
            visible=False
        )

    def load_settings():
        try:
            settings = JsonData.load_json('gui_settings.json')
            return settings
        except FileNotFoundError:
            return {}

    def save_settings(values):
        settings = {
            'chrome_path': values['gui.chrome_path'],
            'python_command': values['gui.python_command'],
            'track_clicks': values['gui.track_clicks'],
            'debug_output': values['gui.debug_output'],
        }
        JsonData.dump_json(settings, 'gui_settings.json', pretty=True)

    def autodetect_python():
        for cmd in (('python', ), ('python3', ), ('py', '-3')):
            output = subprocess.run([*cmd, '--version'], capture_output=True)
            if (
                    output.stdout
                    and output.stdout.decode('utf-8').split(' ')[1][0] == '3'):
                return ' '.join(cmd)
        return ''

    @classmethod
    def update_gui(cls, window, event, values):
        if event == 'save_settings':
            cls.save_settings(values)

        if event == 'autodetect_python':
            window['gui.python_command'].Update(cls.autodetect_python())
