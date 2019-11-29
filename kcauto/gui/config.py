import PySimpleGUI as sg

from gui.layout_base import LayoutBase
from gui.config_general import ConfigGeneralLayout
from gui.config_expedition import ConfigExpeditionLayout
from gui.config_pvp import ConfigPvPLayout
from gui.config_combat import ConfigCombatLayout
from gui.config_event_reset import ConfigEventResetLayout
from gui.config_ship_switcher import ConfigShipSwitcherLayout
from gui.config_passive_repair import ConfigPassiveRepairLayout
from gui.config_quest import ConfigQuestLayout
from gui.config_scheduler import ConfigSchedulerLayout
from gui.config_tab_buttons import ConfigTabButtonsLayout


class Config(LayoutBase):
    new_termination = False

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Column([[]], size=(cls.PRIMARY_COL_TAB_SIZE[0], 1))
                ],
                [
                    ConfigTabButtonsLayout.get_layout(),
                ],
                [
                    sg.Column([[
                        ConfigGeneralLayout.get_layout(),
                        ConfigExpeditionLayout.get_layout(),
                        ConfigPvPLayout.get_layout(),
                        ConfigCombatLayout.get_layout(),
                        ConfigEventResetLayout.get_layout(),
                        ConfigShipSwitcherLayout.get_layout(),
                        ConfigPassiveRepairLayout.get_layout(),
                        ConfigQuestLayout.get_layout(),
                        ConfigSchedulerLayout.get_layout()
                        ]],
                        justification='center')
                ],
            ],
            key='gui_tab_config',
            size=cls.PRIMARY_COL_TAB_SIZE,
            element_justification='center',
            justification='center',
        )

    @classmethod
    def update_gui(cls, window, event, values):
        ConfigTabButtonsLayout.update_gui(window, event, values)
        ConfigGeneralLayout.update_gui(window, event, values)
        ConfigExpeditionLayout.update_gui(window, event, values)
        ConfigPvPLayout.update_gui(window, event, values)
        ConfigCombatLayout.update_gui(window, event, values)
        ConfigEventResetLayout.update_gui(window, event, values)
        ConfigShipSwitcherLayout.update_gui(window, event, values)
        ConfigPassiveRepairLayout.update_gui(window, event, values)
        ConfigQuestLayout.update_gui(window, event, values)
        ConfigSchedulerLayout.update_gui(window, event, values)
