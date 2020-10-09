from owmeta_core.dataobject import (DataObject, ObjectProperty, DatatypeProperty, PythonClassDescription, PythonModule)
import owmeta_core.dataobject_property as DOP

from . import SU_CONTEXT, BASE_DATA_NS, BASE_SCHEMA_NS


class SciUnitNS:
    '''
    Namespacing for SciUnit DataObjects
    '''

    base_data_namespace = BASE_DATA_NS

    base_namespace = BASE_SCHEMA_NS


class SciUnitClass(type(DataObject)):

    context_carries = ('sciunit_class',)

    def __init__(self, name, bases, dct):
        self.sciunit_class = None
        if 'sciunit_class' in dct:
            self.sciunit_class = dct['sciunit_class']
        super().__init__(name, bases, dct)

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

    def load_sciunit_class(self):
        return self.rdf_type_object.sciunit_class().load_class()


class SciUnit(SciUnitNS, DataObject, metaclass=SciUnitClass):
    class_context = SU_CONTEXT
    rdf_type_object_deferred = True


class SciUnitClassProperty(SciUnitNS, DOP.ObjectProperty):
    '''
    Property that associates a SciUnit type with its SciUnit class
    '''
    class_context = SU_CONTEXT

    linkName = 'sciunit_class'
    value_type = PythonClassDescription
    owner_type = SciUnit


SciUnit.init_rdf_type_object()
