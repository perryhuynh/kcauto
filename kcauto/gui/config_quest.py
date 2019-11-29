import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from util.json_data import JsonData


class ConfigQuestLayout(LayoutBase):
    FONT = ('Helvetica', 8)
    CELL_WIDTH = 124
    SIZE_FIRST_COL = (8, 1)
    SIZE_FIRST_ROW = (20, 1)
    SIZE_COMBAT_CELL = (CELL_WIDTH, 140)
    SIZE_PVP_CELL = (CELL_WIDTH, 30)
    SIZE_EXPEDITION_CELL = (CELL_WIDTH, 55)
    SIZE_SUPPLY_CELL = (CELL_WIDTH, 30)
    LABEL_FIRST_COL_SETTINGS = {
        'font': FONT,
        'justification': 'right',
        'size': SIZE_FIRST_COL
    }
    LABEL_FIRST_ROW_SETTINGS = {
        'element_justification': 'center',
        'size': (CELL_WIDTH, 30)
    }
    LABEL_FIRST_ROW_CBOX_SETTINGS = {
        'font': FONT,
        'pad': ((10, 0), (3, 0)),
        'size': (10, 1),
        'enable_events': True
    }
    COMBAT_CELL_SETTINGS = {
        'element_justification': 'center',
        'size': SIZE_COMBAT_CELL
    }
    PVP_CELL_SETTINGS = {
        'element_justification': 'center',
        'size': SIZE_PVP_CELL
    }
    EXPEDITION_CELL_SETTINGS = {
        'element_justification': 'center',
        'size': SIZE_EXPEDITION_CELL
    }
    SUPPLY_CELL_SETTINGS = {
        'element_justification': 'center',
        'size': SIZE_SUPPLY_CELL
    }
    QUESTS_PER_LINE = 2

    @classmethod
    def generate_quest_checkboxes(cls, quests):
        qlist = [[]]
        for idx, q in enumerate(quests):
            qlist[-1].append(sg.Checkbox(
                q,
                key=f'quest_c.q.{q}',
                font=cls.FONT,
                enable_events=True
            ))
            if (idx + 1) % cls.QUESTS_PER_LINE == 0:
                qlist.append([])
        return qlist

    @classmethod
    def get_layout(cls):
        quest_layout = cls._calc_quest_layout()
        return sg.Column(
            [
                [
                    sg.Text('Quest Module', **cls.LABEL_SETTINGS),
                    sg.Checkbox(
                        'Enabled', key='quest.enabled', enable_events=True)
                ],
                [
                    sg.Text('Enabled Quests', **cls.LABEL_SETTINGS),
                    sg.Multiline(
                        '',
                        key='quest.quests',
                        font=cls.FONT_10,
                        size=(30, 3),
                        background_color='#f0f0f0',
                        disabled=True),
                    cls.generate_clear_btn('quest.quests')
                ],
                [
                    sg.Text('', **cls.LABEL_FIRST_COL_SETTINGS),
                    sg.Column([[
                        sg.Checkbox(
                            'Daily',
                            key='quest_c.c.daily',
                            **cls.LABEL_FIRST_ROW_CBOX_SETTINGS)
                    ]], **cls.LABEL_FIRST_ROW_SETTINGS),
                    sg.Column([[
                        sg.Checkbox(
                            'Weekly',
                            key='quest_c.c.weekly',
                            **cls.LABEL_FIRST_ROW_CBOX_SETTINGS)
                    ]], **cls.LABEL_FIRST_ROW_SETTINGS),
                    sg.Column([[
                        sg.Checkbox(
                            'Monthly',
                            key='quest_c.c.monthly',
                            **cls.LABEL_FIRST_ROW_CBOX_SETTINGS)
                    ]], **cls.LABEL_FIRST_ROW_SETTINGS),
                    sg.Column([[
                        sg.Checkbox(
                            'Other',
                            key='quest_c.c.other',
                            **cls.LABEL_FIRST_ROW_CBOX_SETTINGS)
                    ]], **cls.LABEL_FIRST_ROW_SETTINGS)
                ],
                [
                    sg.Text('Combat', **cls.LABEL_FIRST_COL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['B'].get('daily', [])),
                        **cls.COMBAT_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['B'].get('weekly', [])),
                        **cls.COMBAT_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['B'].get('monthly', [])),
                        **cls.COMBAT_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['B'].get('other', [])),
                        **cls.COMBAT_CELL_SETTINGS),
                ],
                [
                    sg.Text('PvP', **cls.LABEL_FIRST_COL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['C'].get('daily', [])),
                        **cls.PVP_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['C'].get('weekly', [])),
                        **cls.PVP_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['C'].get('monthly', [])),
                        **cls.PVP_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['C'].get('other', [])),
                        **cls.PVP_CELL_SETTINGS),
                ],
                [
                    sg.Text('Expedition', **cls.LABEL_FIRST_COL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['D'].get('daily', [])),
                        **cls.EXPEDITION_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['D'].get('weekly', [])),
                        **cls.EXPEDITION_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['D'].get('monthly', [])),
                        **cls.EXPEDITION_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['D'].get('other', [])),
                        **cls.EXPEDITION_CELL_SETTINGS),
                ],
                [
                    sg.Text('Supply', **cls.LABEL_FIRST_COL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['E'].get('daily', [])),
                        **cls.SUPPLY_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['E'].get('weekly', [])),
                        **cls.SUPPLY_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['E'].get('monthly', [])),
                        **cls.SUPPLY_CELL_SETTINGS),
                    sg.Column(
                        cls.generate_quest_checkboxes(
                            quest_layout['E'].get('other', [])),
                        **cls.SUPPLY_CELL_SETTINGS),
                ]
            ],
            key='config_quest_col',
            visible=False)

    @classmethod
    def _calc_quest_layout(cls):
        quest_data = JsonData.load_json('data|quests|quests.json')
        quest_layout = {}
        for quest_name in quest_data:
            quest = quest_data[quest_name]
            quest['name'] = quest_name
            if quest['name'][0] not in quest_layout:
                quest_layout[quest['name'][0]] = {}
            if quest['type'] not in quest_layout[quest['name'][0]]:
                quest_layout[quest['name'][0]][quest['type']] = [quest['name']]
            else:
                quest_layout[quest['name'][0]][quest['type']].append(
                    quest['name'])
        return quest_layout

    @staticmethod
    def _unpack_quests(window, quests):
        if not quests:
            return
        for quest in quests:
            if quest:
                window[f'quest_c.q.{quest}'].Update(True)

    @classmethod
    def update_gui(cls, window, event, values):
        elements = ('quest.quests.clear', )

        if event.startswith('quest_c.c.'):
            state = window[event].Get()
            event_key = event.replace('quest_c.c.', '')
            quest_layout = cls._calc_quest_layout()
            for qg in quest_layout:
                if event_key in quest_layout[qg]:
                    for q in quest_layout[qg][event_key]:
                        window[f'quest_c.q.{q}'].Update(state)

        if event.startswith('quest_c.'):
            enabled_quests = []
            for element in window.AllKeysDict:
                if element.startswith('quest_c.q.') and window[element].Get():
                    element_key = element.replace('quest_c.q.', '')
                    enabled_quests.append(element_key)
            window['quest.quests'].Update(','.join(enabled_quests))

        if event == 'quest.quests.clear':
            window['quest.quests'].Update('')
            for element in window.AllKeysDict:
                if element.startswith('quest_c.'):
                    window[element].Update(False)

        if values['quest.enabled'] is True:
            cls.update_window_elements(window, elements, {'disabled': False})
            cls.update_window_elements_with_prefix(
                window, 'quest_c.', {'disabled': False})
        else:
            cls.update_window_elements(window, elements, {'disabled': True})
            cls.update_window_elements_with_prefix(
                window, 'quest_c.', {'disabled': True})

        cls._unpack_quests(
            window, window['quest.quests'].Get().strip().split(','))
