import os
from typing import Annotated

from fastapi import Depends

from app.core.config import QoSInterfaceBackend, settings
from app.interfaces.afSessionWithQos import AfSessionWithQosInterface

if settings.qos.backend == QoSInterfaceBackend.HUWAEI:
    from .huawei import HuaweiAfSessionWithQos

    _interface = HuaweiAfSessionWithQos(
        settings.qos.api_url,
        settings.qos.default_ambrup,
        settings.qos.default_ambrdl,
        settings.qos.api_user,
        settings.qos.api_password,
    )

elif settings.qos.backend == QoSInterfaceBackend.TFS:
    from .tfs import TfsAfSessionWithQos

    _interface = TfsAfSessionWithQos(settings.qos.api_url)
else:
    from .noop import NoopAfSessionWithQos

    _interface = NoopAfSessionWithQos()


async def get_interface() -> AfSessionWithQosInterface:
    return _interface


AfSessionWithQosDep = Annotated[AfSessionWithQosInterface, Depends(get_interface)]
