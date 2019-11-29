import PySimpleGUI as sg
from gui.layout_base import LayoutBase

from kca_enums.expeditions import ExpeditionEnum


class ConfigExpeditionPopupLayout(LayoutBase):
    @classmethod
    def get_layout(cls, fleet_id, expeditions, other_expeditions):
        return [
            [
                sg.Text(
                    f'Fleet {fleet_id} Expeditions',
                    font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='expeditions',
                    values=expeditions,
                    font=cls.FONT_10,
                    size=(34, 5),
                    enable_events=True)
            ],
            [
                cls.generate_remove_btn(
                    'expeditions', 'remove selected expedition', size=(20, 1)),
                cls.generate_clear_btn(
                    'expeditions', 'clear expeditions', size=(20, 1)),
            ],
            [
                sg.Combo(
                    [
                        x.display_name for x in ExpeditionEnum
                        if x.display_name
                        not in expeditions + other_expeditions],
                    key='expedition_combo',
                    font=cls.FONT_10,
                    size=(28, 1)),
                cls.generate_add_btn('expeditions', 'add', size=(5, 1)),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel'),
            ]
        ]

    @classmethod
    def update_gui(cls, fleet_id, expeditions, other_expeditions):
        expeditions_backup = str(expeditions)
        initial_expeditions = expeditions.split(',')
        other_expeditions = other_expeditions.split(',')
        while '' in initial_expeditions:
            initial_expeditions.remove('')
        while '' in other_expeditions:
            other_expeditions.remove('')

        popup_window = sg.Window(
            f"Fleet {fleet_id} Expeditions",
            cls.get_layout(fleet_id, initial_expeditions, other_expeditions),
            use_default_focus=False,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return ','.join(popup_window['expeditions'].Values)

            if event == 'cancel':
                popup_window.Close()
                return expeditions_backup

            if event == 'expeditions.add':
                lb_values = popup_window['expeditions'].Values
                lb_values.append(values['expedition_combo'])
                popup_window['expeditions'].Update(values=lb_values)
                popup_window['expedition_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in ExpeditionEnum
                        if x.display_name
                        not in lb_values + other_expeditions],
                    set_to_index=None)

            cls.check_listbox_related_events(
                popup_window, event, values, 'expeditions',
                enabled_events=['remove', 'clear'])

            if event in ('expeditions.remove', 'expeditions.clear'):
                popup_window['expedition_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in ExpeditionEnum
                        if x.display_name
                        not in popup_window['expeditions'].Values
                        + other_expeditions],
                    set_to_index=None)

            LayoutBase.update_widgets(popup_window)
