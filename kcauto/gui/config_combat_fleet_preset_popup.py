import PySimpleGUI as sg
from gui.layout_base import LayoutBase
from constants import MAX_FLEET_PRESETS


class ConfigCombatFleetPresetPopupLayout(LayoutBase):
    @classmethod
    def get_layout(cls, presets):
        return [
            [
                sg.Text('Combat Fleet Presets', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='presets',
                    values=presets,
                    font=cls.FONT_10,
                    size=(19, 6),
                    enable_events=True),
            ],
            [
                cls.generate_remove_btn('presets', 'remove preset'),
                cls.generate_clear_btn('presets', 'clear presets'),
            ],
            [
                sg.Combo(
                    [str(x) for x in range(1, 15) if str(x) not in presets],
                    key='preset_combo',
                    font=cls.FONT_10,
                    size=(13, 1)),
                cls.generate_add_btn('presets', 'add', size=(5, 1)),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel'),
            ]
        ]

    @classmethod
    def update_gui(cls, presets):
        presets_backup = str(presets)
        presets = presets.split(',')
        while '' in presets:
            presets.remove('')

        popup_window = sg.Window(
            'Combat Fleet Presets',
            cls.get_layout(presets),
            use_default_focus=False,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return ','.join(popup_window['presets'].Values)

            if event == 'cancel':
                popup_window.Close()
                return presets_backup

            if event == 'presets.add':
                lb_values = popup_window['presets'].Values
                lb_values.append(values['preset_combo'])
                popup_window['presets'].Update(values=lb_values)
                popup_window['preset_combo'].Update(
                    value=None,
                    values=[
                        str(x) for x in range(1, MAX_FLEET_PRESETS + 1)
                        if str(x) not in lb_values],
                    set_to_index=None)

            cls.check_listbox_related_events(
                popup_window, event, values, 'presets',
                enabled_events=['remove', 'clear'])

            if event in ('presets.remove', 'presets.clear'):
                popup_window['preset_combo'].Update(
                    value=None,
                    values=[
                        str(x) for x in range(1, 15)
                        if str(x) not in popup_window['presets'].Values],
                    set_to_index=None)

            LayoutBase.update_widgets(popup_window)
