from gui.layout_base import LayoutBase


class GuiTabButtonsLayout(LayoutBase):
    GUI_TAB_LIST = ("config", "log", "click plot", "settings", "about")

    @classmethod
    def get_layout(cls):
        return [
            cls.generate_tab_btn(
                'gui', tab, cls.key_suffix_generator(tab), cls.FONT_10, idx)
            for idx, tab in enumerate(cls.GUI_TAB_LIST)
        ]

    @staticmethod
    def key_suffix_generator(label):
        return label.replace(' ', '_').lower()

    @classmethod
    def switch_to_tab(cls, window, tab):
        other_tabs = [
            cls.key_suffix_generator(grp)
            for grp in cls.GUI_TAB_LIST
            if tab != cls.key_suffix_generator(grp)]
        window[f'gui_tab_{tab}'].Update(visible=True)
        window[f'tab_gui_{tab}'].Widget.configure(
            fg=cls.COLORS_TAB_BUTTON_ACTIVE[0],
            bg=cls.COLORS_TAB_BUTTON_ACTIVE[1])
        for k in other_tabs:
            window[f'gui_tab_{k}'].Update(visible=False)
            window[f'tab_gui_{k}'].Widget.configure(
                fg=cls.COLORS_TAB_BUTTON[0], bg=cls.COLORS_TAB_BUTTON[1])

    @classmethod
    def update_gui(cls, window, event, values):
        if event.startswith('tab_gui_'):
            event_key = event.replace('tab_gui_', '')
            other_keys = [
                cls.key_suffix_generator(grp)
                for grp in cls.GUI_TAB_LIST
                if event_key != cls.key_suffix_generator(grp)]

            window[f'gui_tab_{event_key}'].Update(visible=True)
            window[f'tab_gui_{event_key}'].Widget.configure(
                fg=cls.COLORS_TAB_BUTTON_ACTIVE[0],
                bg=cls.COLORS_TAB_BUTTON_ACTIVE[1])
            for k in other_keys:
                window[f'gui_tab_{k}'].Update(visible=False)
                window[f'tab_gui_{k}'].Widget.configure(
                    fg=cls.COLORS_TAB_BUTTON[0], bg=cls.COLORS_TAB_BUTTON[1])
