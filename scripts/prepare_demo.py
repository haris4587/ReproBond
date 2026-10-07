"""Print exact commit-pinned arguments for the synthetic Studio demonstration."""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

commit = sys.argv[1]
assert re.fullmatch('[0-9a-f]{40}', commit)
def fp(name):
    path = Path('evidence/fixtures') / name
    body = path.read_bytes()
    return {'url': f'https://raw.githubusercontent.com/haris4587/ReproBond/{commit}/{path.as_posix()}',
            'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}
terms = {'title': 'Synthetic pendulum replication demonstration', 'paper': fp('original.md'),
    'hypothesis': 'Mean period between 1.90 and 2.10 seconds', 'protocol': 'Three trials, ten complete oscillations per trial',
    'methodology': '1.00 metre string; 5 degree angle; manual stopwatch. This bounty explicitly evaluates synthetic educational records.',
    'allowed_deviations': 'Manual stopwatch and length uncertainty up to 1 cm', 'disallowed_deviations': 'Different string length or large release angle',
    'report_fields': 'Apparatus, length, angle, timing method, all three durations, mean period, deviations, conclusion and limitations',
    'minimum_evidence': 'One complete synthetic report with raw timings and limitations. Synthetic values are accepted for this educational bounty; video and real laboratory certification are not required.'}
print(json.dumps({'terms_json': json.dumps(terms, separators=(',', ':')),
    'evidence_json': json.dumps([fp('negative-replication.md')],separators=(',', ':')),
    'deadline': int(datetime.now(timezone.utc).timestamp()) + 7200, 'bond': 0, 'source_limit': 1},indent=2))
