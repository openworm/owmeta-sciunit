import rdflib

from owmeta_core.dataobject import DataObject, ObjectProperty, PythonClassDescription
from owmeta_core.dataobject_property import ObjectProperty
from owmeta_core.collections import List
from sciunit.models import Model as SUModel


BASE_SCHEMA_URL = 'http://schema.openworm.org/2020/07/sciunit'
BASE_SCHEMA_NS = rdflib.Namespace[BASE_SCHEMA_URL + '/']

BASE_DATA_URL = 'http://data.openworm.org/sciunit'
BASE_DATA_NS = rdflib.Namespace[BASE_DATA_URL + '/']


class SciUnitNS:
    '''
    Namespacing for SciUnit DataObjects
    '''

    class_context = BASE_SCHEMA_URL

    schema_namespace = BASE_DATA_NS

    base_namespace = BASE_SCHEMA_NS


class ModelCapability(SciUnitNS, DataObject):
    '''
    Describes a Capability of a SciUnit Model
    '''

    python_class = ObjectProperty(value_type=PythonClassDescription)
    '''
    Python class for the SciUnit Capability
    '''


class RunnableCapability(SciUnitNS, DataObject):
    '''
    Indicates a runnable SciUnit model
    '''


class ModelClass(type(DataObject)):
    def init_rdf_type_object(self):
        super().init_rdf_type_object()
        rdto = self.rdf_type_object
        rdto.attach_property(SciUnitModelClassProperty)


class Model(SciUnitNS, DataObject, metaclass=ModelClass):
    '''
    A SciUnit model
    '''

    capability = ObjectProperty(value_type=Capability)
    '''
    Capabilities the model has
    '''

    def load_sciunit_model_class(self):
        return self.python_class().load_class()

    def load_sciunit_model(self):
        cls = self.load_sciunit_model_class()
        return cls()


class SciUnitModelClassProperty(ObjectProperty):
    '''
    Property that associates a Model with its SciUnitModel
    '''
    linkName = 'sciunit_model_class'
    owner_type = Model
    value_type = PythonClassDescription


class ModelProperty(SciUnitNS, ObjectProperty):
    '''
    Property for associating an object with a SciUnit model
    '''
    value_type = Model


class RunnableModelAttribute(SciUnitNS, DataObject):
    '''
    Attribute of a runnable model
    '''

    name = DatatypeProperty()
    value = DatatypeProperty()


class RunnableModel(Model):
    '''
    A runnable SciUnit Model
    '''

    attribute = ObjectProperty(value_type=RunnableModelAttribute)
    '''
    Attribute for the Model
    '''
    def __init__(self, python_class=None, **kwargs):
        if python_class is None:
            pcd = PythonClassDescription()
            pcd.name('RunnableModel')
            mod = PythonModule(name='sciunit.models.runnable')
            pcd.module(mod)
            python_class = pcd
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


class LEMSModel(RunnableModel):
    pass

# XXX: Maybe auto-generate the model class as far as capabilities by searching mro(), but
# it doesn't look like the parameters are queryable in general
