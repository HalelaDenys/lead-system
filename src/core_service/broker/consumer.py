from core_service.dto.lead_dto import LeadDataKeyDTO, CreateLeadDTO
from core_service.schemas.lead_schema import LeadQueueMessage
from core_service.service.lead_service import LeadService
from core_service.repo.lead_repo import LeadRepo
from core_service.container import container
from infrastructure import broker, db_helper
from faststream import FastStream, Logger

app = FastStream(broker)


@broker.subscriber(stream="lead-streams")
async def lead_consumer(msg: LeadQueueMessage, logger: Logger):
    logger.info("lead received: %s", msg)

    dto = LeadDataKeyDTO(
        name=msg.name,
        phone=msg.phone,
        offer_id=str(msg.offer_id),
        affiliate_id=str(msg.affiliate_id),
    )

    is_new = await container.dedup.mark_if_not_exists(dto)

    if not is_new:
        logger.info("duplicate skipped")
        return

    async with db_helper.get_session() as session:
        repo = LeadRepo(session)
        service = LeadService(repo)

        await service.add_lead(
            CreateLeadDTO(
                name=msg.name,
                phone=msg.phone,
                country=msg.country,
                offer_id=msg.offer_id,
                affiliate_id=msg.affiliate_id,
            )
        )

    logger.info("lead saved")
