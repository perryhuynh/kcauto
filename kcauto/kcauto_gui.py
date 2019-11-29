import PySimpleGUI as sg
import queue
import subprocess
import threading

from gui.about import About
from gui.click_plotter import ClickPlotter
from gui.config import Config
from gui.config_controls import ConfigControls
from gui.gui_tab_buttons import GuiTabButtonsLayout
from gui.kcauto_controls import KcautoControls
from gui.layout_base import LayoutBase
from gui.runtime_logger import RuntimeLogger
from gui.settings import Settings
from util.logger import Log


def gui_main():
    """Primary method for composing and initializing the kcauto GUI.
    """
    Log.log_success("Starting kcauto GUI.")

    layout = [
        GuiTabButtonsLayout.get_layout(),
        [
            Config.get_layout(),
            RuntimeLogger.get_layout(),
            ClickPlotter.get_layout(),
            Settings.get_layout(),
            About.get_layout(),
        ],
        ConfigControls.get_layout(),
        KcautoControls.get_layout(),
    ]

    # initialize window
    window = sg.Window(
        'kcauto',
        layout,
        use_default_focus=False,
        element_padding=(0, 0),
        margins=(3, 7),
        debugger_enabled=False,
        finalize=True)

    # initialize misc values
    secondary_event = None
    kcauto_proc = None
    kcauto_proc_poll = None
    proc_reader = None
    gui_queue = queue.Queue()
    timeout = None

    # load default config and refresh UI
    event, values = window.read(timeout=100)
    init_cfg_path = window['cfg_path'].Get()
    cfg_load(window, event, values, init_cfg_path)
    event, values = window.read(timeout=100)
    update_gui(window, event, values)

    while True:
        # primary loop
        event, values = window.read(timeout=timeout)

        if event != '__TIMEOUT__':
            # print(event)
            pass

        if event in (None, 'Cancel', ):
            break

        if event == 'save':
            ConfigControls.save_cfg(values['cfg_path'], window, values)

        if event == 'save_cfg_path':
            new_cfg = values['save_cfg_path']
            if new_cfg:
                window['cfg_path'].Update(new_cfg)
                ConfigControls.update_cfg_filename(window, new_cfg)
                ConfigControls.save_cfg(new_cfg, window, values)

        if event == 'load_cfg_path':
            new_cfg = values['load_cfg_path']
            if new_cfg:
                cfg_load(window, event, values, new_cfg)
                secondary_event = 'load'
                event, values = window.read(timeout=100)

        if event == 'run_chrome':
            if values['gui.chrome_path'] and values['general.chrome_dev_port']:
                chrome_cmd_list = [
                    values['gui.chrome_path'],
                    '--remote-debugging-port=' + str(
                        values['general.chrome_dev_port'])
                ]
                Log.log_msg(f"Running chrome: {' '.join(chrome_cmd_list)}")
                subprocess.run(chrome_cmd_list)

        if event == 'run_kcauto':
            timeout = 150
            # automatically switch to log tab
            GuiTabButtonsLayout.switch_to_tab(window, 'log')

            # generate run command for kcauto
            run_cmd_list = values['gui.python_command'].split(' ')
            run_cmd_list.extend([
                'kcauto', '--cli', '--cfg-path', window['cfg_path'].Get()])
            if not values['gui.track_clicks']:
                run_cmd_list.append('--no-click-track')
            if values['gui.debug_output']:
                run_cmd_list.append('--debug-output')

            # run kcauto
            Log.log_msg(f"Running kcauto: {' '.join(run_cmd_list)}")
            kcauto_proc = RuntimeLogger.run_command(run_cmd_list)
            proc_reader = threading.Thread(
                target=RuntimeLogger.output_reader,
                args=(kcauto_proc, gui_queue))
            proc_reader.start()
            window['run_kcauto'].Update(disabled=True)
            window['stop_kcauto'].Update(
                disabled=False,
                button_color=LayoutBase.COLORS_ALERT_BUTTON)
            window.TKroot.bind(
                '<Escape>',
                lambda e, w=window, k=kcauto_proc, p=proc_reader: esc_bind(
                    e, w, k, p))

        if kcauto_proc and proc_reader:
            # process messages from kcauto to logger
            kcauto_proc_poll = (
                RuntimeLogger.process_queue(window, kcauto_proc, gui_queue))

        if event == 'stop_kcauto' or kcauto_proc_poll is not None:
            RuntimeLogger.terminate(window, kcauto_proc, proc_reader)
            window['run_kcauto'].Update(disabled=False)
            window['stop_kcauto'].Update(
                disabled=True,
                button_color=LayoutBase.COLORS_ALERT_BUTTON_DISABLED)
            kcauto_proc_poll = None
            timeout = None

        update_gui(window, event, values)

        if secondary_event == 'load':
            window['scheduler.rules'].Update(window['scheduler.rules'].Values)
            secondary_event = None

    RuntimeLogger.terminate(window, kcauto_proc, proc_reader)
    window.close()
    Log.log_success("Shutting down kcauto GUI.")


def cfg_load(window, event, values, cfg):
    """Method that loads an existing config file and propagtes it to the UI.
    """
    window['cfg_path'].Update(cfg)
    ConfigControls.update_cfg_filename(window, cfg)
    ConfigControls.load_cfg(cfg, window, event, values)


def update_gui(window, event, values):
    """Wrapper method that calls the various update_gui methods.
    """
    KcautoControls.update_gui(window, event, values)
    GuiTabButtonsLayout.update_gui(window, event, values)
    Config.update_gui(window, event, values)
    RuntimeLogger.update_gui(window, event, values)
    ClickPlotter.update_gui(window, event, values)
    Settings.update_gui(window, event, values)
    About.update_gui(window, event, values)
    # for tkinter-level modifications
    LayoutBase.update_widgets(window)


def esc_bind(event, window, kcauto_proc, proc_reader):
    """Method that allows user to hit the [Esc] key to stop kcauto.
    """
    RuntimeLogger.terminate(window, kcauto_proc, proc_reader)
