import PySimpleGUI as sg

from gui.layout_base import LayoutBase


class ConfigTabButtonsLayout(LayoutBase):
    CONFIG_GROUP_LIST = (
        "general", "expedition", "pvp", "combat", "event reset",
        "ship switcher", "passive repair", "quest", "scheduler")
    BREAK_POSITION = 5

    @classmethod
    def get_layout(cls):
        buttons = [
            cls.generate_tab_btn(
                'config', grp, cls.key_suffix_generator(grp), cls.FONT_9, idx,
                pad=((1, 0), (1, 0)))
            for idx, grp in enumerate(cls.CONFIG_GROUP_LIST)
        ]
        return sg.Column(
            [buttons[:cls.BREAK_POSITION], buttons[cls.BREAK_POSITION:]],
            pad=(0, (10, 5)),
            element_justification='center',
            justification='center'
        )

    @staticmethod
    def key_suffix_generator(label):
        return label.replace(' ', '_').lower()

    @classmethod
    def update_gui(cls, window, event, values):
        if event.startswith('tab_config_'):
            event_key = event.replace('tab_config_', '')
            other_keys = [
                cls.key_suffix_generator(grp)
                for grp in cls.CONFIG_GROUP_LIST
                if event_key != cls.key_suffix_generator(grp)]

            window[f'tab_config_{event_key}'].Widget.configure(
                fg=cls.COLORS_TAB_BUTTON_ACTIVE[0],
                bg=cls.COLORS_TAB_BUTTON_ACTIVE[1])
            window[f'config_{event_key}_col'].Update(visible=True)
            for k in other_keys:
                window[f'config_{k}_col'].Update(visible=False)
                window[f'tab_config_{k}'].Widget.configure(
                    fg=cls.COLORS_TAB_BUTTON[0], bg=cls.COLORS_TAB_BUTTON[1])
