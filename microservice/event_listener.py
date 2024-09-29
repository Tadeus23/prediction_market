from contract_service import contract
import asyncio
import logging
from config import *

logger = logging.getLogger(__name__)

def handle_pool_created_event(event):
    pool_id = event['args']['poolId']
    creator = event['args']['creator']
    target_price = event['args']['targetPrice']
    stop_loss = event['args']['stopLoss']
    end_time = event['args']['endTime']

    logger.info(f"Event listener: New Pool Created: Pool ID: {pool_id}, Creator: {creator}, "
                f"Target Price: {target_price}, Stop Loss: {stop_loss}, End Time: {end_time}")

    # ToDo: Notify users on Discord or update a database

def handle_pool_finalized_event(event):
    pool_id = event['args']['poolId']
    final_price = event['args']['finalPrice']
    outcome = event['args']['outcome']

    logger.info(f"Event listener: Pool Finalized: Pool ID: {pool_id}, Final Price: {final_price}, Outcome: {outcome}")

    # ToDo: Notify users on Discord or update a database

def handle_event(event):
    event_name = event.event
    if event_name == 'PoolCreated':
        handle_pool_created_event(event)
    elif event_name == 'PoolFinalized':
        handle_pool_finalized_event(event)
    else:
        logger.warning(f"Event listener: Unhandled event type: {event_name}")

async def event_listener():
    try:
        pool_created_filter = contract.events.PoolCreated.create_filter(from_block='latest')
        pool_finalized_filter = contract.events.PoolFinalized.create_filter(from_block='latest')

        while True:
            created_events = pool_created_filter.get_new_entries()
            finalized_events = pool_finalized_filter.get_new_entries()

            for event in created_events:
                handle_event(event)

            for event in finalized_events:
                handle_event(event)

            await asyncio.sleep(2)

    except Exception as e:
        logger.error(f"Error in event listener: {e}")

def start_event_listener():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(event_listener())

if __name__ == "__main__":
    start_event_listener()
