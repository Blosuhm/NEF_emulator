from typing import List

import httpx

from app.core.config import QoSProfile
from app.interfaces.afSessionWithQos import AfSessionWithQosInterface
from app.models.UE import UE
from app.schemas.afSessionWithQos import AsSessionWithQoSSubscription


class TfsAfSessionWithQos(AfSessionWithQosInterface):

    def __init__(
        self,
        tfs_url: str,
    ) -> None:
        self._client = httpx.AsyncClient(base_url=tfs_url + "/tfs-api/device")
        self.device_id = ""

    def _craft_payload(self, uplink, downlink):
        payload = {
            "name": "mac",
            "device_id": {"device_uuid": {"uuid": self.device_id}},
            "device_config": {
                "config_rules": [
                    {
                        "action": "CONFIGACTION_SET",
                        "acl": {
                            "endpoint_id": {
                                "topology_id": {
                                    "context_id": {
                                        "context_uuid": {
                                            "uuid": "43813baf-195e-5da6-af20-b3d0922e71a7"
                                        }
                                    }
                                },
                                "device_id": {"device_uuid": {"uuid": self.device_id}},
                                "endpoint_uuid": {"uuid": "eth0-endpoint-uuid"},
                            },
                            "direction": "ACLDIRECTION_BOTH",
                            "rule_set": {
                                "name": "RATS 1",
                                "type": "ACLRULETYPE_IPV4",
                                "entries": [
                                    {
                                        "match": {
                                            "src_port": downlink,
                                            "dst_port": uplink,
                                        },
                                        "action": {
                                            "forward_action": "ACLFORWARDINGACTION_DROP",
                                            "log_action": "ACLLOGACTION_NOLOG",
                                        },
                                    }
                                ],
                            },
                        },
                    }
                ]
            },
        }

        return payload

    async def change_qos(
        self, subscription: AsSessionWithQoSSubscription, ues: List[UE], qos: QoSProfile
    ) -> None:
        payload = self._craft_payload(qos.uplinkBitRate, qos.downlinkBitRate)
        self._client.post(self.device_id, json=payload)

    async def revert_qos(
        self, subscription: AsSessionWithQoSSubscription, ues: List[UE]
    ) -> None:
        payload = self._craft_payload(0, 0)
        self._client.post(self.device_id, json=payload)
