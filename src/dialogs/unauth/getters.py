import logging

logger = logging.getLogger(__name__)


async def get_user(**kwargs):
    return {'user_id': kwargs.get('user_id')}
