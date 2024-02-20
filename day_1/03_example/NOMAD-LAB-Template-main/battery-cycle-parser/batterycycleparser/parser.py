from .schema import EntrySection, CycleSection, ProtocolStep, DataPoint
import pandas as pd
from datetime import datetime
from nomad.datamodel import EntryArchive, EntryMetadata


class BatteryCycleParser:
    class NoCyclesFoundException(Exception):
        pass

    class NoStepsFoundException(Exception):
        pass

    def parse(self, mainfile, archive: EntryArchive, logger):
        csvdata = pd.read_csv(mainfile)

        parsedData = self.readcsv(csvdata)

        archive.data = parsedData

    '''
        findCycles(self, entireDataFrame: pd.DataFrame) -> list[tuple(pd.DataFrame, CycleSection)]:
            If the column "Cycle Index" (column 1) is not NaN, that's the start of the an "entry" (type: EntrySection).
            The end of the "entry" is either:
                1. The end of the dataframe (AKA file)
                2. Another row in the dataframe has column "Cycle Index" != NaN.
                
            1. Find the rows of the dataframe where:
                - "Cycle Index" is not NaN.
            2. Put the indices of the rows in a list.
            3. If length of list is = 1, there is only one cycle, 
            4. Else, there are multiple cycles.
            
            if length of list < 1: there are no cycles found, throw NoCyclesFoundException()
            For each cycle, instantiate a "CycleSection" object and fill the object with the attributes of each cycle.
            
            If length of list = 1:
                From index of the row until the end of the file is one entry
                continue with splitting up into operations -> findSteps (Rest, CC DChg, CC Chg, etc.)
            Else (AKA list > 1):
                first entry will go from the index until the index before the index of the second entry.
                Ex: 
                    indices = [3, 100, 150, ...]
                    
                    entry1 = entireDataFrame.iloc[3, 99].copy()
                    entry2 = entireDataFrame.iloc[100, 149].copy()
                    ....
            
            return list[entry1, entry2, ....] 
    '''
    '''
    findSteps(self, singleCycleDataFrame: pd.DataFrame) -> list[tuple(pd.DataFrame, BatteryStep)]:
            Find rows where the value in Step Index (column 2) != NaN.
            The end of the "step" is either:
                1. The end of the dataframe (AKA File)
                2. Another row in the column has column "Step Index" != NaN
                
            1. Find the rows of the dataframe where:
                - "Step Index" is not NaN.
            2. Put the indices of the rows in a list.
            
            if length of list < 1: there are no steps found, throw NoStepsFoundException()
            For each cycle, instantiate a "CycleSection" object and fill the object with the attributes of each cycle.
            
            Iterate through the list:
            [Refer to findCycles]
    '''
    '''
    extractDataPoints(self, singleStepDataFrame: pd.DataFrame) -> list[DataPoint]:
            Instantiate a list of type datapoint
        
            Iterate through each row of the dataframe:
                For each row:
                    - Instantiate a new DataPoint object
                    - Fill the DataPoint object with the attributes of each row
                    - Append the datapoint to the aforementioned list.
            
            Return list.
    '''

    def findCycles(self, entireDataFrame: pd.DataFrame) -> list[tuple[CycleSection, pd.DataFrame]]:

        cycles: list[tuple(CycleSection, pd.DataFrame)] = []

        cycleIndices = entireDataFrame.index[entireDataFrame['Cycle Index'].notna()].tolist()

        for index, cycleIndex in enumerate(cycleIndices):
            df = pd.DataFrame()
            if index == len(cycleIndices) - 1:
                df = entireDataFrame.iloc[cycleIndex:].copy()
            else:
                df = entireDataFrame.iloc[cycleIndex:cycleIndices[index + 1]].copy()

            df.reset_index(drop=True, inplace=True)

            cycle = CycleSection()

            cycle.chargingCapacity = df.iloc[0, 1]
            cycle.dischargingCapacity = df.iloc[0, 2]
            cycle.ChgDChgEfficiency = df.iloc[0, 3]
            cycle.chargingEnergy = df.iloc[0, 4]
            cycle.dischargingEnergy = df.iloc[0, 5]
            cycle.chargingTime = df.iloc[0, 6]
            cycle.dischargingTime = df.iloc[0, 7]

            df.drop(0, axis=0, inplace=True)
            df.drop('Cycle Index', axis=1, inplace=True)
            df.columns = ["Step Index", "Step Number", "Step Type", "Step Time", "Capacity(Ah)", "Energy(Wh)",
                          "Oneset Volt.(V)", "End Voltage(V)", "", "", ""]
            df.reset_index(drop=True, inplace=True)

            cycles.append((cycle, df))
        return cycles

    def findSteps(self, singleCycleDataFrame: pd.DataFrame) -> list[
        tuple[ProtocolStep, pd.DataFrame]]:
        steps: list[tuple[ProtocolStep, pd.DataFrame]] = []

        stepIndices = singleCycleDataFrame.index[singleCycleDataFrame["Step Index"].notna()].tolist()

        for index, stepIndex in enumerate(stepIndices):
            df = pd.DataFrame()

            if index == len(stepIndices) - 1:
                df = singleCycleDataFrame.iloc[stepIndex:].copy()
            else:
                df = singleCycleDataFrame.iloc[stepIndex: stepIndices[index + 1]].copy()

            df.reset_index(drop=True, inplace=True)

            batteryStep = ProtocolStep()

            batteryStep.stepNumber = int(df.iloc[0, 1])
            batteryStep.stepType = df.iloc[0, 2]
            batteryStep.stepTime = self.convertTimeStampToMilliseconds(df.iloc[0, 3])
            batteryStep.capacity = df.iloc[0, 4]
            batteryStep.energy = df.iloc[0, 5]
            batteryStep.onesetVoltage = df.iloc[0, 7]
            batteryStep.endVoltage = df.iloc[0, 8]

            df.drop('Step Index', axis=1, inplace=True)
            df.drop(0, axis=0, inplace=True)
            df.columns = ["DataPoint", "Time", "Total Time", "Current(A)", "Voltage(V)", "Capacity(Ah)", "Energy(Wh)",
                          "Date", "Power(W)", ""]
            df.reset_index(drop=True, inplace=True)

            # batteryStep = BatteryStep(
            #     datapoints=[],
            #     stepNumber=stepNumber,
            #     stepType=stepType,
            #     stepTime=stepTime,
            #     capacity=capacity,
            #     energy=energy,
            #     onesetVoltage=onesetVoltage,
            #     endVoltage=endVoltage
            # )

            steps.append((batteryStep, df))

        return steps

    def extractDataPoints(self, batteryStepDataFrame: pd.DataFrame) -> list[DataPoint]:
        datapoints: [DataPoint] = []

        for index, row in batteryStepDataFrame.iterrows():
            datapoint = DataPoint()

            datapoint.datapointIndex = int(row['DataPoint'])

            datapoint.stepTimePassed = self.convertTimeStampToMilliseconds(row['Time'])
            datapoint.totalTimePassed = self.convertTimeStampToMilliseconds(row["Total Time"])
            datapoint.current = row['Current(A)']
            datapoint.voltage = row['Voltage(V)']
            datapoint.capacity = row['Capacity(Ah)']
            datapoint.energy = row['Energy(Wh)']
            datapoint.date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
            datapoint.power = row['Power(W)']

            datapoints.append(datapoint)

        return datapoints

    def readcsv(self, dataframe: pd.DataFrame) -> EntrySection:

        cycles = self.findCycles(dataframe)
        t_cycles: [CycleSection] = []

        for cycle in cycles:
            steps = self.findSteps(cycle[1])
            for step in steps:
                datapoints = self.extractDataPoints(step[1])

                for datapoint in datapoints:
                    step[0].m_add_sub_section(sub_section_def=ProtocolStep.datapoints, sub_section=datapoint)

                cycle[0].m_add_sub_section(sub_section_def=CycleSection.protocolSteps, sub_section=step[0])


            t_cycles.append(cycle[0])

        print(t_cycles[0].dischargingEnergy)

        entry = EntrySection()

        for cycle in t_cycles:
            entry.m_add_sub_section(sub_section_def=EntrySection.cycles, sub_section=cycle)

        return entry

    def convertTimeStampToMilliseconds(self, timeStamp: str) -> int:
        hours, minutes, seconds = map(int, timeStamp.split(':'))
        time = (hours * 3600 + minutes * 60 + seconds) * 1000

        return time
