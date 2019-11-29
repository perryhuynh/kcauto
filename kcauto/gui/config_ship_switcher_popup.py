import PySimpleGUI as sg
from gui.layout_base import LayoutBase

from kca_enums.damage_states import DamageStateEnum
from kca_enums.ship_types import ShipTypeEnum
from kca_enums.ship_switcher_slots import (
    ShipSwitcherConditionSlot0Enum, ShipSwitcherCriteriaSlot0Enum,
    ShipSwitcherCriteriaSlot8Enum, ShipSwitcherCriteriaSlot9Enum,
    ShipSwitcherOperatorEnum)


class ConfigShipSwitcherPopupLayout(LayoutBase):
    MIN_LEVEL = 1
    MAX_LEVEL = 155
    DEF_LEVEL = 50
    MIN_MORALE = 0
    MAX_MORALE = 100
    DEF_MORALE = 50
    MIN_SHIP_ID = 1
    MAX_SHIP_ID = 2000
    DEF_SHIP_ID = 1

    @classmethod
    def get_layout(cls, slot_id, parent_value):
        cond, crit = cls.unpack_rule_string(parent_value)
        COND_SLOT2_LEVEL_COL = [
            [
                sg.Spin(
                    [x for x in range(cls.MIN_LEVEL, cls.MAX_LEVEL + 1)],
                    cls.DEF_LEVEL,
                    key='cond_slot2_level',
                    font=cls.FONT_10,
                    size=(2, 1)),
            ]
        ]
        COND_SLOT2_DAMAGE_COL = [
            [
                sg.Combo(
                    [x.display_name for x in DamageStateEnum if x.value > -1],
                    key='cond_slot2_damage',
                    font=cls.FONT_10,
                    size=(15, 1)),
            ]
        ]
        COND_SLOT2_MORALE_COL = [
            [
                sg.Spin(
                    [x for x in range(cls.MIN_MORALE, cls.MAX_MORALE + 1)],
                    cls.DEF_MORALE,
                    key='cond_slot2_morale',
                    font=cls.FONT_10,
                    size=(2, 1)),
            ]
        ]
        CRIT_SLOT1_SHIP_COL = [
            [
                sg.Text('ID:', font=cls.FONT_10),
                sg.Spin(
                    [x for x in range(
                        cls.MIN_SHIP_ID,
                        cls.MAX_SHIP_ID + 1)],
                    cls.DEF_SHIP_ID,
                    key='crit_slot1_ship',
                    font=cls.FONT_10,
                    size=(4, 1)),
            ]
        ]
        CRIT_SLOT1_CLASS_COL = [
            [
                sg.Combo(
                    [x.display_name for x in ShipTypeEnum if x.value != 0],
                    key='crit_slot1_class',
                    font=cls.FONT_10,
                    size=(15, 1)),
            ]
        ]
        return [
            [
                sg.Text(f'Slot {slot_id} Rule', font=cls.FONT_10),
            ],
            [
                sg.InputText(
                    parent_value,
                    key='rule',
                    font=cls.FONT_10,
                    size=(60, 1),
                    disabled=True),
            ],
            [
                sg.Text('Switch-Out Conditions', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='conditions',
                    values=cond,
                    font=cls.FONT_10,
                    size=(60, 3),
                    enable_events=True),
            ],
            [
                sg.Combo(
                    [x.display_name for x in ShipSwitcherConditionSlot0Enum],
                    key='cond_slot0',
                    font=cls.FONT_10,
                    size=(10, 1)),
                sg.Text('  ', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in ShipSwitcherOperatorEnum],
                    default_value=ShipSwitcherOperatorEnum.GT.value,
                    key='cond_slot1',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Column(
                    COND_SLOT2_LEVEL_COL,
                    key='cond_slot2_level_col',
                    visible=False),
                sg.Column(
                    COND_SLOT2_DAMAGE_COL,
                    key='cond_slot2_damage_col',
                    visible=False),
                sg.Column(
                    COND_SLOT2_MORALE_COL,
                    key='cond_slot2_morale_col',
                    visible=False),
            ],
            [
                cls.generate_add_btn('conditions', 'add new condition'),
                cls.generate_update_btn(
                    'conditions', 'update selected condition'),
                cls.generate_remove_btn(
                    'conditions', 'remove selected condition'),
            ],
            [
                sg.Text('Switch-In Criteria', font=cls.FONT_10),
            ],
            [
                sg.Listbox(
                    key='criteria',
                    values=crit,
                    font=cls.FONT_10,
                    size=(60, 3),
                    enable_events=True),
            ],
            [
                sg.Combo(
                    [x.display_name for x in ShipSwitcherCriteriaSlot0Enum],
                    key='crit_slot0',
                    font=cls.FONT_10,
                    size=(5, 1)),
                sg.Column(
                    CRIT_SLOT1_SHIP_COL,
                    key='crit_slot1_ship_col',
                    visible=False),
                sg.Column(
                    CRIT_SLOT1_CLASS_COL,
                    key='crit_slot1_class_col',
                    visible=False),
            ],
            [
                sg.Text('Level:', font=cls.FONT_10),
                sg.Combo(
                    [''] + [x.display_name for x in ShipSwitcherOperatorEnum],
                    key='crit_slot2',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Spin(
                    [x for x in range(cls.MIN_LEVEL, cls.MAX_LEVEL + 1)],
                    cls.DEF_LEVEL,
                    key='crit_slot3',
                    font=cls.FONT_10,
                    size=(3, 1)),
                sg.Text('  Damage:', font=cls.FONT_10),
                sg.Combo(
                    [''] + [x.display_name for x in ShipSwitcherOperatorEnum],
                    key='crit_slot4',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Combo(
                    [x.display_name for x in DamageStateEnum if x.value > -1],
                    key='crit_slot5',
                    font=cls.FONT_10,
                    size=(10, 1)),
                sg.Text('  Morale:', font=cls.FONT_10),
                sg.Combo(
                    [''] + [x.display_name for x in ShipSwitcherOperatorEnum],
                    key='crit_slot6',
                    font=cls.FONT_10,
                    size=(2, 1)),
                sg.Spin(
                    [x for x in range(cls.MIN_MORALE, cls.MAX_MORALE + 1)],
                    cls.DEF_MORALE,
                    key='crit_slot7',
                    font=cls.FONT_10,
                    size=(3, 1)),
            ],
            [
                sg.Text('Locked:', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in ShipSwitcherCriteriaSlot8Enum],
                    key='crit_slot8',
                    font=cls.FONT_10,
                    size=(10, 1)),
                sg.Text('  Ringed:', font=cls.FONT_10),
                sg.Combo(
                    [x.display_name for x in ShipSwitcherCriteriaSlot9Enum],
                    key='crit_slot9',
                    font=cls.FONT_10,
                    size=(10, 1)),
            ],
            [
                cls.generate_add_btn('criteria', 'add new criteria'),
                cls.generate_update_btn(
                    'criteria', 'update selected criteria'),
                cls.generate_remove_btn(
                    'criteria', 'remove selected criteria'),
            ],
            [
                sg.Button('Save and Close', key='save'),
                sg.Button('Cancel', key='cancel')
            ]
        ]

    @classmethod
    def generate_rule_string(cls, window):
        conditions = ','.join(window['conditions'].Values)
        criteria = ','.join(window['criteria'].Values)
        window['rule'].Update(f'{conditions}|{criteria}')

    @classmethod
    def unpack_rule_string(cls, value):
        rule_split = value.split('|')
        if len(rule_split) == 2:
            conditions = rule_split[0].split(',')
            criteria = rule_split[1].split(',')
            return (conditions, criteria)
        return ([], [])

    @classmethod
    def generate_condition_string(cls, values):
        rule_list = [''] * 3
        rule_list[0] = ShipSwitcherConditionSlot0Enum.display_name_to_value(
            values['cond_slot0'])
        rule_list[1] = values['cond_slot1']
        if rule_list[0] is ShipSwitcherConditionSlot0Enum.LEVEL.value:
            rule_list[2] = str(values['cond_slot2_level'])
        elif rule_list[0] is ShipSwitcherConditionSlot0Enum.DAMAGE.value:
            rule_list[2] = str(DamageStateEnum.display_name_to_value(
                values['cond_slot2_damage']))
        elif rule_list[0] is ShipSwitcherConditionSlot0Enum.MORALE.value:
            rule_list[2] = str(values['cond_slot2_morale'])
        return ':'.join(rule_list)

    @classmethod
    def unpack_condition_string(cls, window, rule):
        rule_split = rule.split(':')
        window['cond_slot0'].Update(
            ShipSwitcherConditionSlot0Enum(rule_split[0]).display_name)
        window['cond_slot1'].Update(rule_split[1])
        if rule_split[0] == ShipSwitcherConditionSlot0Enum.LEVEL.value:
            window['cond_slot2_level'].Update(int(rule_split[2]))
        elif rule_split[0] == ShipSwitcherConditionSlot0Enum.DAMAGE.value:
            window['cond_slot2_damage'].Update(
                DamageStateEnum(int(rule_split[2])).display_name)
        elif rule_split[0] == ShipSwitcherConditionSlot0Enum.MORALE.value:
            window['cond_slot2_morale'].Update(int(rule_split[2]))

    @classmethod
    def generate_criterion_string(cls, values):
        rule_list = [''] * 10
        rule_list[0] = ShipSwitcherCriteriaSlot0Enum.display_name_to_value(
            values['crit_slot0'])
        if rule_list[0] is ShipSwitcherCriteriaSlot0Enum.SHIP.value:
            rule_list[1] = str(values['crit_slot1_ship'])
        elif rule_list[0] is ShipSwitcherCriteriaSlot0Enum.CLASS.value:
            rule_list[1] = str(ShipTypeEnum.display_name_to_value(
                values['crit_slot1_class']))
        rule_list[2] = values['crit_slot2']
        rule_list[3] = str(values['crit_slot3']) if rule_list[2] else ''
        rule_list[4] = values['crit_slot4']
        rule_list[5] = (
            str(DamageStateEnum.display_name_to_value(values['crit_slot5']))
            if rule_list[4]
            else '')
        rule_list[6] = values['crit_slot6']
        rule_list[7] = str(values['crit_slot7']) if rule_list[6] else ''
        rule_list[8] = ShipSwitcherCriteriaSlot8Enum.display_name_to_value(
            values['crit_slot8'])
        rule_list[9] = ShipSwitcherCriteriaSlot9Enum.display_name_to_value(
            values['crit_slot9'])
        return ':'.join(rule_list)

    @classmethod
    def unpack_criterion_string(cls, window, rule):
        rule_split = rule.split(':')
        window['crit_slot0'].Update(
            ShipSwitcherCriteriaSlot0Enum(rule_split[0]).display_name)
        if rule_split[0] == ShipSwitcherCriteriaSlot0Enum.SHIP.value:
            window['crit_slot1_ship'].Update(int(rule_split[1]))
        elif rule_split[0] == ShipSwitcherCriteriaSlot0Enum.CLASS.value:
            window['crit_slot1_class'].Update(
                ShipTypeEnum(int(rule_split[1])).display_name)
        window['crit_slot2'].Update(rule_split[2])
        if rule_split[2]:
            window['crit_slot3'].Update(int(rule_split[3]))
        else:
            window['crit_slot3'].Update('')
        window['crit_slot4'].Update(rule_split[4])
        if rule_split[4]:
            window['crit_slot5'].Update(
                DamageStateEnum(int(rule_split[5])).display_name)
        window['crit_slot6'].Update(rule_split[6])
        if rule_split[6]:
            window['crit_slot7'].Update(int(rule_split[7]))
        else:
            window['crit_slot7'].Update('')
        window['crit_slot8'].Update(
            ShipSwitcherCriteriaSlot8Enum(rule_split[8]).display_name)
        window['crit_slot9'].Update(
            ShipSwitcherCriteriaSlot9Enum(rule_split[9]).display_name)

    @classmethod
    def update_gui(cls, slot_id, parent_value):
        parent_value_backup = str(parent_value)
        popup_window = sg.Window(
            f'Ship Switcher Slot {slot_id} Config',
            cls.get_layout(slot_id, parent_value),
            use_default_focus=parent_value,
            element_padding=(0, (0, 3)))

        while True:
            event, values = popup_window.Read(timeout=100)

            if event in (None, 'save'):
                popup_window.Close()
                return popup_window['rule'].Get()

            if event == 'cancel':
                popup_window.Close()
                return parent_value_backup

            cls.check_listbox_related_events(
                popup_window, event, values, 'conditions',
                value_generator=cls.generate_condition_string,
                value_unpacker=cls.unpack_condition_string,
                enabled_events=['add', 'update', 'remove', 'unpack'])
            cls.check_listbox_related_events(
                popup_window, event, values, 'criteria',
                value_generator=cls.generate_criterion_string,
                value_unpacker=cls.unpack_criterion_string,
                enabled_events=['add', 'update', 'remove', 'unpack'])

            if (
                    len(popup_window['conditions'].Values) > 0
                    and len(popup_window['criteria'].Values) > 0):
                cls.generate_rule_string(popup_window)
            else:
                popup_window['rule'].Update('')

            if (
                    values['cond_slot0']
                    == ShipSwitcherConditionSlot0Enum.LEVEL.display_name):
                popup_window['cond_slot2_level_col'].Update(visible=True)
                popup_window['cond_slot2_damage_col'].Update(visible=False)
                popup_window['cond_slot2_morale_col'].Update(visible=False)
            elif (
                    values['cond_slot0']
                    == ShipSwitcherConditionSlot0Enum.DAMAGE.display_name):
                popup_window['cond_slot2_level_col'].Update(visible=False)
                popup_window['cond_slot2_damage_col'].Update(visible=True)
                popup_window['cond_slot2_morale_col'].Update(visible=False)
            elif (
                    values['cond_slot0']
                    == ShipSwitcherConditionSlot0Enum.MORALE.display_name):
                popup_window['cond_slot2_level_col'].Update(visible=False)
                popup_window['cond_slot2_damage_col'].Update(visible=False)
                popup_window['cond_slot2_morale_col'].Update(visible=True)

            if (
                    values['crit_slot0']
                    == ShipSwitcherCriteriaSlot0Enum.SHIP.display_name):
                popup_window['crit_slot1_ship_col'].Update(visible=True)
                popup_window['crit_slot1_class_col'].Update(visible=False)
            else:
                popup_window['crit_slot1_ship_col'].Update(visible=False)
                popup_window['crit_slot1_class_col'].Update(visible=True)

            if values['crit_slot2']:
                popup_window['crit_slot3'].Update(disabled=False)
            else:
                popup_window['crit_slot3'].Update(disabled=True)
            if values['crit_slot4']:
                popup_window['crit_slot5'].Update(disabled=False)
            else:
                popup_window['crit_slot5'].Update(disabled=True)
            if values['crit_slot6']:
                popup_window['crit_slot7'].Update(disabled=False)
            else:
                popup_window['crit_slot7'].Update(disabled=True)

            cls.correct_to_value_range(
                popup_window, values, 'cond_slot2_level', cls.MIN_LEVEL,
                cls.MAX_LEVEL, cls.DEF_LEVEL)
            cls.correct_to_value_range(
                popup_window, values, 'cond_slot2_morale', cls.MIN_MORALE,
                cls.MAX_MORALE, cls.DEF_MORALE)
            cls.correct_to_value_range(
                popup_window, values, 'crit_slot1_ship', cls.MIN_SHIP_ID,
                cls.MAX_SHIP_ID, cls.DEF_SHIP_ID)
            cls.correct_to_value_range(
                popup_window, values, 'crit_slot3', cls.MIN_LEVEL,
                cls.MAX_LEVEL, cls.DEF_LEVEL)
            cls.correct_to_value_range(
                popup_window, values, 'crit_slot7', cls.MIN_MORALE,
                cls.MAX_MORALE, cls.DEF_MORALE)

            LayoutBase.update_widgets(popup_window)
