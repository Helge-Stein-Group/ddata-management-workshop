from nomad.datamodel import EntryData
from nomad.metainfo import MSection, Quantity, MEnum, Datetime, SubSection, Package
import numpy as np

import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from nomad.datamodel.metainfo.plot import PlotSection, PlotlyFigure

m_package = Package(name='Battery Cycles')


class DataPoint(MSection):
    datapointIndex = Quantity(type=int)

    stepTimePassed = Quantity(type=np.float64, unit="ms")
    totalTimePassed = Quantity(type=np.float64, unit="ms")
    current = Quantity(type=np.float64, unit="amp")
    voltage = Quantity(type=np.float64, unit="V")
    capacity = Quantity(type=np.float64, unit="amp * hour")
    energy = Quantity(type=np.float64, unit="Wh")

    date = Quantity(type=Datetime)
    power = Quantity(type=np.float64, unit="W")


class ProtocolStep(MSection):
    datapoints = SubSection(section=DataPoint, repeats=True)

    stepNumber = Quantity(type=int)
    stepType = Quantity(type=MEnum(['CC DChg', 'CC Chg', 'Rest']))
    stepTime = Quantity(type=np.float64, unit="ms")
    capacity = Quantity(type=np.float64, unit="amp * hour")
    energy = Quantity(type=np.float64, unit="Wh")
    onesetVoltage = Quantity(type=np.float64, unit="V")
    endVoltage = Quantity(type=np.float64, unit="V")


class CycleSection(PlotSection, MSection):
    protocolSteps = SubSection(section=ProtocolStep, repeats=True)

    chargingCapacity = Quantity(type=np.float64, unit="amp * hour")
    dischargingCapacity = Quantity(type=np.float64, unit="amp * hour")
    ChgDChgEfficiency = Quantity(type=np.float64)
    chargingEnergy = Quantity(type=np.float64, unit="Wh")
    dischargingEnergy = Quantity(type=np.float64, unit="Wh")
    chargingTime = Quantity(type=np.float64, unit="ms")
    dischargingTime = Quantity(type=np.float64, unit="ms")

    def normalize(self, archive, logger):
        logger.info("Normalizing Cycle")

        steps = self.m_get_sub_sections(sub_section_def=CycleSection.protocolSteps)
        time = []
        voltage = []
        current = []
        energy = []

        for step in steps:
            datapoints: list[DataPoint] = step.m_get_sub_sections(sub_section_def=ProtocolStep.datapoints)
            for datapoint in datapoints:
                print(datapoint)
                time.append(datapoint.m_get(quantity_def=DataPoint.stepTimePassed, full=True)/1000)
                voltage.append(datapoint.m_get(quantity_def=DataPoint.voltage, full=True))
                current.append(datapoint.m_get(quantity_def=DataPoint.current, full=True))
                energy.append(datapoint.m_get(quantity_def=DataPoint.energy, full=True))

        voltage_line = px.line(x=time, y=voltage)
        current_line = px.line(x=time, y=current)
        energy_line = px.line(x=time, y=energy)

        figure = make_subplots(rows=1, cols=3)
        figure.add_trace(voltage_line.data[0], row=1, col=1)
        figure.add_trace(current_line.data[0], row=1, col=2)
        figure.add_trace(energy_line.data[0], row=1, col=3)

        figure.update_layout(height=800, width=800, title="Battery")
        print(figure.to_plotly_json())
        self.figures.append(PlotlyFigure(figure=figure.to_plotly_json()))
        # logger.info(figure)
        logger.info("Cycle Normalizer Complete")

class EntrySection(PlotSection, EntryData):
    cycles = SubSection(section=CycleSection, repeats=True)


m_package.__init_metainfo__()
