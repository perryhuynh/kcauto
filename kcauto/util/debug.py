from pyvisauto import Region

from util.logger import Log


class Debug(object):
    """kcauto debug module.
    """
    @staticmethod
    def find_all(asset, similarity):
        region = Region()

        Log.log_warn(f"Searching for {asset} with similarity {similarity}.")
        Log.log_warn("Results:")
        results = region.find_all(asset, similarity)
        for result in results:
            print(result)


debug = Debug()
