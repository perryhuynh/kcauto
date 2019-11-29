import PySimpleGUI as sg
from gui.layout_base import LayoutBase

from kca_enums.scheduler_slots import (
    SchedulerSlot0Enum, SchedulerSlot2Enum, SchedulerSlot3Enum)


class ConfigSchedulerPopupLayout(LayoutBase):
    MIN_TIME_HOURS = 0
    MAX_TIME_HOURS = 23
    MIN_TIME_LIMIT_HOURS = 0
    MAX_TIME_LIMIT_HOURS = 99
    MIN_MINUTES = 0
    MAX_MINUTES = 59

    @classmethod
    def get_layout(cls, values):
        SLOT1_TIME_COL = [
            [
                sg.Text('at ', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_TIME_HOURS,
                        cls.MAX_TIME_HOURS + 1)],
                    2,
                    key='slot1_time_1',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Text(':', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_MINUTES,
                        cls.MAX_MINUTES + 1)],
                    30,
                    key='slot1_time_2',
                    font=cls.FONT_10,
                    size=(2, 1)),
            ]
        ]
        SLOT1_TIME_RUN_COL = [
            [
                sg.Text('after ', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_TIME_LIMIT_HOURS,
                        cls.MAX_TIME_LIMIT_HOURS + 1)],
                    20,
                    key='slot1_time_run_1',
                    font=cls.FONT_10,
                    size=(4, 1)),
                sg.Text('hrs:', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_MINUTES,
                        cls.MAX_MINUTES + 1)],
                    0,
                    key='slot1_time_run_2',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Text('mins (max 99hrs:59mins)', font=cls.FONT_10),
            ]
        ]
        SLOT1_RUNS_COL = [
            [
                sg.Spin(
                    [x for x in range(0, 9999)],
                    1,
                    key='slot1_runs',
                    font=cls.FONT_10,
                    size=(5, 1)),
                sg.Text(' runs', font=cls.FONT_10),
            ]
        ]
        SLOT1_RESCUE_COL = [
            [
                sg.Text('ship ID ', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(0, 9999)],
                    1,
                    key='slot1_rescue',
                    font=cls.FONT_10,
                    size=(5, 1)),
            ]
        ]
        SLOT4_COL = [
            [
                sg.Text('for ', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_TIME_LIMIT_HOURS,
                        cls.MAX_TIME_LIMIT_HOURS + 1)],
                    4,
                    key='slot4_1',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Text('hr:', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_MINUTES,
                        cls.MAX_MINUTES + 1)],
                    30,
                    key='slot4_2',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Text('mins (max 99hrs:59mins)', font=cls.FONT_10),
            ]
        ]
        return [
            [
                sg.Listbox(
                    key='rules',
                    values=values,
                    font=cls.FONT_10,
                    size=(70, 5),
                    enable_events=True)
            ],
            [
                sg.Text('Condition: ', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in SchedulerSlot0Enum],
                    key='slot0',
                    font=cls.FONT_10,
                    size=(15, 1)),
                sg.Column(SLOT1_TIME_COL, key='slot1_time_col', visible=False),
                sg.Column(
                    SLOT1_TIME_RUN_COL,
                    key='slot1_time_run_col',
                    visible=False),
                sg.Column(SLOT1_RUNS_COL, key='slot1_runs_col', visible=False),
                sg.Column(
                    SLOT1_RESCUE_COL,
                    key='slot1_rescue_col',
                    visible=False),
            ],
            [
                sg.Text('Action: ', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in SchedulerSlot2Enum],
                    key='slot2',
                    font=cls.FONT_10,
                    size=(5, 1)),
                sg.Combo(
                    [x.display_name for x in SchedulerSlot3Enum],
                    key='slot3',
                    font=cls.FONT_10,
                    size=(8, 1)),
                sg.Column(SLOT4_COL, key='slot4_col')
            ],
            [
                cls.generate_add_btn('rules', label='Add New Rule'),
                cls.generate_update_btn('rules', label='Update Selected Rule'),
                cls.generate_remove_btn('rules', label='Remove Selected Rule'),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel')
            ]
        ]

    @classmethod
    def generate_rule_string(cls, values):
        rule_list = [''] * 5
        rule_list[0] = SchedulerSlot0Enum.display_name_to_value(
            values['slot0'])
        if rule_list[0] == SchedulerSlot0Enum.TIME.value:
            rule_list[1] = (
                f"{int(values['slot1_time_1']):02}"
                f"{int(values['slot1_time_2']):02}")
        elif rule_list[0] == SchedulerSlot0Enum.TIME_RUN.value:
            rule_list[1] = (
                f"{int(values['slot1_time_run_1']):02}"
                f"{int(values['slot1_time_run_2']):02}")
        elif rule_list[0] in (
                SchedulerSlot0Enum.SORTIES_RUN.value,
                SchedulerSlot0Enum.EXPEDITIONS_RUN.value,
                SchedulerSlot0Enum.PVP_RUN.value):
            rule_list[1] = str(values['slot1_runs'])
        elif rule_list[0] == SchedulerSlot0Enum.RESCUE.value:
            rule_list[1] = str(values['slot1_rescue'])
        rule_list[2] = SchedulerSlot2Enum.display_name_to_value(
            values['slot2'])
        rule_list[3] = SchedulerSlot3Enum.display_name_to_value(
            values['slot3'])
        if rule_list[2] == SchedulerSlot2Enum.SLEEP.value:
            rule_list[4] = (
                f"{int(values['slot4_1']):02}{int(values['slot4_2']):02}")
        return ':'.join(rule_list)

    @classmethod
    def unpack_rule_string(cls, window, rule):
        rule_split = rule.split(':')
        window['slot0'].Update(SchedulerSlot0Enum(rule_split[0]).display_name)
        if rule_split[0] == SchedulerSlot0Enum.TIME.value:
            window['slot1_time_1'].Update(int(rule_split[1][0:2]))
            window['slot1_time_2'].Update(int(rule_split[1][2:4]))
        elif rule_split[0] == SchedulerSlot0Enum.TIME_RUN.value:
            window['slot1_time_run_1'].Update(int(rule_split[1][0:2]))
            window['slot1_time_run_2'].Update(int(rule_split[1][2:4]))
        elif rule_split[0] in (
                SchedulerSlot0Enum.SORTIES_RUN.value,
                SchedulerSlot0Enum.EXPEDITIONS_RUN.value,
                SchedulerSlot0Enum.PVP_RUN.value):
            window['slot1_runs'].Update(int(rule_split[1]))
        elif rule_split[0] == SchedulerSlot0Enum.RESCUE.value:
            window['slot1_rescue'].Update(int(rule_split[1]))
        window['slot2'].Update(SchedulerSlot2Enum(rule_split[2]).display_name)
        window['slot3'].Update(SchedulerSlot3Enum(rule_split[3]).display_name)
        if rule_split[2] == SchedulerSlot2Enum.SLEEP.value:
            window['slot4_1'].Update(int(rule_split[4][0:2]))
            window['slot4_2'].Update(int(rule_split[4][2:4]))

    @classmethod
    def update_gui(cls, parent_values):
        parent_values_backup = list(parent_values)
        popup_window = sg.Window(
            'Scheduler Config',
            cls.get_layout(parent_values),
            use_default_focus=False,
            element_padding=(0, (0, 3)))
        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return popup_window['rules'].Values

            if event == 'cancel':
                popup_window.Close()
                return parent_values_backup

            cls.check_listbox_related_events(
                popup_window, event, values, 'rules',
                value_generator=cls.generate_rule_string,
                value_unpacker=cls.unpack_rule_string,
                enabled_events=['add', 'update', 'remove', 'unpack'])

            if values['slot0'] == SchedulerSlot0Enum.TIME.display_name:
                popup_window['slot1_time_col'].Update(visible=True)
                popup_window['slot1_time_run_col'].Update(visible=False)
                popup_window['slot1_runs_col'].Update(visible=False)
                popup_window['slot1_rescue_col'].Update(visible=False)
            elif values['slot0'] == SchedulerSlot0Enum.TIME_RUN.display_name:
                popup_window['slot1_time_col'].Update(visible=False)
                popup_window['slot1_time_run_col'].Update(visible=True)
                popup_window['slot1_runs_col'].Update(visible=False)
                popup_window['slot1_rescue_col'].Update(visible=False)
            elif values['slot0'] in (
                    SchedulerSlot0Enum.SORTIES_RUN.display_name,
                    SchedulerSlot0Enum.EXPEDITIONS_RUN.display_name,
                    SchedulerSlot0Enum.PVP_RUN.display_name):
                popup_window['slot1_time_col'].Update(visible=False)
                popup_window['slot1_time_run_col'].Update(visible=False)
                popup_window['slot1_runs_col'].Update(visible=True)
                popup_window['slot1_rescue_col'].Update(visible=False)
            elif values['slot0'] == SchedulerSlot0Enum.RESCUE.display_name:
                popup_window['slot1_time_col'].Update(visible=False)
                popup_window['slot1_time_run_col'].Update(visible=False)
                popup_window['slot1_runs_col'].Update(visible=False)
                popup_window['slot1_rescue_col'].Update(visible=True)
            else:
                popup_window['slot1_time_col'].Update(visible=False)
                popup_window['slot1_time_run_col'].Update(visible=False)
                popup_window['slot1_runs_col'].Update(visible=False)
                popup_window['slot1_rescue_col'].Update(visible=False)

            if values['slot2'] == SchedulerSlot2Enum.SLEEP.display_name:
                popup_window['slot4_col'].Update(visible=True)
            else:
                popup_window['slot4_col'].Update(visible=False)

            cls.correct_to_value_range(
                popup_window, values, 'slot1_time_1', cls.MIN_TIME_HOURS,
                cls.MAX_TIME_HOURS, 0)
            cls.correct_to_value_range(
                popup_window, values, 'slot1_time_2', cls.MIN_MINUTES,
                cls.MAX_MINUTES, 0)
            cls.correct_to_value_range(
                popup_window, values, 'slot1_time_run_1',
                cls.MIN_TIME_LIMIT_HOURS, cls.MAX_TIME_LIMIT_HOURS, 0)
            cls.correct_to_value_range(
                popup_window, values, 'slot1_time_run_2', cls.MIN_MINUTES,
                cls.MAX_MINUTES, 0)
            cls.correct_to_value_range(
                popup_window, values, 'slot4_1', cls.MIN_TIME_LIMIT_HOURS,
                cls.MAX_TIME_LIMIT_HOURS, 0)
            cls.correct_to_value_range(
                popup_window, values, 'slot4_2', cls.MIN_MINUTES,
                cls.MAX_MINUTES, 0)

            LayoutBase.update_widgets(popup_window)
