"""Publish one signed APK from internal upload data. Players never assemble anything."""
from pathlib import Path
import json,hashlib,re,sys,zipfile
APP_ID='com.fermiergame.jetnoryxbattle'
CERT='f9c5870261d9799007a2015652d662a60481801e662f77f4c7fd28b47a03f5ed'
def assemble(root:Path,output:Path|None=None):
 m=json.loads((root/'manifest.json').read_text())
 if m.get('applicationId')!=APP_ID or m.get('certificateSha256')!=CERT:raise ValueError('Application identity changed')
 if type(m.get('versionCode')) is not int or m['versionCode']<60002:raise ValueError('Invalid versionCode')
 if m.get('assetName')!='JetNoryx-Battle.apk' or not re.fullmatch('[a-f0-9]{64}',m.get('sha256','')):raise ValueError('Invalid APK metadata')
 if not m.get('parts') or len(m['parts'])>64:raise ValueError('Missing/too many input files')
 if m.get('webOnlyMapsExcluded') is not True or m.get('classicMaps')!=10 or m.get('storageOrigin')!='https://localhost':raise ValueError('Wrong Android map/storage capabilities')
 digest=hashlib.sha256();size=0;seen=set()
 if output:output.parent.mkdir(parents=True,exist_ok=True)
 target=output.open('wb') if output else None
 try:
  for item in m['parts']:
   name=item['file']
   if not re.fullmatch(r'payload/[0-9]{3}\.bin',name) or name in seen:raise ValueError('Unsafe/repeated input path')
   seen.add(name);p=root/name
   if p.is_symlink() or not p.is_file():raise ValueError('Missing/unsafe input')
   part=hashlib.sha256();part_size=0
   with p.open('rb') as f:
    while data:=f.read(1024*1024):
     part.update(data);digest.update(data);size+=len(data);part_size+=len(data)
     if target:target.write(data)
   if part_size!=item['bytes'] or part.hexdigest()!=item['sha256']:raise ValueError('Input integrity failed')
  if size!=m['bytes'] or digest.hexdigest()!=m['sha256']:raise ValueError('APK integrity failed')
 except BaseException:
  if target:target.close();output.unlink(missing_ok=True)
  raise
 finally:
  if target:target.close()
 if output:
  with zipfile.ZipFile(output) as z:
   for name in z.namelist():
    if 'jetnoryx_map_secrete_' in name:raise ValueError('Web-only image in Android APK')
    if name.startswith('assets/public/assets/') and name.endswith(('.js','.css')):
     for marker in [b'jetnoryx_map_secrete_',b'secret.map1',b'secret.map2']:
      if marker in z.read(name):raise ValueError('Web-only map code in Android APK')
   config=json.loads(z.read('assets/capacitor.config.json'))
   if config.get('appId')!=APP_ID or config.get('server',{}).get('hostname')!='localhost' or config['server'].get('androidScheme')!='https' or config['server'].get('url'):raise ValueError('Wrong native storage origin')
 return m
if __name__=='__main__':
 m=assemble(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else None);print(json.dumps({k:m[k] for k in ['assetName','versionCode','sha256','bytes']}))
