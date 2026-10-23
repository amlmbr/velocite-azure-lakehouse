"""Validate the 40 exported JSON definitions and their ADF references offline."""
import json
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'manifest.json').read_text())
objects={(d['kind'],d['name']):json.loads((root/d['path']).read_text()) for d in m['definitions']}
assert len(objects)==40
types={'LinkedServiceReference':'linkedservices','DatasetReference':'datasets','DataFlowReference':'dataflows','PipelineReference':'pipelines'}
missing=[]
def check(x):
 if isinstance(x,dict):
  if x.get('type') in types and x.get('referenceName'):
   ref=(types[x['type']],x['referenceName'])
   if ref not in objects:missing.append(ref)
  for v in x.values():check(v)
 elif isinstance(x,list):
  for v in x:check(v)
for obj in objects.values():
 assert 'properties' in obj
 check(obj)
assert not missing,missing
trigger=objects['triggers','TR_DAILY_PARIS_V2']['properties']
assert trigger.get('runtimeState')=='Stopped'
print('PASS',len(objects),'definitions;',dict(Counter(k for k,n in objects)),'; no missing references; trigger Stopped')
