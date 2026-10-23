"""Vérifie la fermeture des dépendances. --apply republie uniquement les objets de production existants.

Exécuter depuis un environnement Azure CLI déjà authentifié dans le bon abonnement.
Ne crée ni infrastructure, ni secret, ni rôle, ni exécution. Ne démarre aucun trigger.
"""
import argparse,json,subprocess,os
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--apply',action='store_true')
args=parser.parse_args()
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
if args.apply:
    m['factory']=os.environ['AZURE_DATA_FACTORY_RESOURCE_URL'].rstrip('/')
index={(x['kind'],x['name']):x for x in m['definitions']}
types={'LinkedServiceReference':'linkedservices','DatasetReference':'datasets',
       'DataFlowReference':'dataflows','PipelineReference':'pipelines'}
seen=set();order=[]
def refs(x):
    if isinstance(x,dict):
        if x.get('type') in types and x.get('referenceName'):
            yield types[x['type']],x['referenceName']
        for v in x.values():yield from refs(v)
    elif isinstance(x,list):
        for v in x:yield from refs(v)
def visit(key):
    if key in seen:return
    if key not in index:raise ValueError('Définition absente : '+str(key))
    seen.add(key)
    for dep in refs(json.loads((root/index[key]['path']).read_text())):visit(dep)
    order.append(key)
visit(('pipelines','PL_00_ORCHESTRATE_CERTIFIED_V2'))
for kind,name in order:
    path=root/index[kind,name]['path']
    if kind=='linkedservices':
        print('REQUIRED_EXISTING',kind,name)
        # Garder les connexions sécurisées configurées dans la factory.
        if args.apply:
            subprocess.run(['az','rest','--method','get','--url',
                m['factory']+'/'+kind+'/'+name+'?api-version=2018-06-01','-o','none'],check=True)
        continue
    print('APPLY' if args.apply else 'CHECK',kind,name)
    if args.apply:
        # Vérifier l'existence avant PUT : aucun nouvel objet inattendu.
        url=m['factory']+'/'+kind+'/'+name+'?api-version=2018-06-01'
        subprocess.run(['az','rest','--method','get','--url',url,'-o','none'],check=True)
        subprocess.run(['az','rest','--method','put','--url',url,'--body','@'+str(path),'-o','none'],check=True)
print('Définitions vérifiées. Aucun secret, rôle, trigger ou watermark modifié par ce script.')
