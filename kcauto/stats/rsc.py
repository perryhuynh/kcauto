from stats.stats_base import StatsBase
from util.logger import Log


class ResourceStats(StatsBase):
    _fuel_start = None
    _ammo_start = None
    _steel_start = None
    _bauxite_start = None
    _bucket_start = None
    _fuel = None
    _ammo = None
    _steel = None
    _bauxite = None
    _bucket = None

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Resource Stats module initialized.")

    def update_resource_stats(self, data):
        Log.log_debug("Updating resource data from API.")
        for rsc in data:
            if rsc['api_id'] == 1:
                self.fuel = rsc['api_value']
            if rsc['api_id'] == 2:
                self.ammo = rsc['api_value']
            if rsc['api_id'] == 3:
                self.steel = rsc['api_value']
            if rsc['api_id'] == 4:
                self.bauxite = rsc['api_value']
            if rsc['api_id'] == 6:
                self.bucket = rsc['api_value']

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        if not self._fuel_start:
            self._fuel_start = value
        self._fuel = value

    @property
    def fuel_delta(self):
        return self._fuel - self._fuel_start

    @property
    def fuel_ph(self):
        return self.fuel_delta / self.hours_run

    @property
    def ammo(self):
        return self._ammo

    @ammo.setter
    def ammo(self, value):
        if not self._ammo_start:
            self._ammo_start = value
        self._ammo = value

    @property
    def ammo_delta(self):
        return self._ammo - self._ammo_start

    @property
    def ammo_ph(self):
        return self.ammo_delta / self.hours_run

    @property
    def steel(self):
        return self._steel

    @steel.setter
    def steel(self, value):
        if not self._steel_start:
            self._steel_start = value
        self._steel = value

    @property
    def steel_delta(self):
        return self._steel - self._steel_start

    @property
    def steel_ph(self):
        return self.steel_delta / self.hours_run

    @property
    def bauxite(self):
        return self._bauxite

    @bauxite.setter
    def bauxite(self, value):
        if not self._bauxite_start:
            self._bauxite_start = value
        self._bauxite = value

    @property
    def bauxite_delta(self):
        return self._bauxite - self._bauxite_start

    @property
    def bauxite_ph(self):
        return self.bauxite_delta / self.hours_run

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        if not self._bucket_start:
            self._bucket_start = value
        self._bucket = value

    @property
    def bucket_delta(self):
        return self._bucket - self._bucket_start

    @property
    def bucket_ph(self):
        return self.bucket_delta / self.hours_run

    def __str__(self):
        return (
            f"Fuel:{self.fuel} "
            f"(Δ{self.fuel_delta} : {self.fuel_ph:.2f}/hr) / "
            f"Ammo:{self.ammo} "
            f"(Δ{self.ammo_delta} : {self.ammo_ph:.2f}/hr) / "
            f"Steel:{self.steel} "
            f"(Δ{self.steel_delta} : {self.steel_ph:.2f}/hr) / "
            f"Bauxite:{self.bauxite} "
            f"(Δ{self.bauxite_delta} : {self.bauxite_ph:.2f}/hr) / "
            f"Bucket:{self.bucket} "
            f"(Δ{self.bucket_delta} : {self.bucket_ph:.2f}/hr)")
