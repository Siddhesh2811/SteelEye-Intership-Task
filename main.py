import xml.etree.ElementTree as ET
import requests
import zipfile
import pandas as pd
import os

 
def download_extract_csv(link, fname):
    r = requests.get(str(link))
    with open(str(fname), 'wb') as f:
        f.write(r.content)
    target = str(fname)
    handle = zipfile.ZipFile(target)
    handle.extractall("Unzipped Files")
    handle.close()


def xmltocsv(filename):
    i = ET.parse(filename)
    iroot = i.getroot()
    FinInstrmGnlAttrbts = iroot[1][0][0][1][0][0]
    Id = FinInstrmGnlAttrbts[0].text
    FullNm = FinInstrmGnlAttrbts[1].text
    ClssfctnTp = FinInstrmGnlAttrbts[3].text
    CmmdtyDerivInd = FinInstrmGnlAttrbts[5].text
    NtnlCcy = FinInstrmGnlAttrbts[4].text
    Issr = iroot[1][0][0][1][0][1].text
    record = [Id, FullNm, ClssfctnTp, CmmdtyDerivInd, NtnlCcy, Issr]
    return record

if __name__=='__main__':
    mytree = ET.parse('select.xml')
    root = mytree.getroot()
    result = root[1]
    cols = [
    "FinInstrmGnlAttrbts.Id",
    "FinInstrmGnlAttrbts.FullNm",
    "FinInstrmGnlAttrbts.ClssfctnTp",
    "FinInstrmGnlAttrbts.CmmdtyDerivInd",
    "FinInstrmGnlAttrbts.NtnlCcy",
    "Issr"]
    rows = []
    for x in result:
        link = x[1].text
        fname = x[6].text
        download_extract_csv(link, fname)
    files = os.listdir("Unzipped Files")
    for x in files:
        y = xmltocsv("Unzipped Files" + "\\" + x)
        rows.append({"FinInstrmGnlAttrbts.Id": y[0],
                 "FinInstrmGnlAttrbts.FullNm": y[1],
                 "FinInstrmGnlAttrbts.ClssfctnTp": y[2],
                 "FinInstrmGnlAttrbts.CmmdtyDerivInd": y[3],
                 "FinInstrmGnlAttrbts.NtnlCcy": y[4],
                 "Issr": y[5]})

    df = pd.DataFrame(rows, columns=cols)
    df.to_csv('assesment.csv')
