import subprocess
import re
from logging import Logger
from subprocess import CompletedProcess

from retry import retry

from chia.utils import ChiaUtils


class FarmKeys:

    name = 'chia_keys'

    def __init__(self):

        self._farm_key = "Not set"

    @property
    def farm_key(self):
        return self._farm_key

    @farm_key.setter
    def farm_key(self, value):
        self._farm_key = value


class FarmStatus:

    name = 'chia_farm'

    def __init__(self):

        self._status = 0
        self._plot_size = "0 GiB"
        self._plot_size_in_bytes = 0
        self._plot_count = 0
        self._network_size = "0 GiB"
        self._network_size_in_bytes = 0
        self._network_share = "0.0%"
        self._time_to_win = "Infinity"
        self._total_farmed = 0
        self._block_rewards = 0
        self._transaction_fees = 0
        self._last_height = 0

    @property
    def status(self) -> int:
        if self._status == "Farming":
            return 1

        return 0

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def plot_size(self):
        return self._plot_size

    @plot_size.setter
    def plot_size(self, value):
        self._plot_size = value
        self._plot_size_in_bytes = ChiaUtils.size_in_bytes(value)

        if self._network_size_in_bytes > 0 and self._plot_size_in_bytes > 0:
            perc = self._plot_size_in_bytes / self._network_size_in_bytes
            self._network_share = "{:.4%}".format(perc)

    @property
    def plot_count(self):
        return self._plot_count

    @plot_count.setter
    def plot_count(self, value):
        self._plot_count = value

    @property
    def network_size(self):
        return self._network_size

    @network_size.setter
    def network_size(self, value):
        self._network_size = value
        self._network_size_in_bytes = ChiaUtils.size_in_bytes(value)

        if self._network_size_in_bytes > 0 and self._plot_size_in_bytes > 0:
            perc = self._plot_size_in_bytes / self._network_size_in_bytes
            self._network_share = "{:.4%}".format(perc)

    @property
    def network_share(self):
        return self._network_share

    @property
    def time_to_win(self):
        return self._time_to_win

    @time_to_win.setter
    def time_to_win(self, value):
        self._time_to_win = value

    @property
    def total_farmed(self):
        return self._total_farmed

    @total_farmed.setter
    def total_farmed(self, value):
        self._total_farmed = value

    @property
    def block_rewards(self):
        return self._block_rewards

    @block_rewards.setter
    def block_rewards(self, value):
        self._block_rewards = value

    @property
    def transaction_fees(self):
        return self._transaction_fees

    @transaction_fees.setter
    def transaction_fees(self, value):
        self._transaction_fees = value

    @property
    def last_height(self):
        return self._last_height

    @last_height.setter
    def last_height(self, value):
        self._last_height = value

    @property
    def attributes(self) -> dict:

        return {
            'farmingStatus': self.status,
            'totalChiaFarmed': self.total_farmed,
            'userTransactionFees': self.transaction_fees,
            'blockRewards': self.block_rewards,
            'lastHeightFarmed': self.last_height,
            'plotCount': self.plot_count,
            'totalSizeOfPlots': ChiaUtils.size_in_gbytes(self.plot_size),
        }


class ChiaStatus:

    _logger = None

    def set_logger(self, logger: Logger):
        self._logger = logger

    @retry(delay=1, backoff=2, tries=3, logger=_logger)
    def keys(self) -> FarmKeys:
        result: CompletedProcess = subprocess.run(
            ['chia', 'keys', 'show'], check=True, stdout=subprocess.PIPE, universal_newlines=True
        )

        lines = result.stdout.splitlines()
        keys = FarmKeys()

        for line in lines:

            farmer = re.search(r'^Farmer public key \((.*?)\): (.*)', line)
            if farmer:
                self._logger.debug("Found Farmer Key: {}".format(farmer.group(2)))
                keys.farm_key = farmer.group(2)

        return keys

    @retry(delay=1, backoff=2, tries=3, logger=_logger)
    def farm(self) -> FarmStatus:
        result: CompletedProcess = subprocess.run(
            ['chia', 'farm', 'summary'], check=True, stdout=subprocess.PIPE, universal_newlines=True
        )

        lines = result.stdout.splitlines()
        farm = FarmStatus()
        self._logger.debug("Farm Status: {}".format(result.stdout))

        for line in lines:

            status = re.search(r'^Farming status: (.*)', line)
            if status:
                self._logger.debug("Found Farm Status: {}".format(status.group(1)))
                farm.status = status.group(1)

            total_farmed = re.search(r'^Total chia farmed: (.*)', line)
            if total_farmed:
                self._logger.debug("Found Total Farmed: {}".format(total_farmed.group(1)))
                farm.total_farmed = float(total_farmed.group(1))

            block_rewards = re.search(r'^Block rewards: (.*)', line)
            if block_rewards:
                self._logger.debug("Found Block Rewards: {}".format(block_rewards.group(1)))
                farm.block_rewards = float(block_rewards.group(1))

            last_height = re.search(r'^Last height farmed: (\w+)', line)
            if last_height:
                self._logger.debug("Found Last Height: {}".format(last_height.group(1)))
                farm.last_height = int(last_height.group(1))

            time_to_win = re.search(r'^Expected time to win: (.*)', line)
            if time_to_win:
                self._logger.debug("Found Time To Win: {}".format(time_to_win.group(1)))
                farm.time_to_win = time_to_win.group(1)

            plot_count = re.search(r'^Plot count: (\w+)', line)
            if plot_count:
                self._logger.debug("Found Plot Count: {}".format(plot_count.group(1)))
                farm.plot_count = int(plot_count.group(1))

            plot_size = re.search(r'^Total size of plots: (.*)', line)
            if plot_size:
                self._logger.debug("Found Plot Size: {}".format(plot_size.group(1)))
                farm.plot_size = plot_size.group(1)

            network_size = re.search(r'^Estimated network space: (.*)', line)
            if network_size:
                self._logger.debug("Found Network Size: {}".format(network_size.group(1)))
                farm.network_size = network_size.group(1)

            transaction_fees = re.search(r'^User transaction fees: (.*)', line)
            if transaction_fees:
                self._logger.debug("Found Transaction Fees: {}".format(transaction_fees.group(1)))
                farm.transaction_fees = transaction_fees.group(1)

        return farm
