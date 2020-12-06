import unittest

import neuronunit.models.lems as nu_lems
from owmeta_core.context import Context, CLASS_REGISTRY_CONTEXT_KEY
from owmeta_core.data import Data

from owmeta_sciunit.model import Model, RunnableModel, LEMSModel, ReducedModel


def test_runnable_model_runnable_capability():
    assert ('sciunit.capabilities', 'Runnable') in \
            (cap_cname(c) for c in RunnableModel.rdf_type_object.capability.defined_values)


def test_lems_model_runnable_capability():
    assert ('sciunit.capabilities', 'Runnable') in \
            (cap_cname(c) for c in LEMSModel.rdf_type_object.capability.defined_values)


def test_reduced_model_runnable_capability():
    assert ('sciunit.capabilities', 'Runnable') in \
            (cap_cname(c) for c in ReducedModel.rdf_type_object.capability.defined_values)


def test_reduced_model_receives_square_current_capability():
    assert ('neuronunit.capabilities', 'ReceivesSquareCurrent') in \
            (cap_cname(c) for c in ReducedModel.rdf_type_object.capability.defined_values)


def test_reduced_model_produces_action_potentials_capability():
    assert ('neuronunit.capabilities', 'ProducesActionPotentials') in \
            (cap_cname(c) for c in ReducedModel.rdf_type_object.capability.defined_values)


def cap_cname(cap):
    pcd = cap.python_class.onedef()
    cname = pcd.name.onedef()
    mod = pcd.module.onedef()
    modname = mod.name.onedef()
    return modname, cname


class LEMSModelLoadTest(unittest.TestCase):
    def setUp(self):
        self.conf = Data()
        self.conf.init()
        self.ctx = Context('http://example.org/ctx', conf=self.conf)
        self.mapper = self.ctx.mapper
        self.conf[CLASS_REGISTRY_CONTEXT_KEY] = self.mapper.class_registry_context.identifier
        self.imports_ctx = Context('http://example.org/imports', conf=self.conf)

        self.ctx(LEMSModel)(ident='http://example.org/lems_model',
                LEMS_file_path_or_url='tests/data/LEMS_Test_ca_boyle.xml')
        LEMSModel.definition_context.save(self.conf['rdf.graph'])
        self.ctx.add_import(LEMSModel.definition_context)
        self.ctx.save_imports(self.imports_ctx)
        self.ctx.save()
        self.mapper.declare_python_class_registry_entry(LEMSModel)
        self.mapper.save()

    def test_load_lems_model_from_RunnableModel(self):
        self.mapper.declare_python_class_registry_entry(RunnableModel)
        self.mapper.save()

        print(self.conf['rdf.graph'].serialize(format='n3').decode('UTF-8'))

        ctx1 = Context('http://example.org/ctx', conf=self.conf)
        runnable_model = ctx1.stored(RunnableModel).query()
        for loaded_model in runnable_model.load_sciunit_models():
            assert isinstance(loaded_model, nu_lems.LEMSModel)
            break
        else: # no break
            assert False, "Should have loaded a model"

    def test_load_lems_model_from_Model(self):
        Model.definition_context.save(self.conf['rdf.graph'])
        self.mapper.declare_python_class_registry_entry(RunnableModel, Model)
        self.mapper.save()

        print(self.conf['rdf.graph'].serialize(format='n3').decode('UTF-8'))

        ctx1 = Context('http://example.org/ctx', conf=self.conf)
        runnable_model = ctx1.stored(Model).query()
        for loaded_model in runnable_model.load_sciunit_models():
            assert isinstance(loaded_model, nu_lems.LEMSModel)
            break
        else: # no break
            assert False, "Should have loaded a model"
