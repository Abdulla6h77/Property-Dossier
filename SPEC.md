# Property Dossier specification

Source: `D:\tinyfish-details.md`, bounty 7 and its rulebook.

API or agentic app that combines live official records for an address or parcel and monitors property changes.

## TinyFish products

**Required: TinyFish Agent, Fetch, and Monitor.** Use Agent and Fetch for official retrieval and Monitor for address-level changes such as new permits. Explain the role of each.

## Official submission requirements

- **S1** Takes an address (or parcel number) as input
- **S2** Pulls records from at least three official sources (city, county, state or national sites)
- **S3** Outputs a structured dossier (JSON plus a readable report) with every item linked to its source
- **S4** Demo on at least three addresses
- **S5** Short explanation of how TinyFish Agent, Fetch and Monitor are used

## Official approval criteria

- **A1** TinyFish does the core retrieval on live official sites
- **A2** Records are accurate to the source
- **A3** Works for any address in the areas you support, not a hardcoded few
- **A4** Missing records are flagged clearly rather than guessed
- **A5** Goes beyond a single listing page or a map lookup

## Official judging priorities

- **J1** Sources: how many official sources it pulls from, and how well it combines them
- **J2** Accuracy: every record matches its source, with a link to prove it
- **J3** Coverage: works across many addresses and areas, not a handful
- **J4** Honesty: gaps and missing records are flagged, never guessed
- **J5** Monitor adds real value, e.g. alerting on a new permit at or near the address

## Demo and acceptance tests

Show at least three addresses using official sources. Include a case with missing records and show the monitoring workflow.

- **A1** Resolve the input to the correct parcel and retrieve live records from at least three official sources through TinyFish. Verify the source of every item.
- **A2** Validate permits, zoning, tax history, flood zone, violations, and nearby schools against their official sources. Test mismatched parcel IDs and conflicting dates.
- **A3** Support arbitrary addresses within the declared coverage. Test three different addresses and exercise parcel-number input, ambiguous addresses, and locations outside coverage.
- **A4** Distinguish missing records, no matching records, inaccessible sources, and ambiguous parcel identity. Verify that none yields invented results.
- **A5** Generate both JSON and a readable report with item-level links and distinct official record types beyond a map or listing lookup. Compare the JSON and report for consistency.

Additional test for the required monitoring workflow: Test Monitor's association of a permit or change with the selected parcel and rejection of an unrelated address change.

## Edge cases and security

Avoid reproducing private or identifying details from registry records in demos. Preserve source access restrictions. Test unit numbers, address normalization, boundary cases, rate limits, and stale sources.

Keep credentials, access tokens, and other people's personal data out of the build and demo. Use sanitized fixtures for failure tests and label fixture evidence separately from live evidence.

## Rulebook and submission deadline

- Deadline: Tuesday, November 17, 2026 at 11:59 PM Pacific (Wednesday, November 18 at 12:59 PM Pakistan time).
- Enter through the TinyFish Students or Ambassadors program. One person per build and one entry per person per bounty. Claims do not reserve a bounty, and submissions are final.
- Provide a working build link (repo, live demo, or cookbook PR) with notes on what it does and how TinyFish is used. Post about the build on LinkedIn and tag TinyFish. Share it in Discord #showcase. X is optional.
- Pass every approval criterion. Use original work built for the bounty and demonstrate meaningful live TinyFish work end to end across varied inputs. Keep the submitted evidence authentic.
- The general endpoint rubric awards 50/100/150/200 points for 1/2/3/4+ meaningful endpoints (Search, Fetch, Agent, Browser, Monitor). Each endpoint must contribute to the workflow.

## Open questions and dependencies

Choose the initial supported area based on available official sources. The brief does not define 'nearby' for schools or permits or state whether a live change must be captured for the demo.
