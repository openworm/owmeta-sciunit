'''
Classes for SciUnit tests
'''
import owmeta_core.dataobject as DO
import neuronunit.tests.base as NUB
import neuronunit.tests.druckman2013 as DR13
import sciunit.tests as SU

from .base import SciUnit


class Test(SciUnit):
    sciunit_class = SU.Test

    name = DO.DatatypeProperty()
    description = DO.DatatypeProperty()

    def create_sciunit_test(self):
        '''
        Creates a SciUnit Test instance corresponding to this
        `~owmeta_core.dataobject.DataObject`

        The default implementation assumes the initializer takes no arguments.
        '''
        cls = type(self).load_sciunit_class()
        return cls()


class _Namespace:
    pass


class _ClassFactory(object):
    def __init__(self):
        # Mapps from sciunit classes to created classes
        self.created_classes = dict()
        self.namespace = _Namespace()

    def _create_class(self, sciunit_class):
        name = sciunit_class.__name__
        do_bases = []
        for subase in sciunit_class.mro():
            do_base = self.created_classes.get(subase)
            if do_base:
                do_bases.append(do_base)
        res = type(name, tuple(do_bases),
                dict(sciunit_class=sciunit_class))
        self.created_class[sciunit_class] = res
        setattr(self.namespace, name, res)
        return res

    create_class = _create_class

    def create_classes(self, *sciunit_classes):
        ns0 = _Namespace()
        for sciunit_class in sciunit_classes:
            res = self._create_class(sciunit_class)
            setattr(ns0, res.__name__, res)
        return ns0


ClassFactory = _ClassFactory()


ProtocolToFeaturesTest = ClassFactory.create_class(SU.ProtocolToFeaturesTest)
VmTest = ClassFactory.create_class(NUB.VmTest)

Druckman2013 = ClassFactory.create_class(
        DR13.Druckmann2013Test,
        DR13.AP12AmplitudeDropTest,
        DR13.AP1SSAmplitudeChangeTest,
        DR13.AP1AmplitudeTest,
        DR13.AP1WidthHalfHeightTest,
        DR13.AP1WidthPeakToTroughTest,
        DR13.AP1RateOfChangePeakToTroughTest,
        DR13.AP1AHPDepthTest,
        DR13.AP2AmplitudeTest,
        DR13.AP2WidthHalfHeightTest,
        DR13.AP2WidthPeakToTroughTest,
        DR13.AP2RateOfChangePeakToTroughTest,
        DR13.AP2AHPDepthTest,
        DR13.AP12AmplitudeChangePercentTest,
        DR13.AP12HalfWidthChangePercentTest,
        DR13.AP12RateOfChangePeakToTroughPercentChangeTest,
        DR13.AP12AHPDepthPercentChangeTest,
        DR13.InputResistanceTest,
        DR13.AP1DelayMeanTest,
        DR13.AP1DelaySDTest,
        DR13.AP2DelayMeanTest,
        DR13.AP2DelaySDTest,
        DR13.Burst1ISIMeanTest,
        DR13.Burst1ISISDTest,
        DR13.InitialAccommodationMeanTest,
        DR13.SSAccommodationMeanTest,
        DR13.AccommodationRateToSSTest,
        DR13.AccommodationAtSSMeanTest,
        DR13.AccommodationRateMeanAtSSTest,
        DR13.ISICVTest,
        DR13.ISIMedianTest,
        DR13.ISIBurstMeanChangeTest,
        DR13.SpikeRateStrongStimTest,
        DR13.AP1DelayMeanStrongStimTest,
        DR13.AP1DelaySDStrongStimTest,
        DR13.AP2DelayMeanStrongStimTest,
        DR13.AP2DelaySDStrongStimTest,
        DR13.Burst1ISIMeanStrongStimTest,
        DR13.Burst1ISISDStrongStimTest)
