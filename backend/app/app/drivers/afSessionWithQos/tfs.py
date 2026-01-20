from typing import List

import httpx

from app.core.config import QoSProfile
from app.interfaces.afSessionWithQos import AfSessionWithQosInterface
from app.models.UE import UE
from app.schemas.afSessionWithQos import AsSessionWithQoSSubscription


class TfsAfSessionWithQos(AfSessionWithQosInterface):
    async def change_qos(
        self, subscription: AsSessionWithQoSSubscription, ues: List[UE], qos: QoSProfile
    ) -> None:
        pass

    async def revert_qos(
        self, subscription: AsSessionWithQoSSubscription, ues: List[UE]
    ) -> None:
        pass
