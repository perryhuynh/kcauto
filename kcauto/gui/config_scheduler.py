import PySimpleGUI as sg
from gui.layout_base import LayoutBase
from gui.config_scheduler_popup import ConfigSchedulerPopupLayout


class ConfigSchedulerLayout(LayoutBase):
    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Text('Scheduler', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled', key='scheduler.enabled', enable_events=True)
                ],
                [
                    sg.Text('Scheduler Rules', **cls.LABEL_SETTINGS),
                    sg.Listbox(
                        key='scheduler.rules',
                        values=[],
                        font=cls.FONT_10,
                        size=(54, 4),
                        enable_events=True)
                ],
                [
                    sg.Text('', **cls.LABEL_SETTINGS),
                    cls.generate_edit_btn('scheduler.rules', size=(20, 1)),
                    cls.generate_remove_btn('scheduler.rules', size=(20, 1)),
                    cls.generate_clear_btn('scheduler.rules', size=(20, 1)),
                ]
            ],
            key='config_scheduler_col',
            visible=False)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = (
            'scheduler.rules', 'scheduler.rules.edit',
        )

        if values['scheduler.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
        else:
            cls.update_window_elements(window, elements, {'disabled': True})

        cls.check_listbox_related_events(
            window, event, values, 'scheduler.rules',
            enabled_events=['remove', 'clear'])

        if event == 'scheduler.rules.edit':
            window.Hide()
            new_values = ConfigSchedulerPopupLayout.update_gui(
                window['scheduler.rules'].Values)
            window['scheduler.rules'].Update(values=new_values)
            window.UnHide()
