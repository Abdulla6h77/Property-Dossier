# Property Dossier demo

Three live Manhattan lookups using NYC City Planning, the Department of Finance, and the Department of Buildings.

## 350 Fifth Avenue

**Parcel BBL** 1008350041

- Primary zoning district C5-3. [NYC City Planning](https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl=1008350041&%24select=bbl%2Caddress%2Czonedist1&%24limit=3)
- Assessment used to calculate taxes: 492,419,019. [NYC Department of Finance](https://a836-pts-access.nyc.gov/care/datalets/datalet.aspx?LMparent=20&UseSearch=no&jur=65&mode=asmt_fin_2027&pin=1008350041&taxyr=2027)
- DOB NOW approved permit M56697678-I1-PL for BIN 1015862. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1015862&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)
- DOB NOW approved permit M50738171-I1-EW-SP for BIN 1015862. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1015862&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)

Missing records in this lookup: flood, violation, school.

## 120 Broadway

**Parcel BBL** 1000477501

- Primary zoning district C5-5. [NYC City Planning](https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl=1000477501&%24select=bbl%2Caddress%2Czonedist1&%24limit=3)
- Assessment used to calculate taxes: 0. [NYC Department of Finance](https://a836-pts-access.nyc.gov/care/datalets/datalet.aspx?LMparent=20&UseSearch=no&jur=65&mode=asmt_fin_2027&pin=1000477501&taxyr=2027)
- DOB NOW approved permit M08048159-I1-GC for BIN 1001026. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1001026&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)
- DOB NOW approved permit M08044452-I1-EW-SP for BIN 1001026. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1001026&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)
- DOB NOW approved permit M08044442-I1-MS for BIN 1001026. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1001026&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)

Missing records in this lookup: flood, violation, school.

## 11 Madison Avenue

**Parcel BBL** 1008547501

- Primary zoning district C5-3. [NYC City Planning](https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl=1008547501&%24select=bbl%2Caddress%2Czonedist1&%24limit=3)
- Assessment used to calculate taxes: 0. [NYC Department of Finance](https://a836-pts-access.nyc.gov/care/datalets/datalet.aspx?LMparent=20&UseSearch=no&jur=65&mode=asmt_fin_2027&pin=1008547501&taxyr=2027)
- DOB NOW approved permit M08022212-I1-EW-SP for BIN 1088910. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1088910&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)
- DOB NOW approved permit M01443509-I1-PL for BIN 1088910. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1088910&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)
- DOB NOW approved permit M01443509-I1-EW-SP for BIN 1088910. [NYC Department of Buildings](https://data.cityofnewyork.us/resource/rbx6-tga4.json?bin=1088910&%24select=work_permit%2Cblock%2Clot%2Cborough%2Cbin&%24order=work_permit+DESC&%24limit=20)

Missing records in this lookup: flood, violation, school.

## Live permit monitoring

TinyMonitor checks the building-specific DOB permit feed for BIN 1015862 daily. The saved baseline and repeat check both show 18 unique permits. No new permit was observed in the two checks.

[Validation notes and monitor details](LIVE-VALIDATION.md)
