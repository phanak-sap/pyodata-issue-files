import pyodata
from pyodata.v2.model import PolicyFatal,PolicyWarning, ParserError, PolicyIgnore, Config

import logging
logging.basicConfig()
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)


custom_config = Config(
    default_error_policy=PolicyIgnore(),
    custom_error_policies={
         ParserError.ANNOTATION: PolicyIgnore(),
         ParserError.ASSOCIATION: PolicyIgnore()
    })

FILE_NAME = 'metadata.xml'

with open(FILE_NAME, 'rb') as mtd_file:
    local_metadata = mtd_file.read()

sample = pyodata.Client('NOT_VALID', None, metadata=local_metadata , config=custom_config)
print('Metadata validation status: ',sample.schema.is_valid)

