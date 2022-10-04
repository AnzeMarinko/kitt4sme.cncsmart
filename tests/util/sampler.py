import time

from fipy.ngsi.entity import TextAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
import random
from typing import Optional

from cncsmart.ngsy import PartProgramEntity
from tests.util.fiware import orion_client


class MachineSampler(DevicePoolSampler):

    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())

    def new_device_entity(self) -> PartProgramEntity:
        seed = random.randint(0, 5)
        return PartProgramEntity(
            id='',
            file_name=TextAttr.new(f"{seed}_samples.json"),
            json_data=TextAttr.new("[" + ", ".join(["{sample: 1}"] * seed) + "]")
        )

    def sample(self, samples_n: int, sampling_rate: float):
        """Send `sample_n` batches of readings to Orion every `sampling_rate`
        seconds.
        Each batch contains an NGSI entity for each device in the pool.
        """
        for _ in range(samples_n):
            xs = [self.make_device_entity(nid)
                  for nid in range(1, self._device_n + 1)]
            self._orion.upsert_entities(xs)

            time.sleep(sampling_rate)
