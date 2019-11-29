from util.logger import Log
from tkinter import TclError


class LogMsgLine(object):
    """For pretty-printing colorful message logs into the GUI logger window.
    Color-support ticket:
    https://github.com/PySimpleGUI/PySimpleGUI/issues/1664
    """

    @classmethod
    def print_to_logger(cls, window, key, message, log_type=None):
        cls._pprint_log(window, key, message, log_type)

    @staticmethod
    def _pprint_log(window, key, log, log_type=None):
        embedded_type = None
        if log.startswith(Log.CLR_MSG):
            embedded_type = 'msg'
            log = log[len(Log.CLR_MSG):].replace(Log.CLR_END, '')
        elif log.startswith(Log.CLR_SUCCESS):
            embedded_type = 'success'
            log = log[len(Log.CLR_SUCCESS):].replace(Log.CLR_END, '')
        elif log.startswith(Log.CLR_WARNING):
            embedded_type = 'warning'
            log = log[len(Log.CLR_WARNING):].replace(Log.CLR_END, '')
        elif log.startswith(Log.CLR_ERROR):
            embedded_type = 'error'
            log = log[len(Log.CLR_ERROR):].replace(Log.CLR_END, '')

        # the log from kcauto already has newlines, but they result in double
        # newlines when c&p'ed from the GUI logger window. So, strip any
        # newlines and maunally insert them below when pushing into the window
        # element for display.
        log = log.rstrip()
        log_type = log_type if log_type else embedded_type

        txt = window[key].Widget
        try:
            if log_type == 'msg':
                txt.tag_config(log_type, foreground='skyblue')
                txt.insert('end', log + "\n", log_type)
                window[key].Update('', append=True)
            elif log_type == 'success':
                txt.tag_config(log_type, foreground='lightgreen')
                txt.insert('end', log + "\n", log_type)
                window[key].Update('', append=True)
            elif log_type == 'warning':
                txt.tag_config(log_type, foreground='orange')
                txt.insert('end', log + "\n", log_type)
                window[key].Update('', append=True)
            elif log_type == 'error':
                txt.tag_config(log_type, foreground='red')
                txt.insert('end', log + "\n", log_type)
                window[key].Update('', append=True)
            else:
                txt.tag_config('info', foreground='whitesmoke')
                txt.insert('end', log + "\n", 'info')
                window[key].Update('', append=True)
        except TclError:
            # catch invalid command name error when closing GUI
            pass
