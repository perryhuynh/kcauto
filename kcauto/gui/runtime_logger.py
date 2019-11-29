import PySimpleGUI as sg
import queue
import subprocess
from tkinter import TclError

from gui.layout_base import LayoutBase
from gui.log_msg_line import LogMsgLine
from util.logger import Log


class RuntimeLogger(LayoutBase):
    new_termination = False

    @classmethod
    def get_layout(cls):
        return sg.Column(
            [
                [
                    sg.Multiline(
                        key='logger',
                        font=('Courier New', 9),
                        autoscroll=True,
                        size=(92, 34),
                        pad=(0, (15, 0)),
                        background_color='grey20',
                        disabled=False)],
                [
                    cls.generate_clear_btn('logger')
                ]
            ],
            key='gui_tab_log',
            size=cls.PRIMARY_COL_TAB_SIZE,
            visible=False
        )

    @classmethod
    def run_command(cls, cmd):
        cls.new_termination = True
        return subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    @classmethod
    def terminate(cls, window, proc, thread):
        terminated = False
        if proc:
            terminated = True
            proc.terminate()
        if thread:
            terminated = True
            thread.join()
        if terminated:
            try:
                window.TKroot.unbind('<Escape>')
            except TclError:
                # catch bad window path name error when closing GUI
                pass
            if cls.new_termination:
                cls.new_termination = False
                LogMsgLine.print_to_logger(
                    window, 'logger',
                    Log._log_format("Terminated kcauto subprocess via GUI."),
                    log_type='warning')

    @staticmethod
    def output_reader(proc, gui_queue):
        for line in iter(proc.stdout.readline, b''):
            new_l = '{0}'.format(line.decode('utf-8'))
            gui_queue.put(new_l)

    @staticmethod
    def process_queue(window, kcauto_proc, gui_queue):
        try:
            kcauto_proc_poll = kcauto_proc.poll()
            message = gui_queue.get_nowait()
            while message:
                LogMsgLine.print_to_logger(window, 'logger', message)
                message = gui_queue.get_nowait()
        except queue.Empty:
            message = None
        return kcauto_proc_poll

    @classmethod
    def update_gui(cls, window, event, values):
        LIMIT = 500
        num_lines = int(float(window['logger'].Widget.index('end-1c')))
        if num_lines > LIMIT:
            diff = num_lines - LIMIT
            window['logger'].Widget.delete('1.0', f'{diff}.0')
        if event == 'logger.clear':
            window['logger'].Update('')
