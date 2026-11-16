# NYC live validation

The NYC workflow checks zoning through [City Planning PLUTO](https://data.cityofnewyork.us/d/64uk-42ks), assessments through the [Department of Finance](https://www.nyc.gov/assets/finance/jump/bbl_lookup.html), and approved permits through [DOB NOW open data](https://data.cityofnewyork.us/d/rbx6-tga4). TinyAgent reads the exact building permit query. TinyFetch verifies the permit identifiers and joins records with the official parcel. The [local guide](LOCAL.md#nyc-parcel-workflow) shows how to rerun the workflow.

| Address | BBL | BIN | Live result |
| --- | --- | --- | --- |
| 350 Fifth Avenue, Manhattan | 1008350041 | 1015862 | Two permits, primary zoning district and tax assessment. City Planning lists the parcel's primary address as 338 Fifth Avenue. |
| 120 Broadway, Manhattan | 1000477501 | 1001026 | Three permits, primary zoning district and tax assessment. |
| 11 Madison Avenue, Manhattan | 1008547501 | 1088910 | Three permits, primary zoning district and tax assessment. |

The reports flag flood, violation and school records as missing. The full provider outputs are private in `.local`. The report contains only selected property facts.

## Permit monitor

[Permit monitor](https://agent.tinyfish.ai/monitors/11f38a66-33fe-4748-8fad-6ab1929c253c) watches the NYC DOB permit feed filtered to BIN 1015862. Its initial baseline had an upstream proxy failure. A manual baseline and repeat then completed successfully and showed the same 18 unique permit IDs. No new permit was observed in those two checks.

TinyFish confirmed the monitor active on `0 3 * * *` (03:00 UTC daily). At the published rate, this costs about $0.15 per 30 days if all checks complete. [Monitor pricing and scheduling](https://www.tinyfish.ai/blog/how-to-use-tinymonitor)
