import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.nodes import NamedNodeEnum


class ConfigCombatNodeSelectPopupLayout(LayoutBase):
    @classmethod
    def get_layout(cls, node_selects):
        return [
            [
                sg.Text('Node Selects', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='node_selects',
                    values=node_selects,
                    font=cls.FONT_10,
                    size=(21, 6),
                    enable_events=True),
            ],
            [
                cls.generate_remove_btn(
                    'node_selects', 'remove node select'),
                cls.generate_clear_btn('node_selects', 'clear node selects'),
            ],
            [
                sg.Combo(
                    [
                        x.display_name for x in NamedNodeEnum
                        if x.display_name not in [y[0] for y in node_selects]],
                    key='node_1_combo',
                    font=cls.FONT_10,
                    size=(4, 1)),
                sg.Text(' to ', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in NamedNodeEnum],
                    key='node_2_combo',
                    font=cls.FONT_10,
                    size=(4, 1)),
                cls.generate_add_btn('node_selects', 'add', size=(5, 1)),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel'),
            ]
        ]

    @classmethod
    def update_gui(cls, node_selects):
        node_selects_backup = str(node_selects)
        node_selects = node_selects.split(',')
        while '' in node_selects:
            node_selects.remove('')

        popup_window = sg.Window(
            'Node Selects',
            cls.get_layout(node_selects),
            use_default_focus=False,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return ','.join(popup_window['node_selects'].Values)

            if event == 'cancel':
                popup_window.Close()
                return node_selects_backup

            if event == 'node_selects.add':
                lb_values = popup_window['node_selects'].Values
                lb_values.append(
                    f"{values['node_1_combo']}>{values['node_2_combo']}")
                popup_window['node_selects'].Update(values=lb_values)
                popup_window['node_1_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NamedNodeEnum
                        if x.display_name
                        not in [y.split('>')[0] for y in lb_values]],
                    set_to_index=None)

            cls.check_listbox_related_events(
                popup_window, event, values, 'node_selects',
                enabled_events=['remove', 'clear'])

            if event in ('node_selects.remove', 'node_selects.clear'):
                popup_window['node_1_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NamedNodeEnum
                        if x.display_name
                        not in [
                            y.split('>')[0]
                            for y in popup_window['node_selects'].Values]],
                    set_to_index=None)

            if values['node_1_combo'] == values['node_2_combo']:
                popup_window['node_selects.add'].Update(disabled=True)
            else:
                popup_window['node_selects.add'].Update(disabled=False)

            LayoutBase.update_widgets(popup_window)
