from abc import ABC
import PySimpleGUI as sg


class LayoutBase(ABC):
    PRIMARY_COL_TAB_SIZE = (680, 580)
    SIZE_BTN = (None, None)
    FONT_8 = ('Helvetica', 8)
    FONT_9 = ('Helvetica', 9)
    FONT_10 = ('Helvetica', 10)
    FONT_12 = ('Helvetica', 12)
    COLORS_TAB_BUTTON = ('black', 'white')
    COLORS_TAB_BUTTON_ACTIVE = ('white', '#082567')
    COLORS_STANDARD_BUTTON = ('black', 'white')
    COLORS_ACTIVE_BUTTON = ('white', 'blue')
    COLORS_ALERT_BUTTON = ('white', 'red')
    COLORS_ALERT_BUTTON_DISABLED = ('white', 'darkred')
    COLOR_DISABLED_BG = '#f0f0f0'
    PAD_LABEL = ((0, 5), (4, 4))
    PAD_BUTTON_CONTROLS = ((1, 0), 0)

    LABEL_SETTINGS = {
        'font': FONT_10,
        'justification': 'right',
        'size': (16, 1),
        'pad': PAD_LABEL
    }

    @classmethod
    def generate_tab_btn(
            cls, tab_group, label, key_suffix, font, idx,
            pad=PAD_BUTTON_CONTROLS):
        return sg.Button(
            label,
            key=f'tab_{tab_group}_{key_suffix}',
            font=font,
            button_color=(
                cls.COLORS_TAB_BUTTON_ACTIVE
                if idx == 0
                else cls.COLORS_TAB_BUTTON),
            pad=pad)

    @classmethod
    def generate_edit_btn(cls, key_prefix, label='edit', size=SIZE_BTN):
        return sg.Button(
            label,
            key=f'{key_prefix}.edit',
            size=size,
            font=cls.FONT_8,
            button_color=cls.COLORS_STANDARD_BUTTON)

    @classmethod
    def generate_add_btn(cls, key_prefix, label='add', size=SIZE_BTN):
        return sg.Button(
            label,
            key=f'{key_prefix}.add',
            size=size,
            font=cls.FONT_8,
            pad=cls.PAD_BUTTON_CONTROLS,
            button_color=cls.COLORS_STANDARD_BUTTON)

    @classmethod
    def generate_update_btn(cls, key_prefix, label='update', size=SIZE_BTN):
        return sg.Button(
            label,
            key=f'{key_prefix}.update',
            size=size,
            font=cls.FONT_8,
            pad=cls.PAD_BUTTON_CONTROLS,
            button_color=cls.COLORS_STANDARD_BUTTON)

    @classmethod
    def generate_remove_btn(cls, key_prefix, label='remove', size=SIZE_BTN):
        return sg.Button(
            label,
            key=f'{key_prefix}.remove',
            size=size,
            font=cls.FONT_8,
            pad=cls.PAD_BUTTON_CONTROLS,
            button_color=cls.COLORS_STANDARD_BUTTON)

    @classmethod
    def generate_clear_btn(cls, key_prefix, label='clear', size=SIZE_BTN):
        return sg.Button(
            label,
            key=f'{key_prefix}.clear',
            size=size,
            font=cls.FONT_8,
            pad=cls.PAD_BUTTON_CONTROLS,
            button_color=cls.COLORS_STANDARD_BUTTON)

    @staticmethod
    def update_window_elements_with_prefix(window, prefix, parameters):
        for element in window.AllKeysDict:
            if element.startswith(prefix):
                window[element].Update(**parameters)

    @staticmethod
    def update_window_elements(window, elements, parameters):
        for element in elements:
            window[element].Update(**parameters)

    @staticmethod
    def check_popup_related_events(
            window, event, values, key, popup_layout,
            enabled_events=['edit', 'clear']):
        if event == f'{key}.edit' and 'edit' in enabled_events:
            window.Hide()
            new_values = popup_layout.update_gui(values[key])
            window[key].Update(new_values)
            window.UnHide()
        if event == f'{key}.clear' and 'clear' in enabled_events:
            window[key].Update('')

    @staticmethod
    def check_listbox_related_events(
            window, event, values, key,
            value_generator=None, value_unpacker=None,
            enabled_events=['add', 'update', 'remove', 'unpack', 'clear']):
        if 'add' in enabled_events or 'update' in enabled_events:
            if value_generator is None:
                raise ValueError("value_generator not defined.")
        if 'unpack' in enabled_events:
            if value_unpacker is None:
                raise ValueError("value_unpacker not defined.")

        cur = window[key].Widget.curselection()

        if event == f'{key}.add' and 'add' in enabled_events:
            new_value = value_generator(values)
            lb_values = window[key].Values
            lb_values.append(new_value)
            window[key].Update(values=lb_values)
        if event == f'{key}.update' and 'update' in enabled_events:
            new_value = value_generator(values)
            lb_values = window[key].Values
            lb_values[cur[0]] = new_value
            window[key].Update(values=lb_values, set_to_index=cur[0])
        if event == f'{key}.remove' and 'remove' in enabled_events:
            lb_values = window[key].Values
            del lb_values[cur[0]]
            window[key].Update(values=lb_values)
        if event == f'{key}.clear' and 'clear' in enabled_events:
            window[key].Update(values=[])
        if event == key:
            if len(cur) > 0 and 'unpack' in enabled_events:
                value_unpacker(window, window[key].Values[cur[0]])

        if len(cur) > 0:
            if 'update' in enabled_events:
                window[f'{key}.update'].Update(disabled=False)
            if 'remove' in enabled_events:
                window[f'{key}.remove'].Update(disabled=False)
        else:
            if 'update' in enabled_events:
                window[f'{key}.update'].Update(disabled=True)
            if 'remove' in enabled_events:
                window[f'{key}.remove'].Update(disabled=True)

        if len(window[key].Values) > 0:
            if 'clear' in enabled_events:
                window[f'{key}.clear'].Update(disabled=False)
        else:
            if 'clear' in enabled_events:
                window[f'{key}.clear'].Update(disabled=True)

    @staticmethod
    def correct_to_value_range(
            window, values, key, min_val, max_val, default_val):
        if values[key] in (None, ''):
            window[key].Update(default_val)
        elif int(values[key]) < min_val:
            window[key].Update(min_val)
        elif int(values[key]) > max_val:
            window[key].Update(max_val)

    @staticmethod
    def update_widgets(window):
        for element in window.AllKeysDict:
            if isinstance(window[element], sg.Button):
                window[element].Widget.configure(relief='flat')
            if isinstance(window[element], sg.Combo):
                window[element].Widget.state(['readonly'])
            if element.startswith('link_'):
                window[element].Widget.configure(cursor='hand2')
