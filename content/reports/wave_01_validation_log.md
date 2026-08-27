# Wave 01 検証ログ

```text
python scripts/validate_content.py

entries: 1000
status: {'reviewed': 90, 'draft': 910}
warnings: 0
errors: 0
content validation passed
```

```text
python scripts/build_content.py --output preview/content_reviewed_wave01.py

wrote 90 entries
revision: sha256:cfd99efd8e7549047ef87afb2dae43cd7a937e0c79a489931a5b8baae4d35500
```

```text
apply script idempotence

pre-check: pending=50 (expected failure)
first apply: changed=50
post-check: already_applied=50
second apply: changed=0, already_applied=50
```

```text
python -m compileall scripts

passed
```
