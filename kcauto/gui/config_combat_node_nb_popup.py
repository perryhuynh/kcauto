import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.nodes import NamedNodeEnum


class ConfigCombatNodeNBPopupLayout(LayoutBase):
    @classmethod
    def get_layout(cls, node_nb):
        return [
            [
                sg.Text('Node Night Battles', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='node_nb',
                    values=node_nb,
                    font=cls.FONT_10,
                    size=(28, 6),
                    enable_events=True),
            ],
            [
                cls.generate_remove_btn('node_nb', 'remove node night battle'),
                cls.generate_clear_btn('node_nb', 'clear node night battles'),
            ],
            [
                sg.Combo(
                    [
                        x.display_name for x in NamedNodeEnum
                        if x.display_name
                        not in [y.split(':')[0] for y in node_nb]],
                    key='node_combo',
                    font=cls.FONT_10,
                    size=(4, 1)),
                sg.Text(' to ', font=cls.FONT_10),
                sg.Combo(
                    [True, False],
                    key='nb_combo',
                    font=cls.FONT_10,
                    size=(5, 1)),
                cls.generate_add_btn('node_nb', 'add', size=(5, 1)),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel'),
            ]
        ]

    @classmethod
    def update_gui(cls, node_nb):
        node_nb_backup = str(node_nb)
        node_nb = node_nb.split(',')
        while '' in node_nb:
            node_nb.remove('')

        popup_window = sg.Window(
            'Node Selects',
            cls.get_layout(node_nb),
            use_default_focus=False,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return ','.join(popup_window['node_nb'].Values)

            if event == 'cancel':
                popup_window.Close()
                return node_nb_backup

            if event == 'node_nb.add':
                lb_values = popup_window['node_nb'].Values
                lb_values.append(
                    f"{values['node_combo']}:{values['nb_combo']}")
                popup_window['node_nb'].Update(values=lb_values)
                popup_window['node_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NamedNodeEnum
                        if x.display_name not in [
                            y.split(':')[0] for y in lb_values]],
                    set_to_index=None)

            cls.check_listbox_related_events(
                popup_window, event, values, 'node_nb',
                enabled_events=['remove', 'clear'])

            if event in ('node_nb.remove', 'node_nb.clear'):
                popup_window['node_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NamedNodeEnum
                        if x.display_name not in [
                            y.split(':')[0]
                            for y in popup_window['node_nb'].Values]],
                    set_to_index=None)

            LayoutBase.update_widgets(popup_window)
