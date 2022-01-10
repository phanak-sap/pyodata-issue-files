import base64
import pyodata
import requests
import responses
from pyodata.v2.model import PolicyFatal,PolicyWarning, ParserError, Config

custom_config = Config(
    default_error_policy=PolicyWarning(),
    custom_error_policies={
         ParserError.ANNOTATION: PolicyWarning(),
         ParserError.ASSOCIATION: PolicyWarning()
    })


SERVICE_URL = 'http://example.com'
FILE_NAME = 'metadata.xml'
GUID_BINARY = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'


@responses.activate
def testcase():
    guid_base16: str = base64.b16encode(GUID_BINARY).decode()
    guid_base64: str = base64.b64encode(GUID_BINARY).decode()

    responses.add(
        responses.GET,
        # For JSON payload Edm.Binary must be Base64 encoded
        # as defined in https://www.odata.org/documentation/odata-version-2-0/json-format/
        # 4. Primitive Types
        'http://example.com/EntityName?%24top=1&%24select=Guid',
        json={'d':{'results':[{'Guid':guid_base64}]}},
    )
    responses.add(
        responses.GET,
        # For OData URI or HTTP header Edm.Binary must be in the literal form
        # as defined in https://www.odata.org/documentation/odata-version-2-0/overview/
        # 6. Primitive Data Types
        f'http://example.com/EntityName(binary\'{guid_base16}\')/Description/',
        json={'d':{'Description':'PASS'}},
    )

    with open(FILE_NAME, 'rb') as mtd_file:
        local_metadata = mtd_file.read()

    client = pyodata.Client(SERVICE_URL, requests, metadata=local_metadata , config=custom_config)

    items = client.entity_sets.EntityName.get_entities().select('Guid').top(1).execute()
    assert items[0].Description == 'PASS'


testcase()
