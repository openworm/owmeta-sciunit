import logging

from owmeta_core.dataobject import (DataObject, PythonClassDescription, PythonModule)
import owmeta_core.dataobject_property as DOP

from . import SU_CONTEXT, BASE_DATA_NS, BASE_SCHEMA_NS


L = logging.getLogger(__name__)


class SciUnitNS:
    '''
    Namespacing for SciUnit DataObjects
    '''

    base_data_namespace = BASE_DATA_NS

    base_namespace = BASE_SCHEMA_NS


class SciUnitClass(type(DataObject)):
    '''
    Attributes
    ----------
    sciunit_class : type
        The SciUnit class corresponding to this class
    '''

    context_carries = ('sciunit_class',)

    def augment_rdf_type_object(self, rdto):
        if not getattr(self, 'sciunit_class', None):
            return

        rdto.attach_property(SciUnitClassProperty)

        sucn = self.sciunit_class.__name__
        sumn = self.sciunit_class.__module__

        ctx = rdto.context

        pcd = ctx(PythonClassDescription)()
        pcd.name(sucn)
        mod = ctx(PythonModule)(name=sumn)
        pcd.module(mod)
        rdto.sciunit_class(pcd)

    def load_sciunit_classes(self):
        '''
        Load the SciUnit class(es) for this DataObject class.

        If you already have the specific class, the return value should be equal to
        `self.sciunit_class`
        '''
        rdto = self.rdf_type_object.contextualize(self.context)
        for c in rdto.sciunit_class.get():
            yield c.resolve_class()


class SciUnit(SciUnitNS, DataObject, metaclass=SciUnitClass):
    '''
    Base class for SciUnit `DataObject`s
    '''
    class_context = SU_CONTEXT
    rdf_type_object_deferred = True


class SciUnitClassProperty(SciUnitNS, DOP.ObjectProperty):
    '''
    Property that associates a SciUnit `DataObject` sub-class with its SciUnit class
    '''
    class_context = SU_CONTEXT

    linkName = 'sciunit_class'
    value_type = PythonClassDescription
    owner_type = SciUnit


SciUnit.init_rdf_type_object()
