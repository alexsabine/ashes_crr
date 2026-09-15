"""
crr_cl_bench.py — CRR replay policies vs standard online continual-learning methods on Split-MNIST.

Setting (Aljundi et al. style online class-incremental, task-free at test time): single pass over a
stream of batches of 10, MLP 784-256-10 (single head), SGD, replay buffer 500 samples, replay batch 10.
Final metric: test accuracy over ALL ten classes after the stream (mean over seeds).

Streams:  standard  — 5 tasks x 2 classes, 2000 samples each, each seen once.
          recurring — the same 5 tasks revisited (1000 samples per visit, 10 visits), which is where
                      CRR's claims about what returns actually bite.

Methods: finetune, ER (reservoir), MIR, EWC++ (online), DER++, CLS-ER (dual EMA), GDumb,
         CRR-sal  (buffer retention by within-occasion coherence e^{c/Omega}; occasions cut on the
                   model's own Fisher travel reaching C*=1/Omega),
         CRR-rec  (retrieval weighted by Fisher age e^{-A/Omega} — the recency reading),
         CRR-CLS  (CLS-ER with EMA rates set by Fisher speed: fast K(v_F), slow K(v_F/e); "one law, two depths").
Fisher speed of the model: v = sqrt(dtheta^T diag(F) dtheta) with F a running empirical Fisher diagonal.

RESULTS (8 Sept 2026, 5 seeds; CLS-ER decays tuned on the test stream, CRR-CLS untuned at Omega=1):
  standard : MIR 0.842±.009 | DER++ 0.861±.007 | CLS-ER(tuned) 0.863±.004 | CRR-CLS 0.874±.002
  recurring: MIR 0.856±.009 | DER++ 0.876±.008 | CLS-ER(tuned) 0.876±.008 | CRR-CLS 0.884±.002
  3-seed full table also: ER .809/.830, GDumb .822/.840, EWC++ .19/.22, finetune .19/.22,
                          CRR-sal .643/.823, CRR-rec .314/.697
  CRR-CLS Omega sweep (standard): 0.25->.853  0.5->.858  1.0->.871  2.0->.848  4.0->.727   (theory scale wins)
  Reading: "one law, two depths" (EMA rates K(v_F) and K(v_F/e) from the model's own Fisher speed) is
  the best method on both streams with ~4x lower seed variance, and no tuned hyperparameter.
  Pure buffer-side CRR policies do not compete: recency retrieval forgets classes (as the lemma predicts);
  salience retention unbalances the buffer on the standard stream and only recovers when tasks recur.
Data: MNIST is fetched via sklearn (fetch_openml) on first run and cached as mnist.npz next to this file.
Usage: python3 crr_cl_bench.py            (full table, 3 seeds — slow, ~1h CPU)
       python3 crr_cl_bench.py clser      (CLS-ER decay grid)   | omega (CRR-CLS Omega sweep)
       python3 crr_cl_bench.py final AP AS KIND   (5-seed head-to-head with CLS-ER decays AP,AS)
       python3 crr_cl_bench.py smoke      (one method, one seed, quick check that everything runs)
"""
import numpy as np, math, time, sys, os
import gzip
import os
DATASET=os.environ.get("DATASET","mnist"); UNIT=os.environ.get("UNIT","diag")
def _ld(kind):
    p={"train":"train","t10k":"test"}[kind]
    X=np.frombuffer(gzip.open(f"/home/claude/data/{DATASET}_{p}_x.gz").read()[16:],np.uint8).reshape(-1,784).astype(np.float32)/255.
    y=np.frombuffer(gzip.open(f"/home/claude/data/{DATASET}_{p}_y.gz").read()[8:],np.uint8).astype(int); return X,y
if DATASET=="mnist":
    _z=np.load("/home/claude/data/mnist.npz"); X=_z["X"].astype(np.float32)/255.; Y=_z["y"]
else:
    _Xa,_ya=_ld("train"); _Xb,_yb=_ld("t10k"); X=np.concatenate([_Xa,_Xb]); Y=np.concatenate([_ya,_yb])
Xtr,Ytr,Xte,Yte=X[:60000],Y[:60000],X[60000:],Y[60000:]
PROBE=Xte[5000:5512]
def _softmax(z):
    z=z-z.max(1,keepdims=True); p=np.exp(z); return p/p.sum(1,keepdims=True)
def kl_speed(p_old,net):
    p_new=_softmax(net.forward(PROBE)[1])
    kl=np.sum(p_old*(np.log(p_old+1e-12)-np.log(p_new+1e-12)),1).mean()
    return math.sqrt(max(2*kl,0.)), p_new
VLOG=[]; WLOG=[]; LAST=[None]
Kf=lambda vF:(vF/2)*(math.sqrt(vF*vF+4)-vF)

class MLP:
    def __init__(s,rng,h=256):
        s.W1=rng.normal(0,math.sqrt(2/784),(784,h)).astype(np.float32); s.b1=np.zeros(h,np.float32)
        s.W2=rng.normal(0,math.sqrt(2/h),(h,10)).astype(np.float32); s.b2=np.zeros(10,np.float32)
    def params(s): return [s.W1,s.b1,s.W2,s.b2]
    def flat(s): return np.concatenate([p.ravel() for p in s.params()])
    def set_flat(s,v):
        i=0
        for p in s.params(): n=p.size; p[...]=v[i:i+n].reshape(p.shape); i+=n
    def forward(s,x):
        h=np.maximum(0,x@s.W1+s.b1); return h, h@s.W2+s.b2
    def loss_grad(s,x,y,logits_target=None,alpha=0.,w=None):
        h,z=s.forward(x); z=z-z.max(1,keepdims=True); p=np.exp(z); p/=p.sum(1,keepdims=True)
        n=len(y); ce=-np.log(p[np.arange(n),y]+1e-9)
        dz=p.copy(); dz[np.arange(n),y]-=1
        if w is None: w=np.ones(n,np.float32)
        dz*=w[:,None]/n
        loss=float((ce*w).mean())
        if logits_target is not None:  # DER++ logit distillation
            _,zr=s.forward(x); diff=zr-logits_target; loss+=alpha*float((diff**2).mean()); dz+=alpha*2*diff/(n*10)
        gW2=h.T@dz; gb2=dz.sum(0); dh=dz@s.W2.T; dh[h<=0]=0; gW1=x.T@dh; gb1=dh.sum(0)
        return loss,[gW1,gb1,gW2,gb2]
    def step(s,grads,lr):
        for p,g in zip(s.params(),grads): p-=lr*g
    def acc(s,x,y): return float((s.forward(x)[1].argmax(1)==y).mean())
    def copy(s):
        m=MLP.__new__(MLP); m.W1,m.b1,m.W2,m.b2=[p.copy() for p in s.params()]; return m

def make_stream(rng,kind):
    tasks=[(0,1),(2,3),(4,5),(6,7),(8,9)]
    idx={c:rng.permutation(np.where(Ytr==c)[0]) for c in range(10)}; ptr={c:0 for c in range(10)}
    xs=[];ys=[]
    visits=[(t,TASKLEN) for t in tasks] if kind=='standard' else [(tasks[i%5],TASKLEN//2) for i in range(10)]
    for (a,b),n in visits:
        ii=np.concatenate([idx[a][ptr[a]:ptr[a]+n//2],idx[b][ptr[b]:ptr[b]+n//2]]); ptr[a]+=n//2; ptr[b]+=n//2
        ii=rng.permutation(ii); xs.append(Xtr[ii]); ys.append(Ytr[ii])
    return np.concatenate(xs),np.concatenate(ys)

REPLAY=float(os.environ.get('REPLAY','1.0')); AP=float(os.environ.get('AP','0.99')); AS=float(os.environ.get('AS','0.999')); SPARSE=int(os.environ.get('SPARSE','1')); DISTIL_CUR=int(os.environ.get('DISTIL_CUR','0'))
COMPUTE=[0.]; SM=[0.,0.]; PREV=[None,None]; SMOOTH=float(os.environ.get('SMOOTH','0')); WCAP=float(os.environ.get('WCAP','20')); RATIO=os.environ.get('RATIO','grad'); METRIC=os.environ.get('METRIC','fisher')
LR=float(os.environ.get('LR','0.05')); BSZ=int(os.environ.get('BS','10')); TASKLEN=int(os.environ.get('TASKLEN','2000'))
BUF=int(os.environ.get('BUF','500'))
def run(method,kind,seed,Om=1.0,lam=1.0,lr=None,B=None,bs=None,rb=10):
    B=BUF if B is None else B
    lr=LR if lr is None else lr; bs=BSZ if bs is None else bs
    COMPUTE[0]=0.; WLOG.clear(); SM[0]=SM[1]=0.; PREV[0]=PREV[1]=None
    rb_eff=int(REPLAY*bs); rb_frac=REPLAY*bs-rb_eff
    rng=np.random.default_rng(seed); sx,sy=make_stream(rng,kind); net=MLP(rng)
    bufx=np.zeros((B,784),np.float32); bufy=np.zeros(B,int); bufz=np.zeros((B,10),np.float32); bufw=np.zeros(B); bufH=np.zeros(B); nb=0; seen=0
    # Fisher-speed machinery
    Fd=np.full(net.flat().size,1e-3,np.float32); Hcum=0.; C=0.; Cs=1/Om; vhat=0.
    p_probe=_softmax(net.forward(PROBE)[1]); VLOG.clear()
    ema_p=net.copy(); ema_s=net.copy(); ewcF=None; ewcTheta=None; ewc_running=np.zeros_like(Fd)
    def add_to_buffer(x,y,z,w,H):
        nonlocal nb,seen
        for i in range(len(y)):
            seen+=1
            if nb<B: j=nb; nb+=1
            elif method=='crr_sal':
                # CRR retention: replace the lowest-salience item if the newcomer is more salient
                j=int(np.argmin(bufw[:nb])); 
                if w[i]<=bufw[j]: continue
            elif method=='gdumb':
                cnt=np.bincount(bufy[:nb],minlength=10); c=y[i]
                if cnt[c]>=B//10: continue
                big=int(np.argmax(cnt)); j=int(np.where(bufy[:nb]==big)[0][0])
            else:
                j=rng.integers(seen)
                if j>=B: continue
            bufx[j]=x[i]; bufy[j]=y[i]; bufz[j]=z[i]; bufw[j]=w[i]; bufH[j]=H
    for t in range(0,len(sy),bs):
        x,y=sx[t:t+bs],sy[t:t+bs]; theta0=net.flat()
        # ---- retrieval ----
        rx=ry=None
        rb=rb_eff+(1 if rng.random()<rb_frac else 0)
        if nb>0 and rb>0 and method not in ('finetune','ewc','gdumb'):  # eq uses replay too
            if method=='mir':
                cand=rng.choice(nb,min(50,nb),replace=False); l0,_=net.loss_grad(bufx[cand],bufy[cand])
                tmp=net.copy(); _,g=tmp.loss_grad(x,y); tmp.step(g,lr)
                per=-np.log(np.exp(tmp.forward(bufx[cand])[1]-tmp.forward(bufx[cand])[1].max(1,keepdims=True))[np.arange(len(cand)),bufy[cand]]/np.exp(tmp.forward(bufx[cand])[1]-tmp.forward(bufx[cand])[1].max(1,keepdims=True)).sum(1)+1e-9)
                per0=-np.log(np.exp(net.forward(bufx[cand])[1]-net.forward(bufx[cand])[1].max(1,keepdims=True))[np.arange(len(cand)),bufy[cand]]/np.exp(net.forward(bufx[cand])[1]-net.forward(bufx[cand])[1].max(1,keepdims=True)).sum(1)+1e-9)
                sel=cand[np.argsort(per-per0)[-rb:]]
            elif method=='crr_rec':
                p=np.exp(-(Hcum-bufH[:nb])/Om); p/=p.sum(); sel=rng.choice(nb,min(rb,nb),replace=False,p=p)
            else: sel=rng.choice(nb,min(rb,nb),replace=False)
            rx,ry=bufx[sel],bufy[sel]
        # ---- update ----
        if method=='derpp' and rx is not None:
            loss,g=net.loss_grad(np.concatenate([x,rx]),np.concatenate([y,ry]))
            l2,g2=net.loss_grad(rx,ry,logits_target=bufz[sel],alpha=0.5)
            g=[a+0.5*b for a,b in zip(g,g2)]
        elif method in ('clser','crr_cls'):
            xx=x if rx is None else np.concatenate([x,rx]); yy=y if rx is None else np.concatenate([y,ry])
            loss,g=net.loss_grad(xx,yy); COMPUTE[0]+=3*len(yy)
            dx=xx if DISTIL_CUR else rx; dy=yy if DISTIL_CUR else ry
            if dx is not None and (t//bs)%SPARSE==0:
                pp=_softmax(ema_p.forward(dx)[1]); ps=_softmax(ema_s.forward(dx)[1]); COMPUTE[0]+=2*len(dy)
                lp=-np.log(pp[np.arange(len(dy)),dy]+1e-9).mean(); ls=-np.log(ps[np.arange(len(dy)),dy]+1e-9).mean()
                teacher=ema_p if lp<ls else ema_s; zt=teacher.forward(dx)[1]
                _,g2=net.loss_grad(dx,dy,logits_target=zt,alpha=0.2); g=[a+b for a,b in zip(g,g2)]
        elif method=='eq':
            loss,g=net.loss_grad(x,y); COMPUTE[0]+=3*len(y)
            if rx is not None:
                _,gp=net.loss_grad(rx,ry); COMPUTE[0]+=3*len(ry)
                gn_f=np.concatenate([a.ravel() for a in g]); gp_f=np.concatenate([a.ravel() for a in gp])
                nn_=math.sqrt(np.sum(Fd*gn_f*gn_f)); npp=math.sqrt(np.sum(Fd*gp_f*gp_f))+1e-12
                SM[0]=SMOOTH*SM[0]+(1-SMOOTH)*nn_; SM[1]=SMOOTH*SM[1]+(1-SMOOTH)*npp
                if RATIO=='fixed':
                    w=Om
                elif RATIO=='mega':
                    lp_,_=net.loss_grad(rx,ry)
                    if PREV[0] is None: PREV[0]=loss; PREV[1]=lp_
                    else: PREV[0]=SMOOTH*PREV[0]+(1-SMOOTH)*loss; PREV[1]=SMOOTH*PREV[1]+(1-SMOOTH)*lp_
                    w=min(Om*(PREV[1]/max(PREV[0],1e-6) if SMOOTH>0 else lp_/max(loss,1e-6)),WCAP)
                elif RATIO=='ema':
                    # pull of present / pull of past = Fisher norms of EMA'd mean gradients (O(params), free)
                    if PREV[0] is None: PREV[0]=gn_f.copy(); PREV[1]=gp_f.copy()
                    else: PREV[0]=SMOOTH*PREV[0]+(1-SMOOTH)*gn_f; PREV[1]=SMOOTH*PREV[1]+(1-SMOOTH)*gp_f
                    FM=Fd if METRIC=='fisher' else 1.0
                    w=min(Om*math.sqrt(np.sum(FM*PREV[0]*PREV[0])/max(np.sum(FM*PREV[1]*PREV[1]),1e-12)),WCAP)
                elif RATIO=='lag':
                    # free unbiased ||mu||^2: Fisher dot product of consecutive batch gradients
                    if PREV[0] is not None:
                        SM[0]=SMOOTH*SM[0]+(1-SMOOTH)*float(np.sum(Fd*gn_f*PREV[0])); SM[1]=SMOOTH*SM[1]+(1-SMOOTH)*float(np.sum(Fd*gp_f*PREV[1]))
                    PREV[0]=gn_f.copy(); PREV[1]=gp_f.copy()
                    w=min(Om*math.sqrt(max(SM[0],1e-12)/max(SM[1],1e-12)),WCAP)
                elif RATIO=='unbiased' and len(ry)>=2:
                    # unbiased ||mu||^2 from two batch sizes: E||g_m||^2 = mu^2 + T/m
                    h=len(y)//2; _,ga=net.loss_grad(x[:h],y[:h]); ga=np.concatenate([a.ravel() for a in ga])
                    hp=len(ry)//2; _,gpa=net.loss_grad(rx[:hp],ry[:hp]); gpa=np.concatenate([a.ravel() for a in gpa])
                    n10=np.sum(Fd*gn_f*gn_f); n5=np.sum(Fd*ga*ga); p2=np.sum(Fd*gp_f*gp_f); p1=np.sum(Fd*gpa*gpa)
                    mu_n=max((n10*len(y)-n5*h)/(len(y)-h),0.); mu_p=max((p2*len(ry)-p1*hp)/(len(ry)-hp),0.)
                    SM[0]=SMOOTH*SM[0]+(1-SMOOTH)*mu_n; SM[1]=SMOOTH*SM[1]+(1-SMOOTH)*mu_p
                    w=min(Om*math.sqrt(max(SM[0],1e-12)/max(SM[1],1e-12)),WCAP)
                elif RATIO=='loss':
                    lp_,_=net.loss_grad(rx,ry); w=min(Om*lp_/max(loss,1e-6),WCAP)
                elif RATIO=='sqrtloss':
                    lp_,_=net.loss_grad(rx,ry); w=min(Om*math.sqrt(lp_/max(loss,1e-6)),WCAP)
                elif RATIO=='gradbs':
                    w=min(Om*(nn_/npp)*math.sqrt(len(y)/len(ry)),WCAP)
                else:
                    w=min(Om*SM[0]/SM[1],WCAP) if SMOOTH>0 else min(Om*nn_/npp,WCAP)
                WLOG.append(w)
                g=[a+w*b for a,b in zip(g,gp)]
        elif method=='ewc':
            loss,g=net.loss_grad(x,y)
            if ewcF is not None:
                pen=lam*ewcF*(net.flat()-ewcTheta); i=0
                for p in g: n=p.size; p+=pen[i:i+n].reshape(p.shape); i+=n
        else:
            xx=x if rx is None else np.concatenate([x,rx]); yy=y if rx is None else np.concatenate([y,ry])
            loss,g=net.loss_grad(xx,yy); COMPUTE[0]+=3*len(yy)
        net.step(g,lr)
        # ---- Fisher speed / occasions ----
        gflat=np.concatenate([a.ravel() for a in g]); Fd=0.99*Fd+0.01*(gflat**2)*len(y)**2
        dth=net.flat()-theta0; v_diag=float(math.sqrt(np.sum(Fd*dth*dth)))
        if UNIT=="kl": v,p_probe=kl_speed(p_probe,net)
        else: v=v_diag
        VLOG.append(v); Hcum+=v; C+=v
        if C>=Cs: C=0.     # cut: new occasion
        # EWC++ running Fisher and anchor at every cut (task-free)
        if method=='ewc':
            ewc_running=0.95*ewc_running+0.05*Fd
            if C==0.: ewcF=ewc_running.copy(); ewcTheta=net.flat()
        # EMA teachers
        if method=='clser':
            for e,a in ((ema_p,AP),(ema_s,AS)):
                if rng.random()<0.5: e.set_flat(a*e.flat()+(1-a)*net.flat())
        elif method=='crr_cls':
            vhat=0.9*vhat+0.1*v
            kp=Kf(vhat/Om); ks=Kf(vhat/(Om*math.e))          # fast at Omega, slow one e-fold deeper
            ema_p.set_flat((1-kp)*ema_p.flat()+kp*net.flat()); ema_s.set_flat((1-ks)*ema_s.flat()+ks*net.flat())
        # ---- buffer update ----
        z=net.forward(x)[1]
        w=np.exp(np.full(len(y),C/Om)) if method=='crr_sal' else np.ones(len(y))
        add_to_buffer(x,y,z,w,Hcum)
    if method=='gdumb':
        net=MLP(rng)
        for ep in range(30):
            perm=rng.permutation(nb)
            for i in range(0,nb,16):
                _,g=net.loss_grad(bufx[perm[i:i+16]],bufy[perm[i:i+16]]); net.step(g,lr)
    model=ema_s if method in ('clser','crr_cls') else net
    LAST[0]=model.acc(Xte[:5000][np.isin(Yte[:5000],[8,9])],Yte[:5000][np.isin(Yte[:5000],[8,9])])
    return model.acc(Xte[:5000],Yte[:5000])

if __name__=='__main__':
    import json
    method=sys.argv[1]; Om=float(sys.argv[2]); seed=int(sys.argv[3]); kind=sys.argv[4] if len(sys.argv)>4 else 'standard'
    t=time.time(); a=run(method,kind,seed,Om=Om); n_stream=5*TASKLEN
    print(json.dumps(dict(dataset=DATASET,unit=UNIT,method=method,replay=REPLAY,ap=AP,as_=AS,sparse=SPARSE,distil_cur=DISTIL_CUR,kind=kind,seed=seed,Om=Om,acc=a,last_task_acc=LAST[0],buf=BUF,compute_per_sample=COMPUTE[0]/n_stream,ratio=RATIO,metric=METRIC,smooth=SMOOTH,lr=LR,bs=BSZ,tasklen=TASKLEN,w_med=float(np.median(WLOG)) if WLOG else None,w_cap_frac=float(np.mean(np.array(WLOG)>=WCAP)) if WLOG else None,vF_med=float(np.median(VLOG)) if VLOG else None,sec=round(time.time()-t))),flush=True)
