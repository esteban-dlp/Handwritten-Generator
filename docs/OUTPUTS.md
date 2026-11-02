# Output versions and local history

The portable CLI creates sequential output directories under the requested output root. Each contains document.html, document.pdf and manifest.json with hashes and configuration. Existing versions are not replaced. Source PDFs, personal configurations and libraries belong under private/; all generated content belongs under outputs/. Both are excluded by the repository allowlist.

In the original author's local workspace only, a previous organization pass archived legacy outputs in outputs/versiones/v001, retained working files in outputs/trabajo and linked outputs/actual to the archive. Those private historical files and their compatibility links are not part of this public repository. They are not needed for installation.
