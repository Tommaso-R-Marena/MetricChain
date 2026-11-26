import proofs.CertificateAlgebra
/-! Workstream P7 (science division): smoke test.  Runs the theory division's `verify` (their definition, from
`proofs/CertificateAlgebra.lean`, unchanged) with `#eval` on their own frustrated-triangle certificate. -/
open MetricChain
#eval verify triangleCert triangle (fullDom 3 2) 1   -- expected: true
#eval verify triangleCert triangle (fullDom 3 2) 2   -- expected: false
