# Property Dossier tasks

Criterion and requirement IDs refer to [SPEC.md](SPEC.md). This checklist plans implementation and validation.

## Prerequisites

- [x] Record the official submission requirements, approval criteria, and judging priorities.
- [ ] Confirm product access, endpoint contracts, live test authorization, and sufficient quota. Resolve or document the open decisions in SPEC.md.
- [ ] Keep setup, configuration, dependencies, and verification project-local.

## Implementation and approval checks

- [ ] **A1** Resolve the input to the correct parcel and retrieve live records from at least three official sources through TinyFish. Verify the source of every item.
- [ ] **A2** Validate permits, zoning, tax history, flood zone, violations, and nearby schools against their official sources. Test mismatched parcel IDs and conflicting dates.
- [ ] **A3** Support arbitrary addresses within the declared coverage. Test three different addresses and exercise parcel-number input, ambiguous addresses, and locations outside coverage.
- [ ] **A4** Distinguish missing records, no matching records, inaccessible sources, and ambiguous parcel identity. Verify that none yields invented results.
- [ ] **A5** Generate both JSON and a readable report with item-level links and distinct official record types beyond a map or listing lookup. Compare the JSON and report for consistency.
- [ ] Test Monitor's association of a permit or change with the selected parcel and rejection of an unrelated address change.

## Demo and submission

- [ ] Show at least three addresses using official sources. Include a case with missing records and show the monitoring workflow.
- [ ] Run the edge-case and security checks in SPEC.md. Capture reproducible live evidence separately from fixture results.
- [ ] Review every submission requirement (S1, S2, S3, S4, S5) and approval criterion before marking the build ready.
- [ ] Prepare setup instructions, the working build link, notes explaining TinyFish's role, the required LinkedIn post tagging TinyFish, and the Discord #showcase share. Obtain publication authorization before posting.
- [ ] Verify the evidence and submit by Tuesday, November 17, 2026 at 11:59 PM Pacific (Wednesday, November 18 at 12:59 PM Pakistan time).
