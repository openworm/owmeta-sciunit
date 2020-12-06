from owmeta_core.dataobject import (ObjectProperty,
                                    DatatypeProperty,
                                    PythonClassDescription)
import owmeta_core.dataobject_property as DOP

from sciunit.models import Model as SUModel
import sciunit.capabilities as SUCap
from sciunit.models.runnable import RunnableModel as SURunnableModel
from neuronunit.models.lems import LEMSModel as NULEMSModel
from neuronunit.models.reduced import ReducedModel as NUReducedModel
from neuronunit.models.channel import ChannelModel as NUChannelModel

from . import (SU_CONTEXT, NU_CONTEXT, BASE_NU_SCHEMA_NS,
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

    key_property = python_class


class RunnableCapability(Capability):
    '''
    Indicates a runnable SciUnit model
    '''

    sciunit_class = SUCap.Runnable

    class_context = SU_CONTEXT


class ModelMeta(type(SciUnit)):
    def augment_rdf_type_object(self, rdto):
        rdto.attach_property(CapabilityProperty)

        super().augment_rdf_type_object(rdto)
        # Using the mro rather than just __bases__ partly to make queries easier, but
        # also, this is well-founded: since capabilities are defined as super-classses of
        # models, then the Liskov substitution principle would imply that all capability
        # superclasses are also capabilities of any model to which the capability subclass
        # is applied.
        for parent in self.sciunit_class.mro():
            if (issubclass(parent, SUCap.Capability) and
                    # No real value in declaring this -- Capability is an "abstract" class
                    parent is not SUCap.Capability and
                    not issubclass(parent, SUModel)):
                # We only look at the in-memory ClassContext for the capabilities
                ctxdpcd = PythonClassDescription.contextualize_class(self.definition_context)
                pcd = ctxdpcd.from_class(parent)
                ctxdc = Capability.contextualize_class(self.definition_context)
                cap = ctxdc(python_class=pcd)
                # Not declaring super-classes
                rdto.capability(cap)


class Model(SciUnit, metaclass=ModelMeta):
    '''
    A SciUnit model
    '''

    class_context = SU_CONTEXT

    sciunit_class = SUModel

    rdf_type_object_deferred = True

    name = DatatypeProperty(__doc__='Name of the model')

    def load_sciunit_models(self):
        '''
        Load the sciunit model for this model class

        .. note:

        The default implementation assumes there are no parameters or other setup --
        probably not what you want.
        '''

        for model in self.load():
            yield model.contextualize(self.context).init_model()

    def init_model(self): raise NotImplementedError


class CapabilityProperty(SciUnitNS, DOP.ObjectProperty):
    '''
    Describes a capability a model has
    '''

    linkName = 'capability'
    class_context = SU_CONTEXT
    value_type = Capability
    owner_type = Model
    multiple = True


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


Model.init_rdf_type_object()


class RunnableModel(Model):
    '''
    A runnable SciUnit Model
    '''

    class_context = SU_CONTEXT

    sciunit_class = SURunnableModel

    attribute = ObjectProperty(value_type=RunnableModelAttribute,
            __doc__='Attribute for the Model')

    def load_attributes(self):
        '''
        Load the module attributes into `dict` from the `attribute`
        '''
        attrs = dict()
        for a in self.attribute.get():
            attrs[a.name()] = a.value()
        return attrs

    def init_model(self):
        mod = self.sciunit_class(name=self.name())
        attrs = self.load_attributes()
        # XXX: RunnableModel has some abstruse mechanism by which the "back-end" gets
        # attributes set which is different from what happens when you pass attrs to the
        # initializer, so we just call set_attrs here...
        mod.set_attrs(**attrs)
        return mod


class NeuronUnitNS:
    '''
    Namespacing for NeuronUnit DataObjects
    '''

    base_data_namespace = BASE_NU_DATA_NS

    base_namespace = BASE_NU_SCHEMA_NS


class LEMSModel(NeuronUnitNS, RunnableModel):
    """A generic LEMS model"""
    sciunit_class = NULEMSModel

    class_context = NU_CONTEXT

    LEMS_file_path_or_url = DatatypeProperty(__doc__='LEMS file')

    def init_model(self):
        ''' Loads the SciUnit model and sets attributes '''

        res = self.sciunit_class(
                self.LEMS_file_path_or_url(),
                name=self.name())
        attrs = self.load_attributes()
        res.set_attrs(**attrs)
        return res


class ChannelModel(LEMSModel):
    """A model for ion channels"""
    sciunit_class = NUChannelModel

    class_context = NU_CONTEXT


class ReducedModel(LEMSModel):
    """A reduced model"""
    sciunit_class = NUReducedModel

    class_context = NU_CONTEXT
# XXX: Maybe auto-generate the model class as far as capabilities by searching mro(), but
# it doesn't look like the parameters are queryable in general
