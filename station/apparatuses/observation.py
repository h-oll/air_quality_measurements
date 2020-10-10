from datetime import datetime
import logging
import uuid

## Enable logging
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


class Observation:
    def __init__(self, observable):
        self.uuid = uuid.uuid4()
        self.observable = observable
        self.outcome = observable.apparatus.data[observable.short_name]
        self.time = observable.apparatus.data["time"]
        logger.info(f'time: {self.time}, outcome: {self.outcome}, unit: {self.observable.unit}, short_name: {self.observable.short_name}, apparatus: {self.observable.apparatus.name}".')
