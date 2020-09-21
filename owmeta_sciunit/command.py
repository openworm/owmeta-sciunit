from owmeta_core.command_util import SubCommand
from owmeta_sciunit.model import Model


class OWMSciunitModel:
    '''
    SciUnit Model commands
    '''
    def __init__(self, par):
        self._owm_sciunit = par
        self._owm = par._owm

    def list(self):
        '''
        List models
        '''
        ctx = self._owm.default_context.stored
        for m in ctx(Model)().load():
            yield m

    def list_kinds(self, full=False):
        '''
        List kinds of model
        '''
        from owmeta_core.dataobject import TypeDataObject, RDFSSubClassOfProperty
        from owmeta_core.graph_object import ZeroOrMoreTQLayer
        from owmeta_core.rdf_query_util import zomifier

        conf = self._owm._conf()
        ctx = self._owm.default_context.stored

        rdfto = ctx(Model.rdf_type_object)
        sc = ctx(TypeDataObject)()
        sc.attach_property(RDFSSubClassOfProperty)(rdfto)

        nm = conf['rdf.graph'].namespace_manager
        g = ZeroOrMoreTQLayer(zomifier(Model.rdf_type), ctx.rdf_graph())
        for x in sc.load(graph=g):
            if full:
                yield x.identifier
            else:
                yield nm.normalizeUri(x.identifier)


class OWMSciunit:
    '''
    SciUnit commands
    '''

    model = SubCommand(OWMSciunitModel)

    def __init__(self, par):
        self._owm = par
