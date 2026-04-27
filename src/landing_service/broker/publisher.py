from landing_service.schemas.landing_schema import LeadQueueMessage, CreateLeadSchema
from faststream.exceptions import FastStreamException
from infrastructure import broker
import logging

logger = logging.getLogger(__name__)


class LeadPublisher:

    @staticmethod
    async def lead_publish_message(
        lead_data: LeadQueueMessage | CreateLeadSchema,
    ) -> bool:
        try:
            msg = LeadQueueMessage(**lead_data.model_dump())

            await broker.publish(
                msg,
                stream="lead-streams",
            )
            logger.info("Lead published to stream: %s", lead_data.phone)
            return True
        except FastStreamException as e:
            logger.error("Failed to publish lead to Redis Stream: %s", e)
            raise
