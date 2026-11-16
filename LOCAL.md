# Local workflow

Resolve one parcel, retain source-backed record types, flag missing categories, and compare permit identifiers.

Requires Python 3.10 or later. From this project folder:

```powershell
python main.py example.json --report
``

The example uses synthetic input. Output marked `offline_input` comes from supplied files.

## Provider entry point

Set `TINYFISH_API_KEY` in the process environment. The provider entry point uses TinyFish's documented service endpoints. Live verification is pending.

`python tinyfish.py lookup.json` runs one bounded Agent lookup per configured source, then Fetch corroborates the parcel ID and excerpt. Supply `subject`, `official_hosts`, and `sources` as an array of objects with `url`. `--watch-permits` explicitly creates a recurring watch on a corroborated permit page. Verify that the selected page actually shows parcel-level updates before using it as bounty evidence.

Select a real coverage area, wire Agent and Fetch to at least three sources, and connect Monitor to parcel-scoped permit changes.

Start with `python tinyfish.py nyc-demo.json --dry-run`. This preset targets a public commercial building and uses NYC Finance, City Planning, and DOB's published open dataset. The broad permit dataset is a lookup entry point. Only enable a watch after identifying a parcel-scoped result URL and checking its baseline. Expand to two more addresses after this first parcel passes.

If a lookup times out, use the TinyFish run history to find the existing run before retrying. Use `--reuse-run HOST RUN_ID` for a run that used the same source and lookup goal. The CLI reads that run instead of starting another lookup for the host. Repeat the option for multiple saved runs.

## NYC parcel workflow

For NYC, resolve the address to its borough-block-lot (BBL) and building identification number (BIN) using [NYC GeoSearch](https://geosearch.planninglabs.nyc/). Confirm the borough and house number when multiple addresses are returned.

```powershell
python nyc.py 1008350041 1015862 --tax-year 2027 --start-agent
python nyc.py 1008350041 1015862 --tax-year 2027 --agent-run RUN_UUID
```

Save the returned run ID. The second command reads that run and uses TinyFetch to check the parcel against City Planning's PLUTO dataset, Finance's assessment roll, and the Department of Buildings' approved permit dataset. It imports only permit IDs found by both Agent and Fetch for the exact building and parcel. A condo billing lot that differs from the permit lot requires an official cross-reference and is left unresolved by this workflow.
