# Responsible data and AI use

This GitHub repository is PUBLIC. Do not add confidential industry datasets,
personal data, credentials, unpublished partner requests, notebook outputs
containing secrets, or derived figures/models that may disclose restricted
information. Obtain explicit data-owner permission before posting partner
datasets or findings publicly.

NASA POWER gridded temperature estimates and optional Meteostat station data are downloaded to Git-ignored `data/private/` by default.
Accompanying provenance JSON records the requested place or station, dates, retrieval time and data source. These files do not establish independent validation or homogeneous trends. NASA POWER estimates represent grid cells; Meteostat station records may have large historical gaps and incomplete underlying-provider licensing.

The offline temperature example is **fully synthetic**; even a statistically
significant fitted “trend” from that dataset is not scientific evidence about
Dar es Salaam or East Africa.

AI assistants can help explain, debug and test code, but students must verify
generated code, challenge modelling assumptions, and document which claims
are supported by actual data. Never paste restricted industry material into
an external AI system without authorization.

Licenses: code [MIT](LICENSE), original teaching material
[CC BY 4.0](LICENSE-CONTENT.md), datasets [separately](DATA_LICENSES.md).


## Synthetic insurance backup

The [insurance backup](projects/insurance-claims/README.md) generates an entirely
**fictional establishment-level dataset** in memory. The names, records, claim
frequencies, training-programme associations and accounting costs are
fabricated. They do **not** originate from WCF, TIRA, any insurance partner, or
any real institution. The fake costs are arbitrary units, **not TZS**.

The generator and notebook are suitable for public GitHub. Do not substitute
actual claims, policyholder records, workers' personal information, or
identifiable organizational data in the public notebook or in external AI
prompts. Publication of real project results still requires separate approval.
