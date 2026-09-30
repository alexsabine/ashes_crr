import sys, re, subprocess, os, time, html
S='/tmp/claude-0/sec_an_src/src'
def get(url,fn):
    for k in range(4):
        r=subprocess.run(['curl','-sSL','-m','180','-A','Mozilla/5.0 (research; sec_an)','-o',fn,'-w','%{http_code}',url],capture_output=True,text=True)
        if r.stdout=='200' and os.path.getsize(fn)>1000: return True
        time.sleep(5)
    print('FAIL',url,r.stdout,r.stderr[:200]); return False
for aid in sys.argv[1:]:
    absf=f'{S}/abs_{aid}.html'
    if not os.path.exists(absf): get(f'https://arxiv.org/abs/{aid}',absf); time.sleep(2)
    t=open(absf,encoding='utf-8',errors='replace').read()
    vers=re.findall(r'<strong>(?:<a[^>]*>)?\[v(\d+)\](?:</a>)?</strong>\s*(.*?)\s*\(',t,re.S)
    cur=max(int(v) for v,_ in vers) if vers else None
    title=html.unescape(re.sub(r'\s+',' ',re.search(r'<h1 class="title mathjax"><span class="descriptor">Title:</span>(.*?)</h1>',t,re.S).group(1))).strip()
    comm=re.search(r'<td class="tablecell comments mathjax">(.*?)</td>',t,re.S)
    jref=re.search(r'<td class="tablecell jref">(.*?)</td>',t,re.S)
    pdf=f'{S}/pdf_{aid}v{cur}.pdf'
    if not os.path.exists(pdf): get(f'https://arxiv.org/pdf/{aid}v{cur}',pdf); time.sleep(2)
    txt=pdf[:-4]+'.txt'
    if not os.path.exists(txt) and os.path.exists(pdf):
        subprocess.run(['uv','run','-q','--with','pymupdf','python','-c',f"import pymupdf;d=pymupdf.open('{pdf}');open('{txt}','w').write(''.join(p.get_text() for p in d))"])
    print(aid,f'v{cur}','|'.join('v'+v+' '+' '.join(d.split()[1:4]) for v,d in vers),'|',title[:90],'| C:',html.unescape(re.sub('<.*?>','',comm.group(1))).strip()[:100] if comm else '-','| J:',html.unescape(re.sub('<.*?>','',jref.group(1))).strip()[:80] if jref else '-', os.path.getsize(txt) if os.path.exists(txt) else 'NOTXT')
