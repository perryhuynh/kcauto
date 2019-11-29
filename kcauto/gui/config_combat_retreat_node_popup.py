import PySimpleGUI as sg
from gui.layout_base import LayoutBase

from kca_enums.nodes import NodeEnum


class ConfigCombatRetreatNodePopupLayout(LayoutBase):
    @classmethod
    def get_layout(cls, nodes):
        return [
            [
                sg.Text('Retreat Nodes', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='nodes',
                    values=nodes,
                    font=cls.FONT_10,
                    size=(19, 6),
                    enable_events=True),
            ],
            [
                cls.generate_remove_btn('nodes', 'remove node'),
                cls.generate_clear_btn('nodes', 'clear nodes'),
            ],
            [
                sg.Combo(
                    [
                        x.display_name for x in NodeEnum
                        if x.display_name not in nodes],
                    key='node_combo',
                    font=cls.FONT_10,
                    size=(13, 1)),
                cls.generate_add_btn('nodes', 'add', size=(5, 1)),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel'),
            ]
        ]

    @classmethod
    def update_gui(cls, nodes):
        nodes_backup = str(nodes)
        nodes = nodes.split(',')
        while '' in nodes:
            nodes.remove('')

        popup_window = sg.Window(
            'Retreat Points',
            cls.get_layout(nodes),
            use_default_focus=False,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return ','.join(popup_window['nodes'].Values)

            if event == 'cancel':
                popup_window.Close()
                return nodes_backup

            if event == 'nodes.add':
                lb_values = popup_window['nodes'].Values
                lb_values.append(values['node_combo'])
                popup_window['nodes'].Update(values=lb_values)
                popup_window['node_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NodeEnum
                        if x.display_name not in lb_values],
                    set_to_index=None)

            cls.check_listbox_related_events(
                popup_window, event, values, 'nodes',
                enabled_events=['remove', 'clear'])

            if event in ('nodes.remove', 'nodes.clear'):
                popup_window['node_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NodeEnum
                        if x.display_name not in popup_window['nodes'].Values],
                    set_to_index=None)

            LayoutBase.update_widgets(popup_window)
