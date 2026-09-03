# Onboarding and recovery

Design first-run behavior and failure behavior separately from the normal route.

## Onboarding contract

Document only setup that is actually required:

- runtime or CLI availability and how to detect it;
- required environment variables or credentials, without printing their values;
- first-run initialization and writable locations;
- external service permissions and expected response;
- the shortest command or action that verifies readiness.

The happy path should attempt the normal operation directly when possible. Do not make every invocation repeat a full configuration audit. If setup fails, identify the missing item, give the smallest repair, and state whether retrying is safe.

## Recovery matrix

| Failure | Diagnose | Recovery | Continue? |
| --- | --- | --- | --- |
| malformed input | name the field/format and show accepted shape | correct only the input | no, until fixed |
| missing dependency | identify command/runtime/package | install or configure through the user's approved environment | after verification |
| authentication/credential | identify the variable or permission, never the secret | configure securely and retry the failed step | only if retry is safe |
| network/external service | preserve request/state and report provider error | retry with bounded attempts or resume | yes when idempotent |
| script/tool failure | retain stderr and the affected artifact | repair the local step or ask for intervention | do not discard prior work |
| irreversible action | stop before mutation | request explicit confirmation | only after approval |

Do not claim a dependency is installed, a credential is valid, or a remote action succeeded without observable evidence. Avoid unbounded retries and never log secrets.
