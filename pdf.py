import PyPDF4
import re

FILE_PATH = './test/CBC-Sample (2).pdf'

with open(FILE_PATH, mode='rb') as f:
    reader = PyPDF4.PdfFileReader(f)
    page = reader.getPage(0)
    txt = page.extractText()

numericalValues = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", txt)
# 
values = re.split("\n",txt)
data = {}
data['source'] = values[35] + values[36] + values[37]
data['labNumber'] = numericalValues[7] 
data['pid'] = values[16] + values[17]
data['dateRequested'] = values[47] + values[48] + values[49] + values[50] + values[51]
data['dateReceived'] = values[85] + values[86] + values[87] + values[88] + values[89]
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