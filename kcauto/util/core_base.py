from abc import ABC
from datetime import datetime

import config.config_core as cfg
import nav.nav as nav
from util.logger import Log


class CoreBase(ABC):
    """kcauto module core base class.
    """
    _enabled = False
    module_name = ''
    module_display_name = ''
    time_disabled = None

    def __init__(self):
        self.update_from_config()

    def update_from_config(self):
        """Method that enables or disables the module based on the config.
        """
        module_cfg = getattr(cfg.config, self.module_name)
        enabled = module_cfg.enabled
        update = True if enabled != self.enabled else False
        if update:
            self.enabled = enabled

    def goto(self):
        """Method that navigates to the module's page using the nav module.
        """
        nav.navigate.to(self.module_name)

    @property
    def enabled(self):
        """Indicates whether or not the module is enabled.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise TypeError(
                f"Enabled setting for module {self.module_display_name} "
                "is not a bool.")
        if value is True:
            Log.log_success(f"{self.module_display_name} module enabled.")
            self.time_disabled = None
        else:
            Log.log_warn(f"{self.module_display_name} module disabled")
            self.time_disabled = datetime.now()
        self._enabled = value
