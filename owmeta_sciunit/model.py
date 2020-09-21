import rdflib

from owmeta_core.dataobject import (DataObject, ObjectProperty, DatatypeProperty, PythonClassDescription, PythonModule)
import owmeta_core.dataobject_property as DOP
from owmeta_core.collections import List

from sciunit.models import Model as SUModel
from sciunit.models.runnable import RunnableModel as SURunnableModel
from neuronunit.models.lems import LEMSModel as SULEMSModel
from neuronunit.models.channel import ChannelModel as SUChannelModel

from . import (SU_CONTEXT, NU_CONTEXT, BASE_DATA_NS, BASE_SCHEMA_NS, BASE_NU_SCHEMA_NS,
               BASE_NU_DATA_NS)


class SciUnitNS:
    '''
    Namespacing for SciUnit DataObjects
    '''

    base_data_namespace = BASE_DATA_NS

    base_namespace = BASE_SCHEMA_NS


class Capability(SciUnitNS, DataObject):
    '''
    Describes a Capability of a SciUnit Model
    '''

    class_context = SU_CONTEXT

    python_class = ObjectProperty(value_type=PythonClassDescription)
    '''
    Python class for the SciUnit Capability
    '''


class RunnableCapability(SciUnitNS, DataObject):
    '''
    Indicates a runnable SciUnit model
    '''

    class_context = SU_CONTEXT


class ModelClass(type(DataObject)):

    context_carries = ('sciunit_model_class',)

    def __init__(self, name, bases, dct):
        self.sciunit_model_class = None
        if 'sciunit_model_class' in dct:
            self.sciunit_model_class = dct['sciunit_model_class']
        super().__init__(name, bases, dct)

    def augment_rdf_type_object(self, rdto):
        rdto.attach_property(SciUnitModelClassProperty)

        if not getattr(self, 'sciunit_model_class', None):
            raise AttributeError('Expecting `sciunit_model_class` attribute to be defined')

        sucn = self.sciunit_model_class.__name__
        sumn = self.sciunit_model_class.__module__

        ctx = rdto.context

        pcd = ctx(PythonClassDescription)()
        pcd.name(sucn)
        mod = ctx(PythonModule)(name=sumn)
        pcd.module(mod)
        rdto.sciunit_model_class(pcd)


class Model(SciUnitNS, DataObject, metaclass=ModelClass):
    '''
    A SciUnit model
    '''

    class_context = SU_CONTEXT

    sciunit_model_class = SUModel

    capability = ObjectProperty(value_type=Capability)
    '''
    Capabilities the model has
    '''

    rdf_type_object_deferred = True

    def load_sciunit_model_class(self):
        return self.python_class().load_class()

    def load_sciunit_model(self):
        cls = self.load_sciunit_model_class()
        return cls()


class SciUnitModelClassProperty(SciUnitNS, DOP.ObjectProperty):
    '''
    Property that associates a Model with its SciUnitModel
    '''
    class_context = SU_CONTEXT

    linkName = 'sciunit_model_class'
    value_type = PythonClassDescription
    owner_type = Model


Model.init_rdf_type_object()


class ModelProperty(SciUnitNS, DOP.ObjectProperty):
    '''
    Property for associating an object with a SciUnit model
    '''
    class_context = SU_CONTEXT

    value_type = Model


class RunnableModelAttribute(SciUnitNS, DataObject):
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

    sciunit_model_class = SURunnableModel

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
    sciunit_model_class = SULEMSModel

    class_context = NU_CONTEXT


class ChannelModel(LEMSModel, NeuronUnitNS):
    """A model for ion channels"""
    sciunit_model_class = SUChannelModel

    class_context = NU_CONTEXT

# XXX: Maybe auto-generate the model class as far as capabilities by searching mro(), but
# it doesn't look like the parameters are queryable in general
