import logging 

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class Apparatus:
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid
        self.observables = [] 

    def observe(self):
        logger.critical('Observe method not implemented.')
        raise NameError('Observe method not implemented.')
        
    
    def get_observations(self):
        for o in self.observables:
            o.read_observation()

