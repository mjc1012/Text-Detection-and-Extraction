import docx2txt as d2t
import re

FILE_PATH = './test/CBC Sample.docx'
txt = d2t.process(FILE_PATH)

numericalValues = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", txt)
values = re.split('\s+',txt)
print(values)
data = {}
data['source'] = values[15] + " " + values[16] + " " + values[17] 
data['labNumber'] = values[29] 
data['pid'] = values[7]
data['dateRequested'] = values[23] + " " + values[24] + " " + values[25]
data['dateReceived'] = values[43] + " " + values[44] + " " + values[45] 
data['whiteBloodCells'] = numericalValues[18] 
data['redBloodCells'] = numericalValues[23] 
data['hemoglobin'] = numericalValues[28] 
data['hematocrit'] = numericalValues[31] 
data['meanCorpuscularVolume'] = numericalValues[34] 
data['meanCorpuscularHb'] = numericalValues[37] 
data['meanCorpuscularHbConc'] = numericalValues[40] 
data['rbcDistributionWidth'] = numericalValues[43] 
data['plateletCount'] = numericalValues[46] 
data['segmenters'] = numericalValues[51] 
data['lymphocytes'] = numericalValues[54] 
data['monocytes'] = numericalValues[57] 
data['eosinophils'] = numericalValues[60] 
data['basophils'] = numericalValues[63] 
data['bands'] = numericalValues[66] 
data['absoluteSeg'] = numericalValues[69] 
data['absoluteLymphocyteCount'] = numericalValues[74] 
data['absoluteMonocyteCount'] = numericalValues[79] 
data['absoluteEosinophilCount'] = numericalValues[83] 
data['absoluteBasophilCount'] = numericalValues[87] 
data['absoluteBandCount'] = numericalValues[91]


for x, y in data.items():
    print(x, '=', y)