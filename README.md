# MyOTA identity service

The administrative permission catalogue includes `operations.read` for the
read-only NATS/JetStream status/history page and `observability.view` for
operational status. These can be assigned to custom roles without granting
global administration or domain-write access. Neither is granted automatically
to ordinary participants. The operations API validates signed access tokens;
the browser never receives broker or database credentials.

MyOTA is a programme-agnostic platform for outdoor activation programmes. MPOTA is represented as a configured programme, not as the platform itself. No rules or charter text are copied from POTA or any other programme: every programme supplies its own configuration, policy, eligibility, awards and public charter.

This repository owns amateur-radio-aware accounts and authentication. It is
independent of Keycloak and does not treat an external OIDC provider as the
source of truth. The service owns accounts/persons, operator/SWL
participation, one primary callsign plus additional callsigns, verification
lifecycle, roles/scopes, sessions, recovery, privacy, security events, and
optional per-programme OIDC mappings.

## What works now

- Amateur-radio-aware identity: operator/SWL participation, multiple callsigns, one primary callsign, lifecycle and verification fields.
- The identity service does not own programmes, entities, activity/QSOs,
  awards, or admin-web presentation; those boundaries are defined in the
  [repository map](https://github.com/myota-platform/myota-docs/blob/main/docs/repository-map.md).
- The current slice includes login, registration, account administration,
  callsign verification fields, scoped roles, privacy export/deactivation,
  and security-event primitives.

Account administration also exposes the Phase 1 resource aliases: `PATCH
/v1/identity/accounts/{accountId}`, `PATCH
/v1/identity/roles/{roleCode}`, `PUT
/v1/identity/accounts/{accountId}/role-assignments`, and `PUT
/v1/identity/accounts/{accountId}/primary-callsign`. The older action routes
remain compatibility aliases. See the [Phase 1 API resource update record](https://github.com/myota-platform/myota-docs/blob/main/docs/api-phase1-resource-updates.md).

The unit-test adapter can run in memory. Durable Compose/Kubernetes operation
uses PostgreSQL through the platform/deployment configuration and requires
explicit production secrets; do not use the test adapter as a production
data store.

## Run the vertical slice

```bash
python3 -m unittest discover -s tests -v
python3 services/dev_server.py
```

Open the identity service health endpoint on port 8001 when running the local
slice. For durable data, use the Compose stack in myota-deploy with Colima.

The remaining Internet-facing identity gates are listed in the [charter gap
analysis](https://github.com/myota-platform/myota-docs/blob/main/docs/charter-gap-analysis.md),
including production key management, abuse controls, user self-service, and
security review.

The durable runtime also exposes aggregate identity metrics at `/metrics` for
users, participation type, callsigns, roles, security events and locked
accounts. OpenTelemetry request telemetry is enabled by the deployment
configuration rather than by the unit-test adapter.

## Architecture

Read the [MyOTA charter](https://github.com/myota-platform/myota-docs/blob/main/docs/project-charter.md)
for the platform purpose and policy boundaries. MPOTA remains sample data
only; this service must support any programme without inheriting another
programme's rules.

## Source project

The original `ea7klk/mpota` repository remains untouched. Its charter and planned flows are treated as the migration source; see [`docs/migration-from-mpota.md`](docs/migration-from-mpota.md).
