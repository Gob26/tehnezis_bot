

from core.entities.models import CrawlingTarget
from core.entities.schemas import CrawlingTargetCreate
from sqlalchemy.ext.asyncio import AsyncSession

class CrawlingTargetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, target: CrawlingTargetCreate) -> CrawlingTarget:
        new_target = CrawlingTarget(
            title=target.title,
            url=str(target.url),
            xpath=target.xpath,
            price=target.price
        )

        self.session.add(new_target)
        await self.session.commit()
        await self.session.refresh(new_target)

        return new_target
    
    async def create_many(self, targets: list[CrawlingTargetCreate]) -> list[CrawlingTarget]:
        new_targets = [CrawlingTarget(
            title=target.title,
            url=str(target.url),
            xpath=target.xpath,
            price=target.price
        ) for target in targets]

        self.session.add_all(new_targets)
        await self.session.commit()

        return new_targets