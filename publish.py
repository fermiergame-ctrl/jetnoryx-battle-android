"""Only this binary-only public repository; no private sources, signing secrets or Cloudflare."""
import json,subprocess,pathlib,os
REPO='fermiergame-ctrl/jetnoryx-battle-android'
def gh(*args):return subprocess.check_output(['gh',*args],text=True).strip()
if os.environ.get('GITHUB_REPOSITORY')!=REPO:raise SystemExit('Wrong distribution repository')
repo=json.loads(gh('api','repos/'+REPO))
if repo['private']:raise SystemExit('Public standard runners required; never run this job in the private game repository')
m=json.loads(pathlib.Path('release-input/manifest.json').read_text());tag='android-'+str(m['versionCode'])
releases=json.loads(gh('api','repos/'+REPO+'/releases?per_page=100'))
for r in releases:
 if not r['draft'] and r['tag_name'].startswith('android-') and int(r['tag_name'][8:])>m['versionCode']:raise SystemExit('Do not publish a versionCode older than the public version')
existing=next((r for r in releases if r['tag_name']==tag),None)
if existing and not existing['draft']:
 asset=next((a for a in existing['assets'] if a['name']=='JetNoryx-Battle.apk'),None)
 if not asset or asset.get('digest')!='sha256:'+m['sha256']:raise SystemExit('Existing public APK differs; increase versionCode instead of replacing it')
 print('The same immutable release is already public')
else:
 if not existing:
  notes='BÊTA Android : essais sur téléphones physiques à poursuivre.\n\nTélécharger le fichier APK ci-dessous et l’installer sur Android 7 ou plus. Pour une mise à jour, installer par-dessus sans désinstaller ni effacer les données.\n\nAPK signé, version '+m['versionName']+'. SHA-256 : '+m['sha256']+'\n\nAucun compte GitHub nécessaire pour télécharger. Dix cartes classiques ; les deux cartes secrètes restent réservées au Web. Le jeu Web reste indépendant.'
  pathlib.Path('release-notes.txt').write_text(notes)
  gh('release','create',tag,'--repo',REPO,'--draft','--target',os.environ['GITHUB_SHA'],'--title','JetNoryx Battle Android '+m['versionName'],'--notes-file','release-notes.txt')
 # Drafts do not resolve through the public /releases/tags endpoint.
 # Resolve the draft once from the authenticated list and use its numeric ID.
 release=next(r for r in json.loads(gh('api','repos/'+REPO+'/releases?per_page=100')) if r['tag_name']==tag)
 asset=next((a for a in release['assets'] if a['name']=='JetNoryx-Battle.apk'),None)
 if not asset or asset.get('size')!=m['bytes'] or asset.get('digest')!='sha256:'+m['sha256']:
  gh('release','upload',tag,'release/JetNoryx-Battle.apk','--repo',REPO,'--clobber')
 release=json.loads(gh('api','repos/'+REPO+'/releases/'+str(release['id'])));asset=next(a for a in release['assets'] if a['name']=='JetNoryx-Battle.apk')
 if asset['size']!=m['bytes'] or asset.get('digest')!='sha256:'+m['sha256']:raise SystemExit('GitHub asset integrity not confirmed; keep the draft')
 gh('api','--method','PATCH','repos/'+REPO+'/releases/'+str(release['id']),'-F','draft=false','-f','make_latest=true')
print('Public signed APK ready for anonymous verification')
