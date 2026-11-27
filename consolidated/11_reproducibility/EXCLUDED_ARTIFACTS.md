# Artifacts left out of the archive

*Generated; do not edit.*

| division | file | bytes | reason | git object | SHA-256 |
|---|---|---:|---|---|---|
| structbio | `experiments/structbio/gmec_dev/certs/v2-lib/1UBQ.mincert.json` | 10035244 | larger-than-5-MiB | `1ec678294f77494990a20ccc0f74b4ec48270b17` | `0c9dfbd9392ec930eeddf41ef53ff7a475d09237782e83ecd5f422c242a1ad79` |
| structbio | `experiments/structbio/gmec_dev/certs/v2/1UBQ.mincert.json` | 15901276 | larger-than-5-MiB | `f6c18f9d8192a0379985737fa2221ad3e7306267` | `f1250c338d0fc8342d6c2cf8995fdbde1f15f091064c1a6e6dc9d5b54a981954` |
| frontier | `experiments/frontier/freezes/FRONTIER-FRZ-0002_heldout_commitment_v1/sealed_list_v1.enc` | 2736 | sealed-evaluation-material | `562e85f0682b82616f81d6ab263a5eaaeeb87e84` | not computed (file not read) |

Rules: sealed evaluation material is never copied and never read; files larger than 5 MiB, caches and build products are referenced, not copied.  Every file listed is unchanged in the repository and is retrieved with

```
git clone https://github.com/Tommaso-R-Marena/MetricChain.git && cd MetricChain
git show <pinned commit of the division>:<file> > <local name>
sha256sum <local name>
```

Not part of any branch, and therefore not referenced here: untracked caches that divisions describe as regenerable (their reports say how), tool installations, and the credentials of the sealed list (held by the research owner).
