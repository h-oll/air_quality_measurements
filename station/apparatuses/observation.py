from datetime import datetime
import logging

## Enable logging
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def format_observation(observable, outcome):
    logger.info(f'outcome: {outcome}, unit: {observable.unit}, short_name: {observable.short_name}, sensor: {observable.apparatus.name}.')
    return {
        "time": str(datetime.now()),
        "outcome": outcome,
        "unit": observable.unit,
        "name": observable.name,
        "short_name": observable.short_name,
        "kind": observable.kind,
        "apparatus_uuid": observable.apparatus.uuid,
        "apparatus_name": observable.apparatus.name              
    }
