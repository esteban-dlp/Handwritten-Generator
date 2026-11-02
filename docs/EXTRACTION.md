# Extracting and reviewing handwriting

## General notes are valid input

Start with the user's existing notes; do not require a special alphabet worksheet. Inspect several pages, establish the page coordinate system, and identify reliable labeled examples. Existing notes contain natural variation but touching letters, skew, paper lines and ambiguous symbols make segmentation harder. A transcription helps but is not mandatory.

For better coverage, optionally suggest isolated characters on clean paper: write the desired character several times with space between samples, include uppercase/lowercase separately, and label uncommon symbols. Good scans should be straight, sharply focused and around 300 dpi. Vector PDFs often preserve cleaner boundaries. Never promise every letter can be recovered.

## Regions schema

Coordinates are PDF points in the top-left-origin, page-local coordinate system used by PyMuPDF. Pages are 1-based. Crop tightly around the full ink, including dots, accents and descenders. A region must contain exactly one Unicode character; do not infer `1` versus `l` or `O` versus `0` from shape alone.

```json
{
  "source_cell": 16,
  "regions": [
    {"character": "a", "page": 1, "rect": [20, 30, 28, 41]},
    {"character": ",", "page": 1, "rect": [42, 38, 45, 43]}
  ]
}
```

The agent or human prepares this map after inspecting the actual source. The extractor renders the labeled crops; it does **not** discover labels autonomously or run OCR. Repeated identical crops are deduplicated within a batch using character plus image hash. Similar-looking but non-identical crops still require review. It works on both vector and scanned PDF pages, but raster crops can include background/grid fragments. Avoid connected letters, or mark uncertain samples for rejection rather than inventing cuts. Normalize page rotation/scan skew before preparing coordinates.

```sh
manuscrito extract private/notes.pdf --regions private/regions.json --output private/candidates.json
manuscrito review private/candidates.json --output outputs/new-samples.html
manuscrito counts private/candidates.json
```

## Review and approval

Always provide (1) counts by character, (2) all samples including the existing approved set, and (3) only new candidates. HTML review can be generated directly. For PDF delivery use your agent's document export tool to export the review HTML/count report, checking pagination and actual appearance. Clearly identify the batch and stable IDs in all reports.

The HTML gallery lets the user uncheck individual samples. **Download approved library** produces a JSON file of retained samples; the page does not write to the original library. It works entirely locally without a server. Record rejected IDs in a local rejection ledger.

Do not replace an existing library with a new-only download. Back up the current approved library, then merge approved candidates into its `characters` object by character and stable ID. Preserve `source_cell` compatibility: rescale geometric widths/heights when source units differ. Deduplicate by full crop content, preserve provenance, and generate updated reports. Require explicit user approval before promoting candidates. There is no arbitrary per-character cap unless requested.

## Library schema

```json
{"source_cell":16,"characters":{"a":[{"id":"stable-id","width":8,"height":11,"png":"BASE64_PNG","source":"notes.pdf","page":1,"rect":[20,30,28,41],"status":"approved"}]}}
```

Images are embedded for a portable local review. They are personal data: never commit the JSON, review HTML, or outputs without permission. Keep original input PDFs unchanged. The MIT software license does not grant rights to someone else's handwriting.
