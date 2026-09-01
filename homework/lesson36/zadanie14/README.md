# Lekcja 36 – Zadanie 14

## Disaster Recovery – S3 Cross-Region Replication i RDS Snapshot

W zadaniu skonfigurowano podstawowe mechanizmy Disaster Recovery (DR) w AWS.

### S3

Bucket źródłowy:

- Nazwa: `python-course-lesson35-stanislaw`
- Region: `eu-central-1`

Bucket DR:

- Nazwa: `python-course-lesson35-stanislaw-dr`
- Region: `eu-west-1`

Na obu bucketach włączono Versioning.

Skonfigurowano S3 Cross-Region Replication (CRR):

```text
eu-central-1
    |
    | Cross-Region Replication
    v
eu-west-1
