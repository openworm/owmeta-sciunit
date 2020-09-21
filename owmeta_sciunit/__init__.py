import rdflib
from owmeta_core import BASE_CONTEXT
from owmeta_core.context import ClassContext


__version__ = '0.0.1'


BASE_SCHEMA_URL = 'http://schema.openworm.org/2020/07/sciunit'
BASE_SCHEMA_NS = rdflib.Namespace(BASE_SCHEMA_URL + '/')

BASE_DATA_URL = 'http://data.openworm.org/sciunit'
BASE_DATA_NS = rdflib.Namespace(BASE_DATA_URL + '/')

BASE_NU_SCHEMA_URL = 'http://schema.openworm.org/2020/07/neuronunit'
BASE_NU_SCHEMA_NS = rdflib.Namespace(BASE_NU_SCHEMA_URL + '/')

BASE_NU_DATA_URL = 'http://data.openworm.org/neuronunit'
BASE_NU_DATA_NS = rdflib.Namespace(BASE_NU_DATA_URL + '/')

SU_CONTEXT = ClassContext(BASE_SCHEMA_URL, imported=(BASE_CONTEXT,))
NU_CONTEXT = ClassContext(BASE_NU_SCHEMA_URL, imported=(SU_CONTEXT, BASE_CONTEXT))
