import json, re, sys, unicodedata, difflib
OFF=32.0
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]','',s)
W=json.load(open('work/words_whisper.json'))
# merge "R" ".E" ".T." into one token
ww=[]
for w in W:
    if ww and re.fullmatch(r'\.?[A-Z]\.?',w['w']) and re.fullmatch(r'R(\.?[A-Z]\.?)*',ww[-1]['w'].replace('.','') or 'x'):
        ww[-1]['w']+=w['w']; ww[-1]['end']=w['end']; continue
    ww.append(dict(w))
phrases=[]
for line in open('lyrics.txt',encoding='utf-8'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    toks=[]
    for tok in line.split():
        kind='plain'
        if tok.startswith('**'): kind='zoom'
        elif tok.startswith('*'): kind='red'
        elif tok.startswith('{'): kind='censor'
        raw=tok.replace('*','').replace('{','').replace('}','')
        disp=raw
        if kind=='censor':
            m=re.match(r'([A-Za-zÀ-ú])[A-Za-zÀ-ú]*(.*)',raw); disp=m.group(1)+'*'+m.group(2)
        toks.append({'text':disp,'kind':kind,'n':norm(raw)})
    phrases.append(toks)
L=[t for p in phrases for t in p]
a=[t['n'] for t in L]; b=[norm(w['w']) for w in ww]
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1): L[i1+k]['t']=ww[j1+k]['start']; L[i1+k]['e']=ww[j1+k]['end']
    elif tag=='replace' and (i2-i1)==(j2-j1):
        for k in range(i2-i1): L[i1+k]['t']=ww[j1+k]['start']; L[i1+k]['e']=ww[j1+k]['end']
    elif tag=='replace' and j2>j1:
        t0=ww[j1]['start']; t1=ww[j2-1]['end']; n=i2-i1
        for k in range(n): L[i1+k]['t']=t0+(t1-t0)*k/n; L[i1+k]['e']=t0+(t1-t0)*(k+1)/n
# interpolate missing
for i,t in enumerate(L):
    if 't' not in t:
        p=max([j for j in range(i) if 't' in L[j]],default=None); q=min([j for j in range(i+1,len(L)) if 't' in L[j]],default=None)
        tp=L[p]['e'] if p is not None else L[q]['t']-0.3; tq=L[q]['t'] if q is not None else tp+0.3
        idx=[j for j in range(len(L)) if (p is None or j>p) and (q is None or j<q)]
        k=idx.index(i); t['t']=tp+(tq-tp)*k/len(idx); t['e']=tp+(tq-tp)*(k+1)/len(idx)
# fix stretched first words of a phrase: whisper pins them early after a pause
pos=0
for p in phrases:
    if len(p)>1:
        f,n=p[0],p[1]
        if '.' not in f['text'] and n['t']-f['t']>max(0.45,0.12*len(f['text'])+0.3):
            f['t']=n['t']-min(0.5,max(0.2,0.07*len(f['text']))); f['e']=n['t']
    pos+=len(p)
out=[]
for p in phrases:
    out.append({'start':round(p[0]['t']-OFF,3),'end':round(p[-1]['e']-OFF,3),
                'words':[{'text':t['text'],'kind':t['kind'],'t':round(t['t']-OFF,3)} for t in p]})
json.dump(out,open('work/lyrics_timed.json','w'),ensure_ascii=False,indent=1)
for o in out: print(f"{o['start']:6.2f}-{o['end']:6.2f} "+' '.join(f"{w['text']}@{w['t']:.2f}" for w in o['words']))
