import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from kca_enums.nodes import NodeEnum
from kca_enums.formations import FormationEnum


class ConfigCombatNodeFormationPopupLayout(LayoutBase):
    @classmethod
    def get_layout(cls, node_formations):
        return [
            [
                sg.Text('Node Formations', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='node_formations',
                    values=node_formations,
                    font=cls.FONT_10,
                    size=(32, 6),
                    enable_events=True),
            ],
            [
                cls.generate_remove_btn(
                    'node_formations', 'remove node formation'),
                cls.generate_clear_btn(
                    'node_formations', 'clear node formations'),
            ],
            [
                sg.Combo(
                    [
                        x.display_name for x in NodeEnum
                        if x.display_name
                        not in [y.split(':')[0] for y in node_formations]],
                    key='node_combo',
                    font=cls.FONT_10,
                    size=(4, 1)),
                sg.Text(' to ', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in FormationEnum],
                    key='formation_combo',
                    font=cls.FONT_10,
                    size=(15, 1)),
                cls.generate_add_btn('node_formations', 'add', size=(5, 1)),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel'),
            ]
        ]

    @classmethod
    def update_gui(cls, node_formations):
        node_formations_backup = str(node_formations)
        node_formations = node_formations.split(',')
        while '' in node_formations:
            node_formations.remove('')

        popup_window = sg.Window(
            'Node Selects',
            cls.get_layout(node_formations),
            use_default_focus=False,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return ','.join(popup_window['node_formations'].Values)

            if event == 'cancel':
                popup_window.Close()
                return node_formations_backup

            if event == 'node_formations.add':
                lb_values = popup_window['node_formations'].Values
                formation_value = FormationEnum.display_name_to_value(
                    values['formation_combo'])
                lb_values.append(f"{values['node_combo']}:{formation_value}")
                popup_window['node_formations'].Update(values=lb_values)
                popup_window['node_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NodeEnum
                        if x.display_name not in [
                            y.split(':')[0] for y in lb_values]],
                    set_to_index=None)

            cls.check_listbox_related_events(
                popup_window, event, values, 'node_formations',
                enabled_events=['remove', 'clear'])

            if event in ('node_formations.remove', 'node_formations.clear'):
                popup_window['node_combo'].Update(
                    value=None,
                    values=[
                        x.display_name for x in NodeEnum
                        if x.display_name not in [
                            y.split(':')[0]
                            for y in popup_window['node_formations'].Values]],
                    set_to_index=None)

            LayoutBase.update_widgets(popup_window)
