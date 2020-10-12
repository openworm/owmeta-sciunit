from owmeta_sciunit.model import RunnableModel, LEMSModel, ReducedModel


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
