import rdflib

from owmeta_core.dataobject import (DataObject, ObjectProperty, DatatypeProperty, PythonClassDescription, PythonModule)
import owmeta_core.dataobject_property as DOP
from owmeta_core.collections import List

from sciunit.models import Model as SUModel
from sciunit.capabilities import Runnable as SURunnable
from sciunit.models.runnable import RunnableModel as SURunnableModel
from neuronunit.models.lems import LEMSModel as SULEMSModel
from neuronunit.models.channel import ChannelModel as SUChannelModel

from . import (SU_CONTEXT, NU_CONTEXT, BASE_DATA_NS, BASE_SCHEMA_NS, BASE_NU_SCHEMA_NS,
               BASE_NU_DATA_NS)
from .base import SciUnit, SciUnitNS


class Capability(SciUnit):
    '''
    Describes a Capability of a SciUnit Model
    '''

    class_context = SU_CONTEXT

    python_class = ObjectProperty(value_type=PythonClassDescription)
    '''
    Python class for the SciUnit Capability
    '''


class RunnableCapability(Capability):
    '''
    Indicates a runnable SciUnit model
    '''

    sciunit_class = SURunnable

    class_context = SU_CONTEXT


class Model(SciUnit):
    '''
    A SciUnit model
    '''

    class_context = SU_CONTEXT

    sciunit_class = SUModel

    capability = ObjectProperty(value_type=Capability)
    '''
    Capabilities the model has
    '''

    rdf_type_object_deferred = True

    def load_sciunit_model(self):
        cls = type(self).load_sciunit_class()
        return cls()


class ModelProperty(SciUnitNS, DOP.ObjectProperty):
    '''
    Property for associating an object with a SciUnit model
    '''
    class_context = SU_CONTEXT

    value_type = Model


class RunnableModelAttribute(SciUnit):
    '''
    Attribute of a runnable model
    '''

    class_context = SU_CONTEXT

    name = DatatypeProperty()
    value = DatatypeProperty()


class RunnableModel(Model):
    '''
    A runnable SciUnit Model
    '''

    class_context = SU_CONTEXT

    sciunit_class = SURunnableModel

    attribute = ObjectProperty(value_type=RunnableModelAttribute)
    '''
    Attribute for the Model
    '''
    def __init__(self, python_class=None, **kwargs):
        super().__init__(python_class=python_class, **kwargs)

    def load_attributes(self):
        '''
        Load the module attributes into `dict` from the `attribute`
        '''
        attr = self.attribute()
        attrs = dict()
        for a in attr.load():
            attrs[a.name()] = a.value()
        return attrs

    def load_sciunit_model(self):
        '''
        Loads the SciUnit model and sets attributes
        '''
        mod = self.load_sciunit_model()
        attrs = self.load_attributes()
        mod.set_attrs(**attrs)
        return mod


class NeuronUnitNS:
    '''
    Namespacing for NeuronUnit DataObjects
    '''

    base_data_namespace = BASE_NU_DATA_NS

    base_namespace = BASE_NU_SCHEMA_NS


class LEMSModel(RunnableModel, NeuronUnitNS):
    """A generic LEMS model."""
    sciunit_class = SULEMSModel

    class_context = NU_CONTEXT


class ChannelModel(LEMSModel, NeuronUnitNS):
    """A model for ion channels"""
    sciunit_class = SUChannelModel

    class_context = NU_CONTEXT

# XXX: Maybe auto-generate the model class as far as capabilities by searching mro(), but
# it doesn't look like the parameters are queryable in general
