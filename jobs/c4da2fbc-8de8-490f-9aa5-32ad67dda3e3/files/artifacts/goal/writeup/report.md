# Kekborn Genesis — corrected snapshot and contribution release

**The final package contains 6,610 holder rows, 3,868 counted jobs, 1,990.5 IMD of proven payments, and recomputed scores, tiers and genetics for every holder.** Both snapshot files are byte-for-byte unchanged. No deployment, mint, signature, purchase or spending was performed.

Upstream: [goal-3400-kekborn-genesis-snapshot-scoring at e58c6a7e71dba55cbc65ca27d5519acc143a35de](https://github.com/identity-md-launches/goal-3400-kekborn-genesis-snapshot-scoring/tree/e58c6a7e71dba55cbc65ca27d5519acc143a35de). **The corrected release is that immutable tree plus the capsule below.** The upstream commit is unchanged; this report carries the corrections.

Start with the [pinned archive](https://codeload.github.com/identity-md-launches/goal-3400-kekborn-genesis-snapshot-scoring/tar.gz/e58c6a7e71dba55cbc65ca27d5519acc143a35de). The decoder verifies its 171 files, copies them into a new directory, applies saved deltas, rebuilds jobs.csv from saved evidence and verifies every output hash. **The scores.csv delta contains the final assignments**; decoding does not run the scorer or use the network. The 175-file package includes every requested dataset/document, sources/, decisions.json and the offline scorer.

**Fixed snapshot and holdings.** T = 2026-11-25T11:00:00Z; only orders created strictly before T qualify. Each chain uses its last block at or before T.

| Chain | Block | UTC block time | RPC tag |
| --- | ---: | --- | --- |
| Ethereum, 1 | 26491756 | 2026-11-25T10:59:59Z | `0x1943b6c` |
| Robinhood, 4663 | 122989778 | 2026-11-25T11:00:00Z | `0x754acd2` |

holders.csv merges 4,840 Ethereum and 2,131 Robinhood holders, with 361 overlapping addresses. Supplies are 4,210,819.525771 and 71,170.146452 IMD respectively. It preserves exact raw/per-chain balances and retains pools, contracts and dust. snapshot.json preserves both token addresses and block hashes.

**Jobs, payments and evidence.** jobs.csv retains 17,028 source jobs and explicit reasons for 9,366 unlinked jobs. Its 3,868 counted holder roots comprise 3609 completed, 151 abandoned, 107 failed and 1 ongoing. Category totals retain all 113 unknown jobs. Goal children and panels count once; paid continuations stay distinct; shared payments count once. The 1,881 roots with only job-time evidence stay linked but unscored.

Intake execution state and payment confirmation are now separate. All 79 wrongly excluded orders had paid status, pre-T admission, successful receipts and 0.5-IMD transfers. Another 472 paid orders were counted as jobs but omitted from spending. Their 275.5 IMD brings proven spending to 1,990.5 IMD across 3,873 distinct transfers. Three confirmed orders remain unmatched and add no spend.

The omitted oracle shard now has **516 successful detail/result pairs**, read 2026-11-25T17:28:32.686Z through 2026-11-25T17:48:18.497Z. sources/revision/job-details.json and job-results.json save the scoring fields and UTC read times. Original failure records remain as history. Newly available blocked reasons refine abandoned-versus-failed classification; execution states remain read-time observations.

For [job 0011ea8f-dce3-4a06-9b61-41bb5d8067b8/result](https://api.imd.fun/jobs/0011ea8f-dce3-4a06-9b61-41bb5d8067b8/result), the response explicitly says `"complete":true` and names artifacts/answer.json, hash `837b90cdafbfea756c8da098474912f89644cd56b153013338e22e1223f82e3f`. Its corrected row has one accepted implement node, zero revisions, accepted share 1 and complexity 3. Result completion does not imply oracle attestation or semantic correctness.

**Scoring and rarity.** Let L(x,c)=min(1,ln(1+max(x,0))/ln(1+c)). The score is rounded to four decimals:

`25L(C,50) + 15L(P,100) + 10sqrt(D/6) + 15L(X,500) + 15L(R,50) + 10L(Q,50) + 10L(G,5)`.

C=completed jobs; P=verified IMD spent; D=known-category diversity; X=completed-work complexity; R=successful completed deliverables; Q=accepted-node shares; G=paid goals. Balance adds no points; missing signals add zero. methodology.md specifies all rules; tools/scores/score.py recomputes every row offline and --check compares bytes.

Weighted Fisher–Jenks minimizes within-class squared deviations of positive scores; 6,149 zeros join Common. Equal scores never split. Upper bounds are inclusive and preceding bounds exclusive for higher tiers. No percentage quota is used.

| Tier | Upper score | Wallets |
| --- | ---: | ---: |
| Common | 23.1886 | 6352 |
| Uncommon | 35.8868 | 124 |
| Rare | 52.3704 | 70 |
| Epic | 71.9484 | 43 |
| Legendary | 94.1773 | 21 |

Genetics follow methodology.md's requested category-to-trait mapping. All counted jobs remain in the denominator; unknown grants no trait. The review's 12-job wallet now shows 83% unknown and 17% code/contracts. Unknown-only wallets explicitly show unknown 100%: no trait. Goals combine dominant known traits.

**Validation and limits.** All six findings reproduced: the original --check failed, its own recomputation changed 159 scores/28 tiers/37 genetics, and its manifest had 24 stale hashes plus 42 omissions. After all corrections, 163 scores, 36 tiers and 37 strings differ from upstream. Wallet 0xe33ab493249a2df0d8c4a71ac54f46d1f7778367 changes from 51.8586/Epic to **82.8472/Legendary**.

The decoded release passes exact holders/jobs/scores rebuild checks, 29 normalization tests, scorer regressions, order-evidence checks and independent reconciliation of every wallet's score, spending, genetics, tiers and all 174 manifest entries. Both archival tags are corrected in data-accessibility.md. History limits remain below.

Seven newest-100 order histories remain truncated; 1,840 candidate transactions lack intake logs and three intake responses lack orders. Robinhood historical totalSupply and all 25 balance samples were unavailable: 27 replay windows matched, 11 were unavailable; independent samples had zero matches and three unavailable. Current supply cannot establish historical balances. Seats and API states are read-time observations; current ownership does not establish historic worker credit. New oracle projections omit full objectives, HTTP bodies and per-output hashes to fit this report, while retaining all scoring inputs. methodology.md and data-accessibility.md explain the limits and verification alternatives.

Provenance: supplied b01 snapshot, b02 collection/build results and b03 repairs, with their source files retained. Each batch item addressed one named piece and its result files/checks; no new batch is proposed. decisions.json is one object with notes and finish=true. Corrected root documents supersede historical worker reports.

| Package file | SHA-256 |
| --- | --- |
| snapshot.json | `b94dc67d27bc6aaa49811431ee68a3fd25d6c90f09de8fde0f1920792d7dd425` |
| jobs.csv | `3480dddde70ba6b612c874377f586040bd7f05ee5d3863ce879651042523ca1c` |
| scores.csv | `e953c846150678df6518b8b4b6bf79850cd81d51aad1589810f778c787bb093c` |
| manifest.json | `5bad1921fe2bb07eebf08337794ffb3763d2b48e8f320823ec60d1e5a9151759` |

**Recover the files.** Save this Python block as decode.py and run `python3 decode.py PINNED_CHECKOUT NEW_DIRECTORY report.md`; the output directory must not exist. Then run `python3 -B tools/revision/check.py` and `python3 -B tools/scores/score.py --check` there. No network or external Python package is required.

```python
import base64,csv,hashlib,io,json,lzma,pathlib,re,shutil,subprocess,sys
base,out,report=map(pathlib.Path,sys.argv[1:4])
def compact(v):return json.dumps(v,separators=(',',':'),ensure_ascii=False).encode()
def sha(v):return hashlib.sha256(v).hexdigest()
def safe(p):
 q=pathlib.PurePosixPath(p)
 if q.is_absolute() or '..' in q.parts:raise ValueError('Unsafe package path')
 return q
encoded=re.search(r'```kekborn-capsule\n(.*?)\n```',report.read_text(),re.S).group(1)
packed=base64.b85decode(''.join(encoded.split()))
expected=re.search(r'Capsule SHA-256: `([a-f0-9]{64})`',report.read_text()).group(1)
if sha(packed)!=expected:raise ValueError('Capsule hash mismatch')
capsule=json.loads(lzma.decompress(packed))
paths=capsule['base']
inventory=[]
for p in paths:
 safe(p);inventory.append([p,sha((base/p).read_bytes())])
if sha(compact(inventory))!=capsule['baseDigest']:raise ValueError('Wrong or modified upstream tree')
def strings(v):
 if isinstance(v,str):yield v
 elif isinstance(v,list):
  for x in v:yield from strings(x)
 elif isinstance(v,dict):
  for k,x in v.items():yield k;yield from strings(x)
refs=sorted({s for p in capsule['referenceSources'] for s in strings(json.loads((base/p).read_text())) if len(s)>12})
def expand(v):
 if isinstance(v,dict):
  if set(v)=={'$'}:return refs[v['$']]
  return {k:expand(x) for k,x in v.items()}
 if isinstance(v,list):return [expand(x) for x in v]
 return v
capsule=expand(capsule)
if out.exists():raise ValueError('Choose a new output directory')
out.mkdir(parents=True)
for p in paths:
 target=out/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(base/p,target)
def patch(v,edits):
 for op in edits:
  path=op[0]
  if not path:v=op[1];continue
  node=v
  for key in path[:-1]:node=node[key]
  if len(op)==1:del node[path[-1]]
  else:node[path[-1]]=op[1]
 return v
pending=[]
for p,mode,data,fmt,digest in capsule['changes']:
 safe(p);f=out/p;f.parent.mkdir(parents=True,exist_ok=True)
 if mode=='build_jobs':pending.append((p,digest));continue
 if mode=='lines':
  lines=f.read_text().splitlines(keepends=True)
  for a,b,replacement in reversed(data):lines[a:b]=replacement
  value=''.join(lines)
 elif mode=='csv':
  rows=list(csv.reader(io.StringIO(f.read_text())))
  for i,j,kind,val in data:
   rows[i][j]=json.dumps(patch(json.loads(rows[i][j]),val),sort_keys=True,separators=(',',':'),ensure_ascii=False) if kind=='j' else val
  stream=io.StringIO();csv.writer(stream,lineterminator='\n').writerows(rows);value=stream.getvalue()
 elif mode in ('json','jpatch'):
  obj=data if mode=='json' else patch(json.loads(f.read_text()),data)
  indent,ascii,nl=fmt
  value=json.dumps(obj,indent=indent,ensure_ascii=ascii,separators=(',',':') if indent is None else None)+nl
 elif mode=='text':value=data
 else:raise ValueError('Unknown package encoding')
 f.write_text(value,encoding='utf-8')
 if sha(f.read_bytes())!=digest:raise ValueError('Output hash mismatch: '+p)
for p,digest in pending:
 if p!='jobs.csv':raise ValueError('Unexpected rebuild target')
 subprocess.run([sys.executable,'-B',str(out/'tools/jobs/build_jobs.py'),'--root',str(out)],check=True)
 if sha((out/p).read_bytes())!=digest:raise ValueError('Rebuilt jobs hash mismatch')
meta=capsule['manifestMetadata']
allpaths=sorted((set(paths)|{c[0] for c in capsule['changes']})-{'manifest.json'})
meta['files']=[{'path':p,'bytes':(out/p).stat().st_size,'sha256':sha((out/p).read_bytes())} for p in allpaths]
f=out/'manifest.json';f.write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
if sha(f.read_bytes())!=capsule['manifestSha256']:raise ValueError('Manifest hash mismatch')
print('Decoded',len(allpaths)+1,'files; every output hash verified; snapshot unchanged.')
```

Capsule SHA-256: `58f34916b58679ebd600c2d4cad77df75e3f14678a4368a8488865c648339c6c`

```kekborn-capsule
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5>Jeh1%v}IIh>FIPQ;>$HV|^t%D99rDLIAYT$xg-lKvQqm(B0Fm{0@Jf^xvbDG$nPcbv(A>ww=n%N;(Y3ZpGThlcT3m
NufD@ZXPBOrGJ!soWaq896FoUb-ho5_Fjlq&bYcc-@{$r$_$UCqVT%Wa1nllF%nd<Y`_vEEnO6>nJ>GzsZmXxA_>T?S<MYx>k4%%R+I~M>U3hGek{ch-~!gN
t!Rdt%q^g+aCW%bU#w%np(!T1O1g0_(<N{m%Cg^b7q|jk$%L3>?@F5-fXN&aMjVwh{#ab`ep~(|EmoO@hkOn`6$~>CD?V+HuT0%u0(v5Twy7>KiugAx#?N+B
T6Rj7-t1uQ3#NMl!M{3G^8P74HW%TrA5J;uwvyzBTt0*T@jQxZE|_kQw^-NAkzPy4sFqRbu|P8F`VI=G7x>Ba7JmjW>4^EHWFc)JLd7F*?Tej{3}~~}M(cTU
7!>(G@}iR%e{Pm;^GuL`7fd(B1%8m!9tpKxzs38eTOfHEH~4{?TV3E9!b@j%*ooLb9dx!G;TJi6n>;k{zZ9urK7aZz`%LW9VqFKqy8j2G<=Gs~q6dr%WOK3K
h?vuaM@RW>;cD9QGXwTL_`;`bykRkQ-s8vs<nPJq9Qse7=NKSEEpn)r7$hT5)IIyDv9zR}n&|)Iw~$r-QpEg@VkTYT8^M!pmn?%BKvAhSf1w92^t0Hs_>dS4
LTEm0`6!YY?YhDzp<7i^+*0c-@qH(jwf}n~zA)+u1~F+rBOm+0aG+;Ds^0X;dE<|&ku;qI?mWvKZuuLSfYo3miI?&k?SD5tDhovs@U-ZnV;ATrf*&t;3_%i6
sL-2cOz67yKXn6T&>S|R<jyIu!44Eb!_EH1Wf0qzTu7TDO`?{o`NJ`yf`YlmML$lUSG$T6q;fvbqVjj1qK}2Ml1y5<Z$%rogWXSyRXf+*v!8-4%(8T?J7Qhn
wp$^BKEkPnY`N8$cfw_oN+N#^817LzfWN+~8;MH3#CO>X!M+}Zxk3La*n5!=o}^PDv6ii8c0A@CZt5zZ2PeSUS7^Hg0l?o!RTWvqYxXLA-(;JX?wU|Hlzp2w
GIx#D@w;o1IzRJ=)FOlH(n389+v39(pj&cCttt3Z5I+zTs53dBhu^Q+2#ovzRP)<B(f}nqi*#`Dm=L?U4Y!}l$n(HX+)hPm%Y^;8ZjbEb`NITmwI$todVz*C
p<gOWrnE2x7qz19%`&{W+yS%anB`>7Z!+&fm2V2Uw6|rov!SWuRU++n7&^?opp`aagXzuxqOJ)Y1a4XvTXg!wiHcKy=sAz;XC9Iyv^U7WyR<l&<mvEiK&lYA
@dCIqa~=1+w=Xbfrvnwz3RN9x5IGw5Dy_lot#E$q83#ZQF;j-bAEG$zlLAmWG^gME>z@C+7Vx?1g8d*~?LsI1K(yC(1H0S&B=4W8vx~u!T~nv`rS;Gf7Kd8b
bo!e4I-6M_DQXNk&O;sgv01uUb6I~-kOasxIbCMMqR`!uLLc(Mg+wGHfhe}3D;-}lrVdY9B8M21)_y2~5PQUqXQ`{|Zk4KC4lgycXSJhNRal0yzI4J{5H&(B
s9s?3kbhlF_S_V%&&I8VG9O^{f|g(Q`j6a4ToH~z(A+<QdP0u#xI3MwFu@n~9gkB$V63A<60avo#AWrxNDeA#$DWlw(+I$-$r;5ZI+2iyVG_}*e6LsZd6x<F
WNrx*<vncU>lWDM{oD%3<y4$5x4n)Kk>|D{m}K{4gHe9iGzB(y9H<_SNBceoeOBdj6SSGWjLnuX06i6=B$VZxm>ytyWA`vN!L+Mp>@^k3n?5<b^ouC5DogS=
L>3(YL1lSIr}7*5x_Sj>5Ch%S1Xh@BYxmPBG*m<^$cn_>!*4WYbZouR@SHDy%(+37-jFVco#rix{`Zy_NA+)<x$&(1)Pj7MaVJ=ll=<7+jOrKT8q$q?><G$Z
C<+RRt!`n>!096k7jbdL2K7kSyj5^c{`(bB{=J1n&8V1Q0H^duCoYi@xb6=#Obzfz{9wFLm$iG3RS$ssqzHv^G_EPWF;%zh*&7qCyXL9;axe=#amBz*@YUzG
<|Ql<({g6JI6_b494lP|$_4vR7MX~FxU==5P3IWu>7V8R6?LRfH?57~!+y-fLB#!a$JHzJ_tbNWm}p?#1EnU7R`d%zl{~rB=?yO@cUk}hzm*Fv)!!%Pa!Lg0
Xb}}3&lKa*am)b2WL$hBSXszJG1I{;fbv(C%`ydn>fC!AolVhv%*TWXt+!_>A+Jq7il1ar<=>KRC!R7{XeR<YxggMG=R}s3K!^K5-fPg!SAP$%{{v)|d94?8
7MxQv@@ziiZ2OB_Q>H+rRIysXeS`%=uGszWR`Vc}eZ)D8KhKs&y!A;M?j9^it&#+!F6wDi1|l)%sTx0s>I-AUAb$;hX=BTALL587cPVGt;fiU-^Dh17Xx>i6
Q9#YLV$}Zhl%lcu2aWPCVV9(+zbDo5v&{OBKO1fvr}TtTb&|!aK@Mc9dxS>VcqXYZ0&9lX`hv|$g+nXK`c53y@*Drh+ECuP7(xjV-J7|Iav{6^#N^n<*B1xn
SAXviYI_HBTz7;?fTVQB`J?;zR|SMd73X#hMbv|$!qZ~ZhKv9XhmP~WFpLP@-}UZ+jCoy$&nY`>E9gc5UpYQZa}|1Kk0Jc_(OBKC^lk9<z&e^E!`^yLW6D*s
eix!F#!Tn{+2>w+h5#HsfJKrmOR7-)h&ylia%NK@Vg$?=98eBv50<z~S!2$zbAz}mJ~%lb!1-qV3MW0xcs*LID)X&5P@?AMY45{~e`-H=4&{}t9Yx=alq>=h
^}05B#2m6T`8l}5y|7`=QnOusUi^lG?K*3`4`zqQ_f6sg46D)tc@Cx$b)vL3d~mn(hnih8{0wt+#hvira<_XHUr%aWK2ZoNM_Y((-j@f2n~=H*?_uKXj*-|g
vB!J3h4Ek=@DNlBOQ$)Ym0A`CZle1m+qk^MM7E;oCErSCb4$Y(n2_HUcL!;bi0r~1#k;cR>?g~t=91!ED0dTFE(xvB)R{WLVCOI?GNFC}$+2&!rSqDnwK|)=
a(hw`3nx5ahU1?K7PQk1pr*2>bvZm7P(Oo5l<IwLw}txZo?vH`M^1il3@&YJvx`a`f0F+`lQb#6hyZt(VkoWeR0FZ9coI35WyWIjlctArB9+ziY3%puT$t`-
H**0Nt@x&d%8WDbrmmk_-@yUVP;d->oJ&R!`#0!lC=|!vd_2@^J0mKjwe7)xL{c{-jF6-XD^Pdw1iuh4t09wpzJS~8P@I;j6I(_1X~CROcjbv=VOTNCE@W1i
&Wz84hg5jwDZ|;fX+zH|;-*@b<y@IxxzyW7Rm70zDkJpxID2LwkNp3|j<+gIetfoAchKQy4*{T$*sOH@g^WPHq=&35n84O_(ojF~oWFMC)(LO~6+Fo|{C720
<suSRfA>#aI<wPq=V^Oj<9>Dp9#ED-__>!(AZcy$`TeY4=3p(ZWuScJnxyh<q#}y_7D@!+chm_@oT6zYN*g+&+5-YPAmlwMd}MKlY6ur>%C}QYa5*SPG!GmY
IoNe6g*jtq$9fJUejx(LG2-SE@W5EBJj;zrsiXTUr62w1`bs|4I%Swot>Edb+K%1Dz0Jf38ry!sBkDK~$QLI2I3W}{nXLsiOj@WfQd?dELN1fEC^ZbySFD2d
80x;xOZ&*re@2jTe#?^Bs~Rf*x?%_Y0B<oZTD+vX@lf-H@R`%41?np_N>)xk#C0=lSgPP<glI7WaF7#{<Ntu#kyEF16?Nby++F!`m;xU98sPi2|K2%;?z~U_
d;bn!93;3mE?moz6WNXpmQTv|jq#Y_8DE@D&ovt*&2_MeR0}SNAf2C48I<fZQ?Lz-Wz8SZs&Nb1VFA@5X~+SLeFKua>VT_09pu)ZgEvQ5X(QcMcO0GS8mo35
M|5NKzg=C6N^0%*po^oaIp(JQs`A#j1icE%cH6~c0^T^=21fW)NvxD!VToEe9z7ZjzamI(f8P<(-`N^H!7R9zwk$qb&0Ui>&furag-hp_ihL382UR7bWvB$j
x^%m?;_bA0U@&8>j%15@$T(6X>GyQszO#Y^F{Q<EN#N}oNNK(&)c*(uuM&sSFYoC|M!AcWlri)EdSZyeZ#pzOWFjS)Qj-=?slfz2dl0_K9nA4X@J<2Oco9Gd
`d2S?E#ZrBV$9idV522rt&zPFTpI*~DYISj%_1UslSS%6f>PsO!x@6}vz(OeK96thEuCM_g5L%Z4&u9?=O|19)-%gxH+PS&LZeiKl1&>>n#2y|_gu?%YJ{*k
H2s_NDB@ro^vBXIUWhx<CCn{gT_+N5w)50==akC!DIYT^e_^`c?8kmSh|l>iDJn<=<ab|+LZe&QzB0B{;DenxoqpTPL;S=-ChuP!2M4)cN^2wTNP=oLX79re
?=7(mbmzyF=6HA5jwmSNYKqEdo)#AF#7Yy|>_Bs)wJf$nL%WVUj$+^Kwk3jY{b}&6fdTA>Ri>a41a39+3!}&M@d~jtagydEa@D?V4om=VMa1-5xG-Azsu~Jc
_Ea(0u8vGW5(Lu7D**l{n!HD#k&K79a=X%)9%ZB+J8?}<%I+3a3Dr$vUU)1qE+&~0?@GMwIi9)PD79GGx5v86s%#vWO}64Y*=GB`@7O(Wi6@SOk3{PP6qNk>
+u^1}VoQCCfj|92V^@9~3k@quH2%a*M)`PAG`b7J>n@|^2Nd)JD;v_*u0g>e6xTX5EodoPZvi2SbJpQa0$l@b>0s2~lN$E>SHV;E9hNZCL*-q`%RQ~iOEJNI
{7H<Dnn9VjgAyv{3*PAtNa0t|a^=DkZHu5~zJl4FLF~#HLQ&K~#z9!uX{E8@i~hSb8{$T1czJ3H`l8v&<aj8f3UBlv&W(okA}V+9_iu+FZaSGBT6|5RqZ0D~
1xTMfdLUK>d|J@kM3UsOCcHdT(ob$ky3IFQ)p8lkg*-I*5IGhl|JqNuP;QiVfii~R(%6E?Qgrk1yes<a{*}CkYA9^t#e|z80KN+N8@ypn@g~g+=9U|`q^fLy
m_UzEJf7)~E@R)zrLpMNk(@xb%5<gTh;z?&Btk*|DM~S%xkW6Y6To#~xJS;`xu-fLNjzGluLkoe&*ql9U`=%ro6X4gyBe6+9(c^PE(g)(`{WQ$_vMH~y%ZBv
VZ7oN*lqh`U6Tg@_0k!|MEk!IJ{J=b77LR2pvuB#mp-9Usix4M@u%aI?22;kXf)gx7Y#w90%iDK5jMt0V^5-Rs{PtR9EcH5Igq%GC)teg=CO8;0D3fDxfv{_
J3TxyiuZ2v#5hk@Y``{p?U~-a><}_1*|RykMVSbSpQK46d+J$B+$*`$VbqB(ri!>EtMv?i0F#u#0eQ*;Rjp%@DbQp6!cJL10;A87axJ78VxSV0bTeVraI(K4
sIKPJ98vico_K>)`_#s$rT7XM9qMaqW`=acc?hEHd{FJDGbpFia7nm^-isB*wYC1NrW@*N<t7qs|MXnQ(?jiV+Q{eYp?`!&+kltFMw$w>5m3|d3LRQIg{SRE
GaR@T3&fvu5Pjyxq8(qjQ8wJ%<R{=9D3F`OMtzj+=@1i8&A3=M`dZK!5$XUKnih8dj(X*)neeEeiSm#q_aCB`Kbi#{4fp_jlT2Ws-xdSEFIE^4*+0-3dK=1N
_cof8WmQ^UG)uN06|9|IeVA@mQ#S@(qD>o--x5aqFu2o52($?w#x`Y;N~faKQASH8G7-sf0+VxcIX~^1ts)9`*n7ZWJHh{KE&oCW{3Y4@kD0B}PhFPIb&-7O
Vm_YY^4~Q!70p5NYZhaOCN(k82#+ba0}mH@p^>@S$sxps0MflUJh5i9TzZE6_c{iXpN-)CV*+~zqL12yLel)>^ZMe){DG|thy^C8e#Lv%;!o4dV&8Q?7!Rzh
A*Ez|)NSUbY|IUX;06){U5DCgxl)Ho1av`xBV(|f+q7}X`*pO)Qr+&%gGt{#%q^}rQ%X|7x(?IaxBeA?Ob>ZEjT!9G`&!w!#2Buf0AkI)ijGrEwKr9fg6kf<
4wTlL4qyk9heLhP*hvWm4}l9~#Z}Stpxq%m&Ufo9{}i`42tq<Zten|USS==j)RB?ci~Ib}hc?82O>(*T&*gh+VrS#zwsN@zl8^C*UPYFXSsHwql~we5S?yn>
-)3BkV|x6y2MI-wKRB?JCnCjCnkY|XnV=lD=lKbKFK#|36E1=P!lf6kqo751asY00gt<+A3u4z-q{qp0h_Wix;CI+o&{F@(R>h=Dv~{~7L(^>J+BDAXX9`r;
=lX@IV=@Mf=%Bi~R*b=^;oh{Armn~i$E1!7R|6tXVmbfQN9aNLI1qitzK)jgnr;CTAn+2B9#*EHlD6-hUBZ%f`b`)Ex8}M=mh%z%=&r0VSxXq^i&`*Rmsckx
mk&U6G-FU77f!Ea43jX=tbZ#TjDa3o6!vqK8doI=93z3;=-YjD3^D<d>8Ea2^T2dh5I_T;%p7%gz@M6pT3o*6j%pdfhp}Zl5*4lv#VH^JI8OBC;_MN`I=kR*
CKgVyQ>{1fyd;>spH?!Up5VxEd@2tjq1&T1viis_AML67gFU~agu$NYUZW|~ffWu6tkh%f-7fn$dXjt?TWH8QNFXMILl+HJ1p57$pwsRR;u?~DjvX`^%j&6u
H{C#D#mgsOo2&06d!~!k6NSMxIdYl+rMD6kmLO430i`Y!eEcC*IgE9-T)@FktA;Nvb7b61nI3ZtD?p!qC#^K04-bGwCyY7`ch2Vs$kb}YDp#!lEay(ipL0jj
A?cam{g@zaoZ>8(IxD=@a*2Anbcd6bketj9B^*D_dm7VJJ73X4EW|sUZRzF|B<%5x!8!vyXp!bJs^<_};k}5;$V8{?dpCcyA9mZ+6}2Frwyt#>W4_~#v7s<;
0u68PT%LJ(_!DH-N&N(-Q16_WX_4J+cjM6l4D86EEO~%*f`4sl0%UN`!)BRPoXY#>zw6HTZ2<lWA98jhy7K;Ry21Fh?mAd?tgWS0v<|LtK;j@JxGE-F_(JQK
KfzR?={Y3wEQ>SH*mnQ5Bb}rcG{?g;f+@P}!t26&R?!bPrsRg!@1hTAM{%{?ZyurWvaQ>f^a?)nGrNmD0ncv~Ni6v^e7Rn&YbdeDZg#fK4I++wAf!7$3E!oJ
mlpYfhNSCfHy4jrF@10B{90~IL5JasT<4hsC&}r=kDb{O)#*mRG=Z>no#kBN-EyeAmAj68w>QH_oXayF=}gIFb6gb|w+Q={ePaFcTyYy-!#i-9F`?ApQ}X1N
s$FpfiDlEZ>?J#EN#Qia;#-yA;%WD&Cj&bq5HlV&2`a<jZJqMG9@;HHcq%gmV93Rq%fE@zAUHZDYw}3DJb8E9ITl_uJRU@KU61F#x`-O;S5^#J=}H+PYEE_L
!VKh5Ck18GkOc;$lQfq8i<!`zbDWru*sCkGhK|?pfG080k!V6z8g1giahc+^YmlsVA)R;s=tBakkEY?gx#mO`4b(4oq3HAvuuXVj$+Jc+w!EsLW0xdu=b>mU
G=;inQ6A3GlSq6iE~+tVfOItQM!@a+Q`m3mxS3jUGN3KpwNguqK^-<ovN<1EnEZJ?@R-|5;2B4HZ`fY+*!>t-G8flSf=$n3h(8KIZo`#;-rm5v%3fcdOyq#T
zzmXyJKpf1iZWf7br6HImBc%lD&bYBOUCun;^uHxRq7kuh!18Xa+3~PdO&B2KEs#evGDorV0MQ=0)QmVz8K3L`_T6`Mq?ywABt*Epo_D$nx$=ujht{;3buWt
Z(WTe0HJu7Mixgc3IQd%dBs(*|8qK;58g-$MnYsM3qVERPv)F%Lp_r;OyVD5z30)ek7dr_Mj=`+{6f9TKp6VY^kBYt0-$vldc)N^pSMs1KvFp_22xlSpARXx
)nmi%*blZUVYWqZ;QzAw_>D>7P~L83N<VJ<;Fkf+A=@C%LiVPfLnu|{JnmMC3m=T#`hsI19my87nUaXgNS9xS!rmo!q7tPJ-$G<Oz!RfBCemfqSeaXo%AP)j
SBvCUkS7fxfZ@l2Qt6Av3($Jy9Ng4xz5WR)=D6aPX{TX!O=T7hj3(M+oTXLQ<>3@u^-{+)b5Q!2cig+%9rzj+s@#AoQD@}Du4OrYgr8@L3uY0X`>zuqS?QAg
q`GW9B`x@iWS|)eKL)$t0dL$}AIaOl!3bNfY2NYZqfN6`9J~D+<9m~=6Hy=VeNtGIAI%?UQ-0S;XOogzF|%vgs!I#p8q$b_O`*xnbc0AB<lXUD&E_Y(*Wd!*
Qew9bU~^`#O!VN#zopl3j*g`j^5!2(nf`!OY_9k#!E9~&ZqAq=r3mRsnom@@V;mJbzb94q`p~t9TubAQW_6&4Y)|*A$0?qv)B5gp9rx;m;(Uw_RZAO|3u!28
Cihr-H|rB4K{R)^h1r53etJLwB#D1KEF5w-x_XtSF%;j4MQ+Uk&!Tg`9?PIo(?7u{OiYs#Ten1e%r<rRX{?FhZ!F>})?8n<V7CNg*U1m^^*b}EAwil$ai?JM
>cTaBB}bW$P~}q0ZhroPlDJd7D2w)72(hst!No5-L%V%Sxb56MlFx%8x&a#^3BJtTMKY>ee_bY`F(eSJV5LTC`21+qCG-Xj!<9P-VE%0&8VOXa-hm)ub;_Er
9(O2?!hurugSgenK$&n>Sw5;-?QY-Yzj8c*6JHs|E6uWI^8}nJ36_G^+M<uLeDh+UCwj`@g)49jw<`auqoF9D^sgtnADog!ro1hG4FSr(z?5QSP5LG##XHm!
{#_HocZXXB2a>!;TqSIo@SECSEfaF~{L05CI(00hwWN;?Z(Jw_V!j!lEp9VE2OW3=A$PfhY7N`8YWgW#A$4-y+R;)c2-KdkKd`P|)O1+!)%9F?AE9l=WP)Yu
NhkT^>dbI!nChNul>>^$O!&8<3Q)yIFz1y~8SFc2)vNWYQ9;!9+pf#b1^q0SaEPLTN~q<|6hdy82{fs5bbT@+#TH5mMd#4fa{Zb3cQH>Ql`aKm*(x|Rr9}HG
JLgrh8g-5UI;m#f@A^F|tCmn|cjEjFMlvBogf}*$GkNyw#(5~Zc33dvBf$_wZOpx_)qx`lE8HEIwYg1iQ^-vZ!s+^NP4OS7)ggx(m0W=e`StNZf?W3<6k_96
tCg3d1J8nVpkXd;?9xw<ASM*r2jPu>?P`ga3iVN%Ka>ajo_;}Ef2v}96r&*!cDeJ0r4raQ-rbCNV|s;;4MHpzIj=9OvE_(leh6V3niS3*6PEp6ZKI7`yY~rj
IAn>lzOLr{47s>)09JcYY5ot0j}qg=`M&?>OAkp52=CczH*s3YzI7;^8+nIq;O;nt7uS5C{-E-?Ue_2ZU<Lqo8Jeajh`==Ud7X%)6gt6Pl->GL*h1kyiV^n)
i9TM@6|8WfgP?p>4KC_xH}B=kpv>4ATQ6r}ua>aFZ0+omQJbS|gz4m(x|ARpGgdCf!;U$A=A~~Aa?L<2lWI^02PZ+$qSd)<z4<A<;EUFTQO;&<DjI7V;}VsC
I_f{Y#*C^z<G&{R>#XS@MLlgGnhYCOo9^K@k~~u6<C_)jD4W9Pur~8s+27+&r{PmUq0bAXXE-rH?MuR`?aX5=@-&WhRmRkpS6qp-4d5VZ+|}8uBrCSovDmUn
@W=eDi@2TEcUwo0+=3+Wg69(!piHO62d~Qz`}dvU<d{M!heH*35WKx4r!Lo50KqHVs(r*uf)ARQBrf`6Jt%Y`4^D9srHff~z+b+`D9_S&@EGfn_`@l>L5Yfq
y~A*YM_^GChGmwGU>WcyR)2txoov_=b0yS5zzhvlIfZAn2@uiRk{8<v`a96OoB7~WLn)Vbl$CAbH`y;&y(g)53^68Zx91*KBQ7j{Mk#)04}OUe=QqR3ZV`e}
*HN}~cme^eZKFK(j(R#M-Y*pHG>;jniG0t!tMuHnuuC!D%F(2ta+x}(&g<E{V4=|d$dM10JDfqYf)6q6N(r9blfz}dH`kF;5}b4}!My?qmcFH0MA(2oDK;Ll
u#H*d3EKUn)7vH6rE%oq2b)w(C!Ec|;0Ud>?lGH;U1;Y1*|`e;`CRL}3Yu~$cN#s^dv^;m%1Xi){!fNJ?t{`UTV#xS0;5ovONrA6l_G49ES4mYg>eEQ1n_jD
Q|)KL_duC`QhoLOiT$1U4-+}67R7DqL5?MaKN|QEWjpwVa-P>8{nNK~O4q}iB3(ZCJVAB-C?puaDAYQpxgMqLRCaFRh1pjt?aad{6jQU6rymn($-T}L&k1m9
=MkzsY*K7o`9;UhGBfxVIU^27Nd^98M~MUgII(jNyktq)FQKJff@vc%O#a7Vpn+Kb>a#DtqKU~dl)#~kFz_el&|<<f>R}Yo>&7>@heXDF)O%D##0bJEaGw^W
!1vx)!ljz@ZvR;Iz%cgDq>Oy9&v>HdVq;9M<tAhamUn-X_Aq8+urt?)9^A}<%Ip&WKBLhG=`*lPm!%10rm~QYH><LYOr3`(&^fx*ft0KfZXK4eUjvnsk|ArH
8TT>Z0MLv4Q)a*9I^&QY9fpf%z6eZc--300$?@oRrg+>huM$)h*cfOu|C96Y5C&I*dw5Wy(C?v>iIS257o3UGyQBS}GFzIB!0G8O&FA5d)@^P59i=<jQ8s0*
{ivfJjn|k#G9>p!<EuJr7*#G8IA-pPh!sfUoz82N#n((6dWgXQ)bDI&MB5}R97q=cxRfMs%Zn?#=CW}R2ylPGZv31Ek_9BJ9A={PKdf$lZ<=cZly7a3j4QbT
Ow$b?G)`TwDL>0vN(P)NV1AYOliZ|KC7m<g>ZEs7*AFt&0VvmguyZ|118nwQZ)0_r<H#X4S0dL1oZv1yJ3-3*1WhvET#hd>G}P8PM~CyeejsO<^xLC%de7!I
GA66taR^zm#O-ZQ4N(HWmc$yA7QuzO^y}TsmD>K!umG6Vm*`vR5=5HPIZu|qIP-{I`5f#DU^KTYxSg<ccNdr@_D(M~mjJpPl{oYhwYClac-d)Y%Q-gF2|=MI
gmI+niE9)!ve|Xk02rAYMI<6qzeY=eV@!EMrer-X-R+%fp{pV}p&`w~>V*0|-2EjAo#7?dzUx=s?~O&bCn-~bh@X}Mv?npGti3qfcnD-(KVGkv=I{3GKY6ET
p+<Y_pOT4h&*F8(%gboVNb}mvE$IsRg2S#Pcdw0*i<m5J@@!w{RdIB_!c<qAl7r@l*Nbn@ry@MhT@B;=D6IkKbja)7xKo`coVWi42y!64KB3&I1CeXzjHf$0
9RWYuBfHQYb>WyaJB%&-<W87t-~h@oA_At(4Ay{ZXuf(_^AFiO+bZqDPQE2P;F7OM&rztG#0AIw{3JlnW-wItXrmEVL+9r>;OsOwAI~pK&AS%<Y#l84;T+(_
ZH_q99^3#;$#Q7&_0CAMOR4C5Pac(@YL!NGxx6#Ums=-cj%XxiejI|X6B`(8n{%_!9ZR_}u$;;$y*1rVLNi}~%_4F;)=hjZ%7NNMuhdTAPWbmvX-Yxr$A2Ae
10^5z4w~rkh-Y_5&5NQ{t2F)(fI7Rm!0SJU#IRM>z7V-v1lRn<m|8MB7Zk_^s>fDY8?9PdLhHwsh1};9R}QLO7Nv+ry<+29&Sw^<HLh<NiO^A-!O1Md0yWlJ
pv%r8fMq0yZYByJe)3Veb<NKwvjCwIM%#mIVS9FNWAjGE&^1@ikjJ#;FrO^H09WeQ{jJ&-%Od344xJ7acBG$h;D4c>CYO8qMoI@44<bQxuwvstdnD+xNdWRn
wBf@rD4M^lK%km#h#0e~A<iAKSP=aK+?;^sPze=6#uG>a1-WYlqVeuJL_vCuQ-_z0@}bK6f0_o3fBp0^y)$L%I$>-CU)wg;_I1uz2n_lmg-Z-lP{~Q2bn(L$
rQ-tim@qM>;A%i=+MtHE05-B^swjzMNkLw-1s~Yj0UJ&YR%kr8<P?a0#2zl@GTpD-?1@BXXU}zfKm`qou7d;UxlSXU3hG|B=|*mIQ-F_3IW~8{YN9+ZXastP
zjTkn+!8higgb*k{*j5^YbvlJ9>wYM#HXS!)SH2Na@jEbUDx48Qtit+P?h%QA=>m>32H@~(6-B|ZYP>K;Xm!?@V<xRHvB$PDnndc0L_fnqRL8%W^GrO8pidS
=-0(X@^nGXfr|=l_|aeWy}WBhiug#*n++a^ytTa0K8`}f{fl(>r_{e6>r46|_%No=XJN&$?<hsBz``IJctopiFZ6rf>ph3%irxnOzXJ7b{a8m8NQ>N(X~%_r
JJb+%((!vYjxhWw^Xt+YqVM`T1YoA5za<JIRjwfY<n?ql2S$hkG}3a(GEBKmx<^SvOH|ZAXd+HiyX_MqrogT{6Wgcx%(-j$hi_1jxy@}zTlkp-R|riiZ&yg*
V}?xT(NgTIf!Vh$f7t74uxOl1AnOhqeo>?PW@>3zE^Arn4i2ahyUVIoC->$(lD)R|IC}PsYuZ}LcBYas51bCI`eA@dY}I*D*g!ma<EdjF*F1HNgz`mO@-xV9
!VQ~cEuL*GGE+C>Bbt>02_IQh%<SH=t%w|n&{d$HOny@i)mQ}2YdD~q^$fv*(2rKG+9f*l4qt7853JSp@KNq;+gfA|a7N0NMXW`uuvCEId#OO0ps)-1%NBe<
TV0mN?`R@p!*B=-<x!f=sNW&e_7`W}+?dzMHYtkp9+jhGo3IWH0=wH5eJIrJK&Dz{tncXNPm-i*PJ0y3?=6I;@%fApo?>R#I1&^-lITq2-6_Bz*2<zxcNCw^
yAvp|rg{vFn71<WQxQ?X;WIlI`qhcC8A7ehtNGy{^ub@^?1k@$c7iUrk*GUvv=nQS*le@RwPawKAGf?{pAvj{S1iE(<dF{c?Boud&_<qRlW3m?WK}`>4IL8B
=WaJQL19u4AK|FDh>SyT_}M8b@GGRJ*j-UT-n~mD1;f#3k}a6X-nt%bm*S2Ckx}tLI>_SP_nxYHEGfazFSCb0rQZDf4!Tz=muk$uGyUp@4^_8787uR&Q5;iG
*E7^!&*$hBf;cc^r0Gz0ke+wfLs0$q`nbLC%M`vr5D97oemh<7M4N&4cF~HYr1fMrXOf@9YU7H~bO4Ceh$`a4w;7d!5H*$^ILAg7DL9a?>|$4yoW;qMiYtG~
Au>5HIm#TD7gg)S>hCrz&9L<W0;d?8$f~l~nn1`yHu=I+$Ss54+@I^F@_^w;Blfti02f@jv}ylJ?dp2P*vo&vRGK|!oDO_LYVE8tjOJc>GgZ|({#}Yn!_$7w
g9Yar?k^xbK{lVnLjUSy|1qwMY0}z|+}%+*ZQ$paj2sx`Wq$(8NcX^Cku)ZZc5IomFDyVi_P#wk>1D|8j#uC;1SlrJpK#F{sa?xA^7BS?g-<#___hpm`e3DR
g7Yyo#ZCaVNQwKab5R)&W40)DdXOms>3MN*jNM@jCeUn;j>05IK-+Dz^J2o~5o^S0pecyt;8K`^)l-&AXjUfa%P^AS&An!IZt6wj@6hwwoA5EEk5XEkF!?4e
#<s(*_GqmMkpPm=ZFU|DJrr^DRee}4d#1SG%e|8C*wveTV!uPmbuB(VZ*Mcoqrx2aEtjYpE7&sTjDna^1TAo8?$znE;$cg5##yjQ7NBNDuZSS54vsqBaiv8}
(@MWs7N$$H!xt{RS`rT|)Z&@>o(bffe?LBZ7@zk#cB?Hs>Sn@3Nv6s&eG&jh#b%?LTXNKx_y0XM=yIYtFe6+v9QzX>EJrgvaO6P$bu6e8dA|}XyOD~A-6lA{
)^^y!;anNgZt%N#UfZS_yAUf1CQT2lf_h+T!CZwOOz@Bs)qt1lYTIPqR9aY9G0q26k(*CPR0UEtHUCy-c|LqV=8!dUYL^{RdZjErI{twdGr;;s@hDH^C&c)5
-N_SU#m8o@RtXYZj#1@72WH+uT4C{R_0D-)74T}DsGXg|z$A?@ReO-VHUe1TLg1&&VqA0Y<YUpUcbuXdmK@fM94Cv`^b8$@G@Kt+?cb_*6lvNyLCi0;&+c1h
vk*czwvfHZ^tY?^x-uIIgJ#M}Q&nC8(7-8%JT7pDaQ{WPwm`jgUTsW9t(6+=8{#`B7r&f&zo+bKuJTtnkzcclZ?j-<*9M7Gra$Ag?H~oK!io#N7s_A$ev9K)
@n>*w1G?VIzw%on-fGJ+H3Eu1UqB@?^(@R{S;PL_4HZn{`?=typ@9fFw#6Z9tVXEeW-H~x>DCaDo5|2!zH5}30mAYW;xvJU7Ra*ntk$&0+8xW68sQOBJ3LSL
LLFCxBjD#=_v0PA2<J_a=k1-!>t1H{c-;!vmgZ)<&5CmK@+XiU4Qkewfl9S78KyzS0iL812Jw-;@Dm&OUJV5D6ZAQaN&?R48KXt&Ih_$+!|HT6_LCO3u7Pyn
8aMQB?xtfk^i|5=^CbZv%5Mrk%9t39mrCZ<YVBaqx9DBA)Z((^zyZIu@3F^B=Xg`ko85A;ar(<Y+caGwRT##VQ>HBU!!h^U2>!`BEn)xc5<hO^yp-(<E&B>M
0rOdzKz>x^WZvB*AQbo<C}&8S^K+GX{jdZtWxBj(kFbTVBmoNIGlqDZ;6EJmu++|^Sc}HYC-Lqg)2+ih{}5DIx=X|Y)P!I-zbHayXTLxKX*M1<#@Z&MM%!}D
`>zz88cnw#ypZcfD{BfIGY3lxFbA*L|22WMn1pVwhgS_`lmz3C|0#G%15`Hrx&7i?7z7)QqG@Cr67;_>Gml8X;LAgPMBnNzLL>Eiwq6Uonzib>X#hl%FGPWZ
cl{VBK5)<OR<^YijBgz9ZtwJ1r<BJUr#HO&E@RMLP<}KsBlhu&+78thFge4<k{9(;AoY97RfQNF(+&>7&aK2_!`gBk0Rj6`UP*7pSU_T66Wd$MxRedns#PbM
_axg_uU8Y?BY$yF_Q~sf;Y|@{v^XD8+9(m>;z9E~vIzA?0OQ0^%FrKqe8{p(xDEM3(>al*LpvZz<pu{)9Y+`W*65Y+bw9)*&6#dP0j~s9#UVaINYNsGhP2a7
!*wiBu)JXgq&Gc@7(G_b8qlj<t&LQlhyO3$ch&oXG{rwlQOs$st@6&yFw&KM8NH;K!(^}Hk+PTka8y4s7&Ge&p=5maM3kY`_+l9|53HZ4wrjhX*Y(Sq)LeY8
R!-H@R^?$85~^yIG?--R;^JHc6S89k<Snt<3@uesCLI#`t~g5v#CJSxDzyKQn4uJ+Z3l-@nnD^&o&S4IYf)~oSHVRMK`lT?Zid$7_xykEJEGsx2{Gj`vHo(r
VABxTvcFtn?gv=EF#H>Pa&hfvK)>36XLZ#lB1XMt0zlhVT61Un!>1Ra1t4$9v^7T$tsgwbTd1dMNH-ad{HvthB%9;6AI04E@De4Uro~t^a#g#bi*^iRKN~w;
*httwP)BL%i9~9??pc}nQN@9R@}uLQ-KD`COlBo&lKBU3mBLVMtf>&tJ7Q*F6`t@-4f6ywtDi+!BTr5QvYE!FDce9t#-x}W?(9{A13b&Hy{cK*lACI3(R||W
PUUD2K*-ndnX>s`^2`Pk^ROrGD<JfMgux&ikc#B_c^;#;<<bL^ZPgfm{KX3jn_KLpXF=RGD(pub^LXE4nxHf+0@96GZSARVqPmh+l_o*OM^YJjjtPGFfNyO7
>fb(3T|PTYH($4-LoxaS*K--utSOr9+T8+B4L4l}?o14~*K<8SVqgv-Bn)~AU;W?;nlj=4J!V|CG&K3muhLFmuX#JuO^53%*HoY^dDy>yS5=YJvV)N-o%8~d
cK#~l!W0^h_flfDw_V2^h?jZaglgzraBX5(9&z-9GL9VFO)q@)m~*p@`#{_VHdIX%27M$liVlq03nAN8AF%n6z;fv8s1dHv00$Xn{0<=PjV>;;;po@rsKGCR
rH0E%9&Y>_sbhK!iMyNjS~Is$oabRpvN$skY_id%u?Bu>5E6%VH{5mDs1Ut-gNO5Fe7+fX9YjKR$CGI=4q0;K;09=vTQBr`z>;xIq+r9lM)}f||G0=#;n3v}
p~_Ep#QufE#urN<wDpl=0_O%fX_Y<C2d|pM7P321@E+B-J#%26Q>74Mp%d1aQ(#{w)$ZcjA>vXveqJNr3_w6o$#=r>&(7RSFKg!vwohUgCxc8$%>J1>3)7>^
rByN|(39f&Gvkxc#xfz@FiiPd+432HG~?Yf(EhP)`TKkbOJv6!2yfw4$q2*tiY%NU@KQeIg^5o^Pcz6lTr9(kaahv-GZ*Zt1$h)bT=^Xq7ap1sv<3{LkDI~7
@!e<U^lLR(;T;IRH!P2sU>PJcv_a>i2Q<Wn6sc%ndG9jMn1n<Jl%=!pzBEkj%6<1>uX~b6za5u)*6p&91Jq)vT~=9Qk|NSumU3;jTWJiGPtwy-22V#kkSeVi
wj1w=2Yv*GMo<G+y95vX8kLoObBE~j`Layr3Ju$m=0Uz-#?So52?zZ?dAH1K@{?ipbBd&XQo!K)P?2|Pk?|-Gg}L|1B5KZnWkc)B2XwHx9$=)8Ye8^Z)@Q}!
oE1fLXM|+5x!!c_p>_s3_{368qGe>16@z*HQuZclw@}_~6=*|Dg{r~n{Wr=}5g9;4f{q*ob*e$v=bD+-;+ECWc`y#T$8?N_Sz=tlv%A2W?G^SHh?+=-SMv@0
<XS+<c9(T)5B$i7Cysyx;8Jnl+_xF4q>gy?*OKPFu-N4togMp;%4^zk@J;eTrW2}5D6aM@+KOeic&hu?;i&F>q}%ze$OHe8pW(mLdUVH19}T&Wkqh<Y<ZS4C
n!Z#;ChVcD5%m-T|3#&`9C(QtdjS#<8<v<|;r{6+CDtc|yyYuvvOS(E0_*&8WGHK5(m%3zID^U0AG8`sFE6(Lv>+m%DRd>jt6@sgii^Hg%xL`3pUqEYRu1>Q
6ztt?S?lBOQJax%b{~h=B^2`#$A0k1I7yqj8VqamjRbof`7+#uZdVUQmJb1(m;w6aWfuh2bcaS~t?}J15lWuwcNCW%7pF244*F8Z07}u0z~rzp2+MNWfKfzk
{TH)b1p2-Cs+(YSpRf`oG!Vb?Ew*mRhvdo4_pdtCOvn`mD|<4>AWS$j7-ph$H;>l-hb_Ls&=z%`ZDkF%;`ZKy;DU@Ux)z?(ss8c9I%VJ{oiO0%=F#4@lB_g?
1LAkQRClb;++gcRHDoUh-p6cWaTnTU6_Fzxp6?2VP>jg*Q4}<kQUW#7L56k^=~7@RxIf%`ms4X!8d3q;wKiHv_hmf>gMfCa8k($~w1aJF#_Tb$&<P8zm<NIU
KDlnrSGCc%LK!7ENRaCl!E9qYTGm`!47`LxOV#rai^1QK_SdliG}ii48xnMyKt2pdW?zK;amF9oGrLc5f3R&w>;t18gi4tiIoB!B@y%NU?6QP3wk@kRU8p_~
zUx9<I2V*01>P_t<n+~@1vwOHu4!&MPTz*JY!hc2s~FM@w~6CMorI;#RXNU##?y|*!FsydP0|9ER@}II(%@Kd_Cd=WfK%YQCfM8~3Y>InpX@3&KcrHISQ9RW
t{2T#S_5VE&6QRv0sisNm`0848^JaO!7BOyTQ>b4*oXUk<$0c@YM&5FtC-VL3mzqtiy>=`6N+5mqdyEttR|n}aCg6LYsvA+oRSLG@-0x8vpMe`MC~4<wo(9K
8gkU!C5hE3a6AWW*t)Wxy-c32)d@jG$`(b)f9?79LuA)v{nI;}P6}hWxo0z+3qB+$QA(CG%CE9$!gbDMQ^{^o5VvPw9=YQ+K}|O9c*!Fjn)i^=lO}+aG!3_1
=(veQ<8h>BKC+x-$+lCJ#@4n&{H1lMqg3q$30(LO3zDOr#ZgVDWa9`9ahCY)ap&NS6y(j$L8w*%*d6+`a&Tv_%^8B$OlMi2<U)Jyn>&rWl4#Zwq*rQzZ)foy
%58~|V`Y={>S04yX~3q}dZ-EcR+-Z5#<Gq{^gxu*UMp9^alCJhi{#Zu0k#<&x*PJyPpb#KGK&|*wa)P>$EHoJzm#!1tSrp=p*D-h4}l-XhVJQkMk`LoJC?As
BHscjl|`))AcCiuum>V(g_I%V6SU()xgyj+Psv^x*j6D&9zTrH!=PRhisEAZhM9ZaI_Gi4mu#nS3VcXC&Ws98CxDMh0}%Rd5sCUZqH2Nti+Eh2K<p_?nDHQL
FzKfNvR*-Ycm1puYK@Y7WG_O8<LAhDuU_Bz9_?&6-pflR-!IG$f-U7_a`B9u=n6EE@RFE|J`*#mf=0%)AK2=~Z&-h?J@Bg$5dfYP=jer4qqTv9(Pr!9I_w1V
I2v!E683@lzJg7J=6`1->D}4VI&6GUQpki?jlnD3^E^M8JOsT0Lwwm{uGccxXC(h_vs(OJ9<IrhDG%;vDOPbMl>-DTL(cMy&qgRM-kY$Wd~)tlQrq1<QMnPy
7EB1>pQB3Pc2j^-K&5JhK<x?0omCBc9pHOh>_{b?Zk}~zB!FGsWGV+HDAS^M8z!9VoP3^jH&@~S7c~2w)8}~*GlitEm|9ZNo0>^@$8(6jf@0NZrR<d8iKuyp
iAq{9hJNe;p*3ntwOsu`b?lZ)yAWCq>PUn;D2-U}aliJ&>VPAvvo#*xR!PygP@RB}!iN|_$n1S^Eu63(1;%|$NjdG8(KfGvWBgnUvQYO5K?pHcc^|C7CRo3k
_=L%IJw%J^(aG8mdeIHz4r>?_$-1|L>js6#o>2;c5l@@@DiXs?JHNf_jjC|gc8j|;Rfl1U)CbphGXvG41;?VL4>5Q(#&RiXb*wL&Y>z|%o=~p|aVAX))gFUY
w#leVQ@LUs*HZaG<<jKBk^PvxU{2CNZGdkj(<ogUZcYcHgwW){-D`1bkJ=ot=6g^k!+t_V>rgo-Av$_7MljGxmJMVq_~_D9*t$v4mnOAacU5$c!U#VeI^Pn~
OVlgd;@y6~U{Vtlv7&yUrL&D--sbSCO@BZ2O034Z<F{H2?$F|0_!A`67`=N1-nT;yRQw8t8gfK)vvb!^jC9v5EdttJuVw<ZIq7nKkVg3_JiO~FsJEVl$eK@t
UI^L<YMlT(v$?*d)%X+$c+_ih5sd^|dW!VKm#Ec69aNVYP(r5Xag+6XqNVBEBbhq%;@-sQLN~TOphcLxOF|j?9lllO#jF#LEL1EbX$8Zo7fQB043;37#F5bv
Uq|-(iio2R&XwyyHy&P+J~VmO;`%E7Qf7jfS%);|WF6LGddsvA$}NJaLgjmD^SB3+eHto2ux!0O4NQ1iaOOIDmXN6Uic8<h^8F*6cd}BA-!-tj7mywbJUHNh
X+EKIk&`p%h<Qv!bfQVLoP=jH>cv1_O9#XQS#t$07~}J$z-_}lzRr%yi)?};N+p0sn7PfE4?6gUg!Hwf3?>A|eU@e7t1%y@dM$U+Ne@zIRp2enh1V>Eo)o-$
ak^H6)HL_pb+)p!ZTmO|77ryKKvI_PKx^-WQYux0j!j_MW8sw}K>1+mo4lW)z+BE{Y|N26cvzV5Kxa}!V^Xr+3Y*!|!g+C1(#*WBZ}%ObQblI5433kf+*)v6
hZ&pqeL7dB(ymABT~{{Xq<^e}-uoQ&z|~>NmWVR(-$J3igCXB;cWp_l>tdGT#6(x*d_bzk=8u;L@*$W9#Frw3L+AVQFSOij#``MmRk-c`V=$P?aaT_}EcS@E
W%)7^Eh<Z}w&LOMgnQT=H%G)+ff+yFZgh&5bfFUSC9!9JUM_ge#t{8maOjz^r@nZB!cy2T!@6|Hq23vZ{xjCjJVaMGbPd2dw#osb`r3<AC{10$zw!DY(_`Dn
s+&j{>;G_sKJ=!2kH2G;<w0^L`3LcF7}Vgs#>Jfuye5&M-b@o{MPJHs<0mjUtskpI7?%5$CA8DOY)L3h#j&-0WIqN%(|R>R-_yZzw$e7VpQ$k{X405CEDcbv
%FbHGXmjsVp<rZu`=%S{0v6mgB%@LX=3nWOivfT7KslV!2`0E}6!mYn0`)anJ3qLEiw#=5G(Nod;oAE6$U#FkUJOO<O81Fo0^!)#cp4lX1<nDm?^hB@VcWXD
Yr$9xXPgtS$7}(CY?;T_zZk7nf_h=*=DBZUs?Q+kIc!s6lg+d~(AU-C|Cc%*tB*x41t>@Jsh97KO5$rq;!drh=;=EYfasgACT$o&nD*j@k5=5=GzyXLMTgK`
c|&I7-f|Z_tW_oitLRM@6OKLBa^u$JCGZcTtq^)aM9&GQUo=Nu5f>SXHF9|1)8YQMAFn(ngpKb-<iqcPEv?c%ypdR4#sLYeE2hiF@enH*D1*@XC2x<}AbGwt
F0?dJl+gT^2)i4jZ#7j52FXWgg{XS|dK059Cxaq#l=;28Gi%*+fIuejqH20Ocvy?Ip~g|pWn!*w*f!XFyU-WEKHk`}HtD0vlrlI31eyVjYoP$ZcW2Wnhuqjh
HfA<NOY5g$54H6*G2-_141V$k4AnmNN4<UqVwT(qy=OKhe<66MCN8U5FmFp(5>E0mDV)cUBBk*P)ajY$h~M>f${=<O_6K%hyb!V>Tb7gki%WE9rD^64{bW5R
PVG$+{8+TE&hD$JY1ZqYW^X!V7fKsHRy-oFKwcE<`7TvjX7egu6hwQ=AmM$$n4;SG?G+b}GtXe#uKj`+Gt2qc_CL6#Z5;kSsBTmS@V?r%#4Oo!+&g|RBZ``g
P^*;+&bR(y;0_hAUteP=<oHn=C-(~z=dcHcvD-c*vxqk{W=VvFVhNRp>=|+e7VE}nrcxHeN@;=3NXT_VZ>`>p-Qv$N(*LH$$@&p9?2w!HA98*T6?Ijc^u8-w
zIv9jxCNdSj(L)HmSQn+t`K3Q6KQsYZdb&wS8?Nv%ZqnB4c*u{UOf7eCz<NHk#2YBU?oFvmb{BihW}(+qP0Y%*1cS+jOF5PgE+ws31+vK__#W%xsOc!TgWtk
&?JMzz(+mf2hdNYDD<zkpM~;g1@MV^yDFGly?Z5`L{=x9qYGDyxk{*s@%CQ;U0IRK3&f88P6?R^%J&~O^>zzXbKuAJWi-C;o=c`D2Xv(y&`J4!zN@sAqIwT3
nD5bQACC?#t%H_|i7e1y^CHVbG_OA5S_f@Q>niDG^@O3HrCCPB*d%$CM^16#2`hZrm+~N66KUFs5eg5R%Qn&R5`jVm;<O5eT^y8yNvycarOw|PlUy|V`Hi1u
>0II14YpmziUc!nbWm`GtfH)-<s*=WDN^fk(c_C{Yx`b*E*KTGM^3e6nm{iS!QZI=RwUmWrCt9ysv8Y=-PC3JOG_PG7kz*fzVD)oID#mqhTiNg%K%HP$Qq!2
FY0RnSl(HYst%q!n2K|zlQ*$Nzd2|Q@mNQ<N3dviNM~;RP=lG<R)Fu}0vSignXh|R%#0btoE$?NgoCy80r;w0Py4{kUib@cpKGUGjBlG-csXjZE=OgOz=-E6
Vt9Y<3+7xj4d2`zSiKpy*D|V>2s~w%Nr+#%kWLMG>bOtw)hvd@Ixn-LhjFl37F+%cM|i=KYsE7yNuszh)JwMfOQt)-#4Pbi?J9~p3I};oWEnpOJ|9t|HCy5?
nl*qgFSWmOK1Eb<?$aHUs3<a|eNOO)yeJtGwx_-WkGpBfQo9mE?siNlc!kRL7eRfgwxw3C-#{t~J&Ze<s=V`7JY?T!FqXXu%My%HkA$Zv33zSzYw8o&KUL5>
$t4vv4K1cjj(bMuZh@768p<VYW|;wELqAB;p|FP?>+{(eBSmM34q%xolpWt&xOXLrrbgbFwKi1me5oj+NlCsT=d01nJ6M`%2?9ja)tyDl^F;U!IvK9Cg!!X`
Zj#vOH+Y`<n4Z(ISclfvoR7ssx<(n_ZNAyp!r=mxxrA%c%g2xf_GofXbToJtIsO0bf<k?4Ia>L_KayCu)Vv-G{9?b@<LlewFwapbn;?cH9yfev5FGJhTnB^_
cyqC!d1^k|wMfc_rONx?$vh22cT~r{hwz^$JFYdtJ_*H*O@*2#gL1!|#NC7@l|riYi-NW7Se4HgksX(5q+`mcYkA~achI%n{ahZQB!#WbITZ~~)I_@Sukd2(
_rvz=D~|wSe`gpJCs{Q`Ov+!te(}?MBP&svU{dgxk68B|nBTChP;$kN04F?$QQ!GiW;SrKxmIYX7~ro~AeD}So1n26eZ_b+dPd|P(PtWVlR=$dYqf(pwCjZN
Ew%6*eNJH#gZeM<jjGg}^8m(|d@KO*N!wuDt)WO3xFSD*nh*k~1U3*R+vi{W-SmPsXg)%@otv{`Yba7BP?zGkyN*Rq(4;Y2{U~7{eEx$+!<B4eVP+VoM*R1C
`*f!2N^$2X+WaKp{IXxi`~%)yYJstN!?(4w<Y*`U@GJfk1ut@yO0ta=@GQ^yOMnQ@W;)8Ho9lbTJFE=7d%Mgn2`zLyi4wb>_fAw`XC%1DqwZk<BHst+^LR|r
6hic~WPzC1A}^ACmL!EvPxJQzA^%kwuMir8>l_ErUoZi`rmuF&(=B@D9uWof0Pa2bkda>zrYT{n3$AtVnzFxn408WxEUPB^DCM0(D(ew^k&~K#Cvu$eWisP9
`lXC6i8qa#b7C}RU|aOwSdw1tq<zq*1)_lZ`dNBO%qrbt{cV830P;vCxofZ0I;|*o-Pf?0E?qp@9K~#f!kMP2?1enhilQNEj^OP>DBk^Tj&k7zWs2$_61CY8
5Px%a$cN6@ipJU&Ho0)qA44Ag%<>s#*)_3~@ww6=`T@=hKkb{iA6hc&gpRYrjy*cu_pxT4u9xyHm9HSHSFjv@`^dC={0c9bnK#;8Nj~f<Gvb3mA3Sb}Y<nn`
IWRHKq%0&E%I~ybB}Fe*-7!bP<1Ll0FdroH)`J6QAlRMjF*{t;(jf3Mtaw?|&VkF-fhoS<060~r_>i+Z?J8SRW$D{~A+4dwiD|l)$Qd9wrUqv-79iMa?X?Bf
sSL`!Ox7{;J$QN<0X6Yfr9j8Qjfwq$6$X+UXLPnQjT;^1g@Jw5agpToiuK6uNa(?^31l@9HmnS7sg@Dw3-*)3cIS$}-R@EuBUy!yeHt3xj}@qx^h?`I4>{N2
ylZ1z8{sm$0kaIh0lnm|r-gDcemIsU$D+%+ifB4|cmdx0<<fURrzXi<$+NMyNBh%m0v#!q0qUx$Vm52qnRwKkCt$<S({eb%|F*-q*Ge-^Nk{A?>VjxtfbK=A
mJH5fBBYmU{F_1GAFHDOyJSX*an?>h8pblvQJvgQG{>t%t-|X^Eb3QCB1OQr(NF1^H{1{^Tg1SY_8ePq>V3u-ihoIl0kFP_tn9Y!-o~k-0!2h(!@Nn$80Ige
*hel$O$VxEs(+IVMbm@!W`KZr*z^lT<2`t#LW#8Ca34C1-X~$#mR=DqVG@b0S@i0<Iyr<IMyrrphmRY0-ctVxac)SQy@;gy(}<Aw$hk4t&>>_vfBtEGw^lwm
N6ZXE?GPAQ=cBFHZ-a<`sqb=WlU`oIFCbS~evb_5W(^R22Y;vKy&Y=XPBf=zx<CNVEG^8vpwQ6}a1DO;$Q>$SCmavJ3Bl7@svG}`;`tDPG5D|apm7YLZdt{9
gK<G_jn7UkHiU{M%mKkD$nC1%Xh}-Eks)xt3S%PPaWLPi`P8Lj_yBEq*w@(mlM8t6+gGfHjc-&YyR;q;(+V#`GXf^cU&GLBgk0K5>I7`71<#U70af%U!S_qO
)${ZKiHrD(W1MecX{`>0qO9NO9~ozD9RhuWv04krW0x-!D%;Jq1QESl(kztup{U>?@Q=|2p(sDMhnTWe^Y+$sDU?|LGcO~6U>#f$vW?1Qif$m_H#xi5Y0``7
*HKkx2gz)=Tmp>ny^r^MGUxpQbBOndV6tT!=@LqrlOpw>8jBf7eeFQgJPmG%iL^dIY~5QYYKH_;;yGJr>qOb6cI|@Hd?+#rHY0{j2oRn1Zxt4NV1!!!HLY*=
7ZwU)RYQGfgw2~H%jE#|j6b_Z1Zht0-aGLq8;_x2At%wkt8V1>lALQhf|JMPL-+W5#~&^$?$e^)5bx*u$RDpFhN`#LEQz5paB^f;fprubL3P>;qqM$p?ZYQ(
_VR?;dmqkuaa==xGVOAxE-$xp@HwH|#cp7~4JB3Vs3I&-AWqLTeY)9j>CG;7=VaH)X^RO%G*=&Zu>ImKG|Qm*u?w$UQlmKZC*8HYzjGC4fnh#;ZI2g;LLDi5
I^bfRY+-^6{*X?>lDeH83tJP+8eW9Zq!QQr<oMs)iPkwpGgfg9$jx-h1<n`pEbsPYWRSph3OR2#MnSG)!r+x_dp*OH)lJg@p?iS9*6JWp(IZ=XX}(O!9ymsA
EbHj^PQKpet)>y*c=wv5mwnP|1xseN41glpzo(ogO2%7G%8&2$NqiG&6G<3_i;)?LMlZnuaD*;wJOkmzI>-6;Sn<>&?yv?<QBn#UPfthmY5M$LIHoJbei|2W
shu#y<zGf>LjNO*p4BER<Y!1qho;9wke1b?<s~JJ>LOXAmN(`7f&7dXfnppwA51xRE|~ehpJ^^sP@<r~x@?NbAg6GPoF|>TLT4+??F<)8g=b8)<*l=oxF14&
KMcb%3J#l%p;)r6G#SZAa)Xe`M&xt8L7K?mE|)&Tu|x*O%jtg-Pu{=k7Nea%mNw}~d!7mx1%v%@r@w?cD{v&h6rv2)w5wgWJGazLdtb51D9hz_i&@}sXe&{V
40#?eOWI<Um>U)_ioz)l$bC~E+JySXk?T>*&|5S<&KZB6nNr8LCCK2gp3e5ZD$CX>S_p$yUDnzOgC*Ga&;cvA%T_fI<S`8gDPHWwaJ~oQKSiUPJncj%WtCQw
R))%^chm~c(8O;Hdj^xr*`*~gMH(%i>&-%12g#*p6cTw3h<7W2D*wEy=&7gebGf#yCA^?yW-*)<@yokJ_}~{+5d03%&UHB4dc;oT6$FLu0jYK7w@OB@<*foY
c1Cn{ByOIhD&XW&R0cXP6Zef+CZi}>ohp7WW6X$%mW>}BqKB)^G^Wo;+_xAZVZRTt>{u7>Uko^hp<P+X*#c+|!m$CbWzrtV;2{EVnDWuFtZQuonb_{uR(SB`
W%r4CvX_;Yf##!pWqWGAaJG~+J;WC~o4Ab7RJ7E$Cymn4*b=+h29<;)LoN40$}`$JpB8Q;tKFI$dr@B<aXi+BAuFu_^R~6R_z>-5*jZUfr<YLlmTiT*)dMFI
^zqKCA-q0Eeuer^%EVI$_OpUo!@@TDwgTQjnFAaLe<)-M#DE>^ur7c^gFuF2rX^)cNJmcoo>`7PUQ>ic&0S4Iz0A4W!R|`*<H<By+6IYGqQLlWk{#bEk@fqb
hG3dbn^#!pkiGa=RqnK!@viSQr%)hr5w9=h=vTxTa5-iX#6@0gw8qq<3|tm^qB5peJL)#)^C{l0Cz2B)Vmk3*#q7rd=-?tmB+Sy?xAd{w$&sp8AN$3{qAOn*
&QGC?F8oR}>6u}?urQU$Ypz|ASF>ABsDP_J`D_xAlKv^!{TgmQJ0<0GiC58>ww|1|<2z0gtT%@F)#N&Lk+<kwZ9i)1sSTA?Z5!Zu8u}U7`r>g5sa!KhMzOAM
>A7+7cAnD#l-W?9(lac=us~_l`EB0c$n)k^vRG<-hD-Y|%2<?s9FVfV-Aykb8INwp@2deO5|gmQ>k3Zs_lzhMJq`WNNbr>AuY-P4dHd8?l|Nb(Ng)tP*InA{
`$4z2w5h^~1eoDI!ZLo)9kl>!@ufYO9YIPEO@BbHjq=sbAFp*TxuA;VygV?H|KaTV^!LIus4cnVI3HZ5XHlX&z(cQ-+E>VAyxzEy85cms@i-_9cLMkzLB=RU
{>v9LMwGE!OOx-oa?L(sC)9i>@3<_T#pF+x{Q8H}vD`oGaCyub=UQ2D#WB91#ZeR9Qjl&K(yjO!k|PpTDuz2OXdKwA>DwE<j#uTs)*P<x1lj!rO~!2OFi$yJ
iy0t5W!TV6$9zD>%(IO%eP!S|GE4?X>x#g^h3N@)^ziT-CR3GHAKF1>x&zJj?JKndujf->@tv70ZsFKkpnC)sWv)z7UE5M@MOt0;u|xnNnYtt#y<c9Jny$dt
rS?rvsX8L}v34es9jr+6G9>4hby50Il$U8g2Tl7&LE-{$h`kKA{D?EAk*jZ`5=SLZnaW)urDPSvvbo2AB|d|t3X+LIJTMan6A?}D=0-Y3j(WhQFamJnyklZx
)7`fge?vfFAx{Y0`;%|9)VT=dqlMY}=W9TYCJ%+n<tcF>E`+V*fhdEABKVTNgN&NC`S=EV>$ye@hWXKyJG4s3$%c7@(ss~Y!$+*y-OxrNC(86G=zM@wB#e&M
shC?a<M>698{CeuF`!QXFI=z0?Nj>`b7Nf~R)O3IW2bss6%r6U5icMK64#$pm@3hoXf(b!<ws|ns%M=YOw~mNU_rSxr;=hc=oexXkBTH3#|wVkvdDUvnz}!b
tM@>Nn02Q=PZ8yQVA{&*A?WHKm&snwbBI`}7X$sL!i{i(#xAkoG7lBHmO$5sBRK@qTE*s*nAtFC12NMZho6AqRPxs+0&?!qsy3z)ll%nmF{SC3j)0w9oyr2Z
mfRO?Peo$JPU9c8A`?@U-H5*F|Ie$4Y!=X#=2?`t5pT|>`jVE2oo!#fckHi0E|m-hDTBR^_<8~Z?3znd{jB4F5W+qgk0f0(TF>Kb6J7-U$!z6dO^T(kjn;hz
_yV!U|7E5akM%2bnR08j?e_Vs^tnK<lYP_kjA<C%&WHP8_89vRWwywy*b+6%+OONk(H@$AzA`t6rqj3Y3=0ylAL5?!?iR!vO{BcN0p;G=#-6F;d|P2*q`2tu
jN#XhTMvtDIM}CTQO|?XSVVaQ*^93zZpt+NQ{Qi=04GHLQ$<dAAnn`j`B%#*eV7rO;$cXSJz?iCvWbHVn@-I9r1y8WEi4s?*V|XkO1UT&<MxUVmoGFv3L`(!
8HJ0arNiU9oV12@J8trEY;mwa<RLuMTB;JFRp^OJTGDtW_(3`nKa0zE<2)$_+dB7H&;}l^rd%1GWi9k=@xqB%l)f7;S5}rX%6qGQjzDIF*7sL;*ut^>IW*=S
3@%mjOgGCov%?l6E%UgsQ^C)z)lQaD<)nqE>X3G$U%}aRaWB#(Svhq;7M@ck!5woG7)REBiNU-*ATo3k5RUW@hm3})#y@$asDrl=eZ@M(VqI=h?ZF^gl59lC
<zS|KWZILow#3c6a=(5Hf4@?SUi%0}Uh!m-!oF`7@eGqq0qx1}^Wk$&F48r?E-^_B3Hlt8LBZ4cBdV|AlV|I71toQsE0py&6uP|V{m;a|)}1lD?EHQjmz<`}
Vr}SWAq5mJ^GNBrD-l$3oeS_Jq#3G-W-~34v9O`zA~+VY6{bCF+UC2^IskDSMPg~ML5@v#v}*7EOr7;zKAT;1$%PWo!`Yzv9(qv!e&Q-9omL)ARcQ{U>@A33
pNizgQZku$SgR7;>|4YabgeR;oERtKaMBZrN&b0mMt=_ZY)k4{E%Fjq7CFkT&?>hesuv^l>l=EIqtY8uWAaMs(6MW_f|Fo!cQ<KIROpthiZ=nq^CJ5*7#AwH
=l_)M=E8#G=cjXDf&ACY3xGwPZ5fA2|3WvszI-=#w)r{QS7NOvWQFeoAcd5*1<aT6X`juAVwGe!_Z8_n+NL@5x*|O~^O`_<6vFDlNp>LWM$tSYgjyJQM0Mk6
EsWp?X27k4D?8i+)-_qNGvz}yQs8iy?-E3`{1ZgxndFt8qW;+bWtePfL=i?9t?>rJz$ugmr7WaSz|=4~UwoIMj6b+M)@M4EC`CLtZmWFsIWbsSz*>|a1ly}_
wjib8eW!eU)ACRA#6*QG`!sO#qSL3{!V3FxS~HXC>U}7jhnHTIIWjfBi#;Q4W<6x;XU^wTXuH-gs|E$UnJQbN%RBW|D9E8ZnOtBnkJ_xarmc3l$YUybMCPa{
3?v0Pw$8sImeMYCNt~vtm~SWQFnufry%X=N3iP&)EvJgQDw_nG!1F&$(4jdVzX*Y*A8BN(dea0>K_CJG(-ZZA(v;WV{1-1iKErwtJja<$eK$;pDlQ856g-9W
BfLa6T_PS^H@JNNnS7=O*%g0G&9L!9W|f>SAnQ8nhrPlx8VO{PRHf=Ny;0vdw`RFG7rWsJ?du?&y)GO@kpGiQcmXw|e5-f%OMu~Q&iE+T=!dqbLrPK1;Ojpx
S~&^XLSXK_OsKGq-8u<)29;MUYdBcynue+(4P}Fa|6;MP`VVXjmRYjpD)u$4E61iED>!{{4v>#5xNrtg*+9jQ&Wgvv+`Ep^xOhJ<1QfQ&riH&t*Y31Skp?pg
=}cnCq=qXYD+@KZnP;mvz?&J~t%i#H?kvaHY4*J+w}^)i^memL31JhXeiN#;c~Vc+8b^OEadw$v5-!`$|A)e1XAJfh9r@E`7$GEC_ZT^v`Po05z8HF9pQVse
8ALoHel6u(&jaTBGvMPn=+&LyD-l`tRN!^r2QuODnuSKl<gB?pMNY<g)nC|K3k5<<m&n_RkhC~H6~K8tTvZuoG=HW{ISR!Jhc@4UXx}UThL13O*OD<nHT^u6
xqj*;!GLIwkVRzMG+Wc0ctGSzc}lUFossEYy+Fm}Zy6V{SvG(b7pLrHni89-qI6$XSzs+1BH*q9m6ygq+$=_0a6&F}6yf+6#b`}5RPP*^cD%BRJZIWPMk~p?
M7#+*u6H|^nj9~`_sH-gPUx-4x+l3V_tm@Q4JBU$ge`k~P|w)r-Fv(YylJ>t;36mgh;AB%!FV2Xyuj(l+FJH}XIB~20<LMRSEFcO^&(cGXEj3RXW#%ob+&Al
W{Vz3klF%vIq~k+$**F+>8PQQnh9N*@fgpXuqrb7SUST5abiz+lv@2n{G#uNGnx{EHGT6kD%eFlryoT)CnQyIr>k28#(q!aFC`m+eHy;kbC@Y(`uZ8TTW%Kx
ON|P3v>w#tYW^v_Fc<_6kunfpxb=$5lR(uKEUbh!M+u6fm=b>bbXZH2pp4(t;VO>TPfnc=Mr3Tvi>tZHD(}^y3$RHhs3rR>RHv<~0uoL2qnFp$+}?exJqpsY
2go7&d*;^6(`uBS#Ue<~UzpJM>K}+I$WgWG96TfIbWG&Ym#!|3nrtWlGZV0%Jk%ASN4wS>!q+*V7utz{MbzgflfwoZ`*y83i0wM)?%dMEfaVmwOhnXE{KouM
tCI1aJ=R0XiUFYTX2_4IGGR?aO#nUcMZ<Tx_sOrqEm%x+4Sma5{$fYzBxV`mp;OL4{v&%wN$vgA4kseuw=l>3K|JyBZ0q*%-1e-wxE5<TF|^zSHx=)ag(5H&
DR)dYWktwtc(A+qv?2F*E53^7;3x?%ePF+cSGBciIjtjdspj0PmSTsR1|f;|35frKSlK97;TI^Pt=~(nNSV54i~zC(pDW}sJmnuSB;NqlVSvfCLnnpW$jQjS
C090odGe=<6jBx`BaB~Fmxw>I>h^eb(F^zSaK<KJCr%W()?=8T@{}j7ph)G1M{n1I(NFzCO6j*!S6dQ)0-5P5N2=zqdwKwg*_$Du>-BA%nwO%XbE7TcdkF``
c&(A^ET2PrBg!Hrvz67Rb|>H<EBBtlYM4~)9`vsS+Ng4uQI8%Tu`Aa2P|Mm9gYhquFcZv`Z-vjCY=fU97*r&~QCsI`e-8>|k$M+BZcs^?AM@bFK|qZ598te~
>yA`#71Xj0qARv_)@&^z0#&Ml!tmiebHl4Z`EBM#?~$o@xQ6JG0BtqjbrCDn0@+5KJlutmCP6FTgv+&A8V1@sW3p2r#-kx9x)>pei7kW*R+PfF0xA!YP^*&>
T#f!eib(!u)R_P%d%4jg-Uc3mqypNMi40BHp^8N{dDNq}jgCfu<5nY|wJn=_CMd&jNS74J*gK7FhQ|cc;DG~IH~@XvTSkPVE-{)*H0VchtZsALCs>4B`mC*2
FIV<+bZ#o)^E@QL)agu+dMbiW{CHS%9tS68jBxo$)W6c7+rOH{4o4>;`DOIht?N?NszgN%B8bP<@>Ox9Ht4is8V?{=qGvZOUaul<V+AjD{8xT;vZ6v~o8zns
ZkBT2>n82V=NE)cg+?K(kcvPq8;5Ql8S_{mhzFD$cCFe3L3oqpEXYfQL|zW6BqbT^r=}1Q9z#L%pH6?VHQOTvcY%*Acj)dv=C!s*Agm&Cm3p77INzS5p9)-T
6>B2GA4GnuN7f;8CiW_7;UOc}*GTBLSo(i&%I0V=2pkRFEn>-PV$+F<*xh0k{i-I09M<sRIi?K_f6(Bh&lemBcSs4_J+B;7L-1%?T@HiVyKTCF2VoEq(9DST
Zy`Tz>o#^b0##}V_G8zIx6@osNa0N&FYsbSynupMe!*g4ryDWmL-C|+RjMmZu6*jUwc$`n2|1P#@yJ^7QZaxHp+v>ix!SiXC3-HJGJd*LYOWDb&2_Bgx|Y!d
NCS)-S4Dy2dm-s4dqV1ioYW%~xVuisgrOm6)9Erq5{4V`<qRj~;)E;~b<D9#j;;Pz>T;B0Ypq4UD_P*E*IFK#*qGo2!EJ<W7MI9L7rikyDwX};TMY$=i@)k;
+J|0%D5;*57I8SMa1jZD5WeO!KnLKoW$9;%L#0}jUII4Q+2UBJakP#t0}n%xSEdueQp5?)RTp#}V?VhNVGBr@^dv7QsKW*|Yxw^l+Bl~%f`JNFMA#n=9FuUn
m{w|IepgRG%Oi<ETOlSR9uMrJXR2hrZ%@kV!I%<R3NAiV4IFH@fVXYV1BR*`jY9eUp8jajmBI_eMt6ciU5@;<dkWSv`W#apkTy}mA;9p@Edpm0;_qA46pH@a
M03*8v##boV)vF2yv;<J;Qr1_A5usV_xm$-fqezih!C3_S-8fKnNZF>K%{cEv-LslP}ypbB+k&zw3spL-6=Ovy&HoqOYBJ;Zrv1yZbg}R=ySy!&PRXI8gC)M
F3|Xycpm{Y3&Bt;L5TqDwSIiP@UWaixmhwB9lbRkB$H`CIk%~8egran1KjidklhBw2YwMzzk418xAU*HJNIxk$RyILLhOf+p<XCiX?~nlODC)@(Cp`zjDW$K
Y7t{<`w_&b1tj_>we@1ZBU(&G_x7;xs^}?&NPeAd6=Ea6Ey~%0ADjCfmHNm%Fy|G7OI;YlLwEWc5D@Zd?j6vOWW!H13anKO&fAbH(m~qy&k1g~4Bbb*YSVr8
dY@f9lh4e5WSS8&8B1k*xYd~`y0zHO|8%aO6i)~?&b=2N=v!s?D%!DXW{+-mgji4^MDS+A_9V)!Xc8Yr;4N>ShXP-ZSf<4YK8{;V9YTJq=F!e6vV~GZd*@gY
$HAz#ytiX5eu4Ca#kR}78d?ng2jHAThGFU1d125kc6mH?ammm(Vp?(37)6UnlIPP>j$(}?s@IlFbj!LG<owT?)00d`JbGPk9pUj5Mi{Tt3AL6vd2d{LLjreE
GLyh?v?#G2D0|=EG>L-!D$3ZI%=PX1k3#+icsb?Fp_|MS?o45#W7aB06}ijw^pnh5|K6m^?fc59(p%Rgsie&RnXA*pCrkLbx~<zg4hU-J7EmT0Ole;6Taj3{
x3&ugPM^nIpKjg!AC+=KID<?~#9dXT@*^@%)F!c$&k)wV^}w1a6|}3*@KgFImG$lfDl8GBeFsTXqMc3#&Tr!q%-r;*_nXz&yv8+G4I+qgM=#mGL4id=aP*<i
RgJvTH@>$A7&b(h<q|=zW~fmIg#H%7uhqYpE&C7}l%XTn)8_lp5!F`$K5mCP)OYYl`QpX7aAv&1I<R<|_K$#Nk(?Uy!1`A>oK-Q@Z61!)EkhCFdjKnS5z{*D
#?!5}+q9Iz!UWGaSP`jt#={4X>DU7ld|!@y7?MOSiYrln8B(269%9<<la505oM<c7;z*2hh#BSaNcHoODgwl~6V**W2ce+>7zgGMj7SJTUa{;G&~62c?elsb
F2o0J<j-wJU>~dgj?tT=9Obe+PyO;BizJ9JjW`~nzbDJ$@M&kadO)uptCtw9p=;&%Yzp6M4ZW+^xHUH#JZLJat|pr{dsM-QLS~8HF$l1FFI;;hi5A53Ke$Cn
3E@v558F$b##WzN+X&oGHMoh>$<K<L!?T<pcD$d?t_PPqwRVr#8eTB}mt}RtZ6TKVCNhpayM&Gq#xzK2fKs0E?i4vGNpMLFaioyEK8pagBcsecyE4Xl3RRj=
+#%v`iBMo7gB;-^DM%!T?};QJ$_K!GGGlNs&XnX*!eKgM>tVHBOYCT%Pj_*KndQD0@K#vr@~Ec<VjEY35e@Z-$TThBR$UptdM8n3dVB~-ZB*NQHueEP;_nP!
^VO?Bt-Y0D!ZCdAY)kh5C>|&Wrc?s*zeH#;GD1)l;=br%hQ7f9($s(Ssjna?{O#}sL7Tan;M{u1R~kJMnc)P_-UhQ=H@?Psl%bVVl)<aH+oc6qG5<O(alkiu
cz;fpbg~xOvZNGehwZ!dKRsy4JXv>zt3&`)&Dt8o1!~d5dd^PCj8nD*&`1^**^Lsz)J)sBKv_ZZr_@Z{XyBv=IjNYmbGQ3v`noV>Dg{ak`hYZOKMDT9TTb^j
uo{}j`UqNFHUmenfuuRtK#{JVbFIUsZLo#v*%3jD3BwkTHlHLH4MmWqd-Tr?t1TA}_Ce)ErcwTOe!`=lHB&Y>-+mAJUs(_xqQEx2mp)$>Ph+i>v0D?%yFge0
Rg7S}!vRM_b52IkM0a~%gD^^V=Ifo_2Q5=Ix{t(*+``X=b!!svb6C<JsySg01_wYucG95tlp+W4eer#!s`~!pj1wD>`fJC}Kd{QV=_p+Hc$q_=ynj(Sf8+v|
bg*A+;`7f>0J9Jfn0#{XWd)>9&$zdsc%$kWLIbuAlcs(`t*qnS++(cwtm=mxs$gvA#`HlqbsX(<H-0WJU=}e&82SS@%4(S^HG4VfwbNX7W`}!shb7sWAw%eX
SS2*~?2S1pD0p!ts@5l)HY1e!@_xBW_g2`?Y)WJq5k1Qkwxjrkudl~jT#<-+C(db7VN8~F;WZ}j7+w=w=T<nc?TCO{DNKfzvh}FxrxAst-wG_XQsz1P9#yM>
LJyJkDsaylLtQL`+<z+rtztK%3{DpX(+H|6j0v)gTk2XHau6f$9FDZ;xier|#19Q0<oN~0d76OJfty6(RyRvs>b4Ta;8Zj{6ZL5dG#M&5<OqDNTJn)GBS1nX
;+jydAvqyxhPj;}d^lkutzaH11Tf{-Ea#-syWOt{62nGIsIbUw2s0{O*FTd$y5mj)&@YvvQLd47ihX~C3Dug1k`006ORq>gsfcc-Esi26RS>Qy*zMi389bJ4
7?#H;{h`@9FW^h1!kgxsJdwCHfDSmtXhC;4SPz#m6|E70w1>L^c@0y?O~CLbxT9s{iL_#A%XLhGCX!0VDiQ3x5)1E>(uYX7Sz6%etMq>$mX&;!(t^%6!HnPJ
wpR(@gR<_?1j_Uv!9g>=T%ZU?Q`?MH<YwD|G8kS*OI0qobp1#az+a@~A6tB$1RvnG6{Bg}OcC9n+(tG#{@+$b$hnx3!V-<j`3ZTgB}0gw49m8_d6DpX+HWUl
OjZ(amAb&tAsA8700LzgmK@wL+&0ck2l`}QPTTJzyh;zXeW3pTvU2siU2r)NBfYZ%DA%$zsIU6i^p3~)^8WNF+6$*!*aVm#Xp?PM1c#COlFjp}2Npc;PBwPC
R63)!G=2<naATZKc{`7MF2+K@KBtd`q3QnX=FsQ(+LZ|TquY>DgP5U<q$tLv9J%nyI4`L^L~tjiEbTk#c6m$bZTOZ6)HnAH3RLm9_8mo7=Dn(_?mJ*EBW_gU
wz=u0o2CZfe*~ASPw89d@b2)lIi^;~5F}UbVU$4B#z9wL<J!znHC<XgDg6u~-Mo`t3)HQwpkU`jXub<d1sg*<$_k@+)WjZ|5X<jy=pqKDa0G7dv(4XNPVHUZ
{N7fScTO11`+Fu5CuKha8Y@j=s4j>SCpe5TT~b$@X8wT+zrXay85~?Yr(F3yordNg$nJ(GPbl_pJZ69{L|)S<tF6rDN1)UBz9C@y{Lbqg*!soW7Cv49?4Ejz
=m`%|n14i#hRJgCYEnCO>!dDD3>j*}FRT8e9t38K#Z2~7sWsfbA^A&41i7`)b+vW%E0o%Oe6K~R3np9aS#=7Ny-@;9RXtJ!vukAj?y(ls#uD#+gTXH#KEFA<
;fo_=@*0DmQcUjjn~ytx4-sB%>K*1i3gZofaBYVu;>~x>EXwp0YwWN@sEaSZ<L_1EEEsJ$(3#xewbg56LR)UT9qb*PovEu?Fjp#K7j$Tgt_N9kaS_xuMYlz7
@cE}Z%zKCej>-PTMDKiG;AkI1(m-T(`^oPu0s3WsqitF2RDEb*nT-Gdr_{?i)tvTXvU3~o-vP440{HeZV!Z+E>f4l3_L@cXYub_?lI<lGn!{>%erm_Ou3M}T
HUztjRb}Q7<5z=Hm=`YJ@|hxY`+`lSsvjtpx;k?p3wX3qlt!y7oR4+eQFDY&iiofNWj!NKO!q62u4_I~_Y9&HmP&F$BlPLS?W8Bn4Ph2*DO~5XR^0OqRf3sK
bED%}dQIK;DJ|+hCmUFfXSbr^Fc5600%JXjQ>U*1B$UBbKo6mIl{Q~<G3S?-nB6AoQ}-fL?x8na#J$gJ=f#KH8Y(7me@KTFNo|-rK6Pw%?Ie8-(Gu;2Gx1}*
+feP-U{uNy`sD9v5ubPJP(T@xX4YcjgtPD8cuLek@^O{a{&K<Tf@nhA84z-m&QbMtar8v#sU&-=EiKlEUP&538$xiO%`;W+c^e4EY}>(m$CkhRL`|Xnasy^(
l3$W$!v&vQ|2BzZ{|ca;XC08gzO%79`WdLtDcpq(9&XaI`|KGUznIp8WyQudL;OR2I#`Z>9PNKVC?`AOxZT7v$47r!8!Oj+Ks!2%B_EOZ8th<1^b6rnuN716
Go%%-D+qyjxc>5Hn>KAT0m08s4o(MKW4hYBA)FnGe()-EGNis`#=BYF(}*hS)#33M73?RPg4Kuvr7kov-GTb6^Pj$|j?UA$h&|O*;p=)R05w~zwE^Ow0P4(Y
<_iBJImp2HqMC@l`YFZ}IMQqc{Dj^!{=_X{h}hmv#vOP@TG4JV@~Ald&~n*P*%f2%3GrBM$&<pSqV2u0MA6&l|9CM(h1(#7>gNSiz!7b*DxKhlv;z+P7}&S9
W=;RLblMt^7Z`~XY5m&}z&V#v_^Hva%LDg?|LblaD;-%KK)I3RVGlTWSS$234>IF&nk@*i?6<yzL>GDxR6xPZZq!ikk=?)w$xe+ne#A+mt3bTz$`cO%0M6-k
&69(!x0I=KnUYv|e!tI|{;KhfGbn!Um()>DQtjNXX(?&<Rr_GsNOf8~KlM+!rgSWFF(^l$$e9NPTYwBi(oWu9BHt%B6uB9#T!^7Q&uA}dp~`JH0L5$ek!Dx3
2}O;s<olFIz#Kf+fY2h#e2RbR@IaOUA;W9i9N?gtd(02oe)pjq(*TGd*A!TsVV!9sHs8ekGexNb<ELqt+3I2w9R`y7%4WL6*f`daX~><!S|Lm`b9a7f`@SIZ
M8Td1WA3~s0~_?>v$OD7T+mG<O+$DM`0<Qk&nsC7FtTEW9^;u3_MdJsBh*CN>_*2&dA44lxYaH6b7;6$uh$gSf!=#jcir)$tg1;*soNWjaTkvqk%Nd%hB92E
&OrTFDcLiph3U!@ikj_thL~B0H_%ncB-v5&#>?PiIecD?^z;jpCOaxm{nHmmd~XH4cn9^<!9-$C&pPIKXD7-`1+>V7!%3`MTXX%607Luerw2MYfv}hl!3M&5
w#1rbgNsu{FG0U<tc@Z_FRl5A=vO7LeGnRH7(aZH1)xbA%cBQ)m8HP)jv3x68Ovb0G|ld~m-YFc3xgj{ai(w*EMH!!IP*l(nLu8t00maMu4`J5MU(hNRJ_kH
cg0oVbq1Ty6SG<b1i}CO6mj;voch8-x~d#KV3r%->d!QN3pHg=AL{*1>*TqFT9|QmtLel2OxlC8p@zcLTzbWeW5!Y6b3vBN$>?o=)q{vUl|rr=zgSj;nD$y9
4R0Zu|DRZy!2QzEmiww=Mkd7y7hqFqHo4x^KSJclrr3)^DmKS2)wO13e)S2CeMAwN$&<5`z*xaLgCN@GBz-EpThp5xYlV|o>a`Gs2Y4Ia@fe8TO~mCkB)YkY
?1OMO8o*UfUeC>%;5DD|v9l1_v`&r|%gqsc*7jSwqt7PjPQ=(pr7Q*0r&UvMX3@%0+H6krd;20{wo78k2JHn05wsEIUgMJ*p5fVspTK{88YkQA-sy~=8}@z;
+(I-}85jIBVLf440S-lonCoXWdhDK7k}4--ehL7{%fC_*={PU9<tGd|fr|9BOXdNHI)BXQo+}KZ*&KEIst#1hointUQVK@1i{0GZD-i=zxLE@5HK_9i1wdZD
G#;75XHqOyi*zG6yzYbw=udRyZ;5HP^c_y8i^c%sRAbn~K&k@U$nRF%wElKCTMz1y(Um#F;QBMsR7~{NX`T{Uc)tJ=Q*C8vcS40w8P1fYvA+!GEV8Pm%gO(g
-RVs}x%VSeSdTgHK|s|6$?mXJ73>e9BLaX<MQOh<!cwtI+xY;DzbKMl^RR2wQi!ocSQqSdFKvBGQ*1>2Z-8zZc;luQU#D<VNB*enE0VD-jF&vx98Ky?dj$nU
7s|5|Z&ew?O4(1LH<#tZ=sM<O#8wwZ_3QiZN&}-?uf6%$k{h~CQ(C&wIxh}FD&f?=z3h6OIkTlcrEDdsnFpe*)Bi1Rd@ZARQ-`eFPcnDt3c5WA=4I%ng*;u(
Llpi7#d>n{p;Z!Bwg=ZAHH9u#L@<8P-<zB#Qs6E=>Lbjn;uRjR7M7tuU}EIF!Z0Vb*sk!=hxe@t_lfzSabBVbT>|2m{;xlK&sfE?-;65K-_kQ~mBTgA6DkFJ
^h6h>(snE^%8sCxS0<vgXW@?DsQs+0_#41RK%eHZH}X##>N!ZK^sgQcO@t(U<f;*yU?5YNF=ML0QNOF(s1k?_s#-Eg9GOEkM?j-_zAe&?-@b3Z1kMbWug=8N
ly;EyW5PI*mIiWP%tA{@743U+f{FNq$}+QI(<@#-_r4uxE@lA0I~M_jYdD||SWoheh%aeDos!%JIqt(x)<AkTifUm)M^?$>X^VOy>cVT-yAxh3U%D<aR>wJ2
fCyPPx>E?F>_Juq$Xd_qSVFP3dT9iK3ljE{egevC&ZSv|vL-C>2b=>?nW+vAp(hWVA?TAGLdaAL6gbUY&K98+Y>Fia_|0hl644_6GZ%;@6A6Wa;PK&!?Fw(4
D0)**WTrk`jJ+Lmnuc6UxG}rUD^@MM-~%DTXwQ9zx^_RhK>1gAWD)=H9{__LXAkY-LU4IRUCM}a_yeQu)^Y6#SffJEu!8kff!~=Wnn;FwY2$Tr$E@*%d5C6%
Eu-JWPTwdy=pZ0kg6a{kA2#7a6^VP-t-ulhKF2~D8Y54oqY!t+a%L{^lW4nh!qO*ogP*wN!qb@QuSs|4D;vr?kggK8f-s$8n_!DTJ6_+Bv}TDT@eLV>Uu6;W
g4G=rye(2^nfUjJl29k$;H)e%yc(}{;Z4d6y_zrl7>7>-i3H;*&^@eiE4l4R;ASy>*85pQxz8wfA8Hg@;1NpUwi}M@d@0nAFY(KPxE>}fr)7BrsPG6^^6q2%
;}#iir~(A<SfRRaly=J>dOw*yP&@nX%1=-lc4vGHq{7#Xb;!?24=qlK)b=G0w>O$&1WG_Do5FQvl=ylo>Iu3MEqZMib;U;|16dnBgm0`;>8TblJMM=}8(^Th
4)R^e26nnHQ?UZ;1G6A73J2ve?E7?Hya`t$v^uGo(;#OK?@NSXAgWe{?NAH|iR*c&JvDKH<#Dm@esiww+Oh{USI63JY#bQ%MpS12pUQmXK2T8q!W#7w>-w;e
ltGZHDKA^<^-UqOtr>AJt-z@l>~KoE0PccgSb2{?#!Y_0-M`FF$_(0k^9?i<PSqV^)=I;OlPIa|l-Z`()(+MWz1(Vq0VPV_hxFIC<__{pHNGYmnkanC9)`fF
O`5Xnc6e}cBbtRuYJ-AU54zKb4faUxwESlH<IE55SoxiKYuv$>VS*q8KkBTK7d27$ysbN8$!unJ*HqI|#uL|#K$VX)JTrpQOX<BT^(nE}YP%SerOo@<?AgXh
eHdTes}7Y&hzo#=zi6ScvbII50a-uuYDIgv3oA|*Q`~#0GC*i*!ha#EdZ&g6ofN<BScd}5^soCVY2a3neWj<5Z;OTxIGi$<81<HO)@u-ddCZTbk+#L(a<%=g
u3`Iy#cOMcFi)S`UxfqJH5iFjgcJQh;kSC^gt!QSN5xb6y5A99iYgAE#I*t;)(p}g3i#<>R>TGs!g~z%1rOWjKv7MrZ%+?k6@JG6(^dk3J{l)Y+(c;ogtJQy
uJ*+IYgw0vrs!s`D{;=Gg<D3^D4ydl4@c?0X-0G{{VLZhiS}^wRk}pRp6S1BuMmWadv{Sfs_^Q{z_k3&f4oE>^s<>shhPiOh)DbgAL)pTx$c{YRienaDvZdb
Pi88zHq4AhG+ZeEg;rGXBqP>B)0mIqK6_x4&m^qj$|p|ZBdbD+=iIKx0tsLxTv<=qq+X2~N|Xd3e`IkNvWi8&R>NPYprMkP)?}=yD89b9V-yWP$?Y<SQU5lz
H#;hMy^_zIXvOC!+FU=FZ^KjMV;3`#(?8v^p9*e;qfld9ji<gNU&_J=Rkyg^8<HCkE8z6xR_8&?@aYLhAP`gGlbB7>sM$TKRN?)5Ka+bD$6)~Q3nA|CK1Q(9
NsHKo=*xxiO`R^8+_#56g4;0-<41VB48H3sP$)AgBwBj^hOq{nIBdl3U2P5iet6(K!2om&=m_I@Xb-X0HHJg%1>r8j%gonvD42Wz>jeN#*GSwj>a~T&vw>B1
_OU^%in9HtoSFRrB411*yKr8XJZkHZJN@?rR^BedG4c*UXzG;PoMuQJXAG084eJqsZJPxpmwpx2OEDES&;QZu!*1Amgie=dVGE|t<%>ZN%L7qSf0W0=k>k~n
+IwRYPIcpCY$JgId<eDSUa0`bOI>R$F-S3ir$6!pkk?t4UuMAAawpg2*)X>}2AFNZcn{p7u{9V4VhAO@6=YdS!56iuy<IW()-htdY;`Ul{i;IJL#=9^tTiZJ
mxftb-6WFSpLNEqcX+#i+NDcyTHzW6VF+s&UNDYXMhV<vlb~F4ozaJh5m?at_m7_NCTps~v@^YjQLhO}EwRvS+%@I^0eUlIuCH9wAfUzR!GLH7=l~Zvz?$8*
X$w6jr4tWgaI!7j71$NR@)O?XQTYH!*rc^1lrH!K(G+ESyA`~`{%bp3G}Jrp6gxB1w_8q$mxxGjU$^UbCYYkf;=5dK6CEG{a81;qyKVsyo*j+{vpRA6_)%u3
y#fpkRxMMl*{kHrmDTQDaJppkCvQvhV^t&noj!L-hPu|7l|Ij|{q%>M>|1J#nf!P7xGE^XK4Fb+Kr%I+@JB-r@=Zg2IER1~FewBRko__TL({04IuBktA{+Ev
${0;OWi2o`Bkt|A>AH5&=lnlyj-M@`nOcBhk8=LB9ea=Q<ORwhpuQN?G4M*_TGXm>87-09IKg!gUv;q?(<;24a1aui&bdS^n58PQV+=sMzw(?2J)4BdtJxKs
<PGVKG5R0Mp-^66@GBkl7Ag7$9SeXEmhbQj|2)~*T6p<=Ud86=Zn6hj-#S$o45$E9Mw0^Sv!tm7faG8#pwTu<*PO0ZEJ5Q@770_ES!to(3}s%DZMan5Mjr>j
c6!w`!|?qcw1mt?uP|F&Igc*Oe{|-L$;GXoPif-oA7ED7%?4ItUj2k-b1!sv+Wjy=ke2110?xz`-HCa9^s4-3gvup1Z`MUx=igbgG^sKBNzczwMYgf(Jt%{o
$Un>)L3rz0%!f+pnDQoB{d>(OAP*6Ddfq2+A9A$cpz3pJSRY0(;gL{DKi#`xRrN+jM^D<{r};6j`SM^SsJ?KNdg85lICVjce1|_{b3c8udt<1JE`ke0?KX{a
_BK~=yDj@T{=uz{<L_%#<Ntw^&|Pb<SL$ARuPuejVJ^8R!j~>$4^Ojl`w9~udte4ViTV8im>-DU%S|3PzG+79xig;`hdAAnVA`i0#A<i*)|bAe14XC3eC!J7
8R8Nh%C8#!x?j{lW6*Kuz(ZTIRDGv9X=}@$n6VPE)yjQ6whD{9wFg0Nwjc}Gxt0c^A(@MOGH`-scFUP8QLIPaFY>!m@_cKd&UfNVtIZLNP_}NZ*Y1dKrab9g
K|M{5ea-bo=nI29_gDF?KIC}PBK`b@o3l$;Y4U<m?VzV-L!Fx}H&Zrr`R5HOFD|#b+|=m=2?bJoydc8JtZpk!aq>kp7Roz@Q}KW{YsKVvDfyg*t+CNp&1{c9
<P_t0bMhphm;9n(I;Ygd0X@*#6m9`k=T2X?dQbgbf09P=A%o+*Qmhed1jF`-^V_1)w|jN2ECP)hpim7<HEOWV0@tuxEzpnF>qWPc?F%;6#f#QFIdP3k_q#ws
`MOoO-JpU!B3`e9e-X>V*qoL`67V0{5$Z>ksPa-qDP&Xir;Ms!PgJzIPW2OrN)T21-m8FTn~18F2Wn0fz??jpD6l&YZt>Ayr~i+s3#*UE&&}1NYNfMhVfZpj
U8Gj<W7D$K0;k*B!TAqW2ZOuF1RBV)ewm*xpMtj1%NlWvrf)uGn5~vF=Icvvg7gm9za>}iDsow8^B(ta!a2uL`p5=o)ou^Ohpb@E>J&%f#*4`fjj7U8wtfeS
^S*H05(|dg2z9wdZvkT#MRWwaRYsg}_xt(DV)h)4^etJCW<?HjK2~;e-kEaGA%7((#y#3fER9#Nqrc5QOouBPVq~jhgeCgH;(V}cf!2-%y2>3M7c3et&Xl~~
PhRimY^g#@T|<ZzO(_!JNSWAqL!Z<BDFdRoc~6KAoZo1EM*gxyaD3dSSi6K3D=45#6rf`M9ysW!WrwN-9)|o5pL5Mcf|+X<m>8>^g*dOqdkl}Uixr@jK6ZC-
ZTu%ylG~N<S%$u9sYzL>Zbv%v!d|7iqFUkdCTuayJr*Rf!%g@fX#k)q-F^lSxm<ihIAObO!g^=Qa-rT&FJ5*+h<483#1A0^wci=4@BWxBaZ$<`Vl=V~I|mA$
kCY{Xfu2<`nt&1~9!g2MQ&@YXDm%bDT*5)S!i-<2bpBW+u?<#Ujh2?<xW9;Bjjxy)c&`LXLRi;9(juWM%&KMG4b*s%VMe{Abug=Qfn8XVxvPgzmi4f4flm^l
XV4rjmo)1bKTNV8(%{4>GFh$gISU(s=|q4w?vM0MIOWu=ZO^)rXO+i|r!Pqfdcno9jE!<o3JRz@>L<j0^X=OLPN4YBEC8`)L!Mqv=r#3%DjI_APKkucXrEK~
Q0eiKqu_vuqh&m68wmz={WREKZyC`0n$~We|G2q|<xo-<lkB;O0+l3tn)M8+Ac+`dlPdWa5>Hgix(uF#R|vO#I<Z6d!7{QZbeR3$+DpxEa}2!xLMogo0>TAx
%igcC<>&_C_crhHl?CiNTA=c$Zu_yb?B=Q6eJzn7#_`WBZ0=Lln@DPRCYfVirudCOKT>`<l=o$1cKal~o_-Pv)((f?k5)H0Nu2-FU_s*XxkGf@&m1VhMGm$q
O@EBMJrEyQ8IQylHclqb6va;Sup5zH_rB-hGiRH%JHl`G*U`s*s!y@OT)Re(Z*;WTj71*3`pbpB<%5%OOwunh;Y7tpt;cd>q|aHs2c?LM1yrY#?cJYGq;qTm
+JPgm@Oxuofutf7q64m9mKuYY&$ZHOFb{rNs~dB42URkO;nFe8cVN<lJIb`V4!MV&6=0w>b;i?M96Anz5a^KwLP`{L*qRii{EC{mR0~99yj;aP2L+0>iZswm
_*{xeG-?CEiKC+i`VG&aBMEd}{4<?3b6Si@2)2DxzcWR-C$iiK9hqyNK;&HzzbnJs;tzNYh^13A7hGh#rFI~~+q#Y<VonKXU{N%%0v2-rCWzu7&4r4rK$Fl;
5~7k<bMit<QAy;PXXE;A!<iJvdVC^jHyM;Ka+e!VXe>gT!~IIMb|xLp^v=Em$g70UT(GA+@%vsZ?)YGu9bTdIpWRSyb<|u0wJ5n0Xyyvh<7YGs16u9(!i0}9
Pes&%e<AtPVUp5zL-v|q7RAE!l-p4|Drwm0dnBxjxVW!Z#+RuA(`ss~ydVC3=ZwIfxJ)TPbS~XU0fGj4t#m2*T|%2ndW7;YNh?!X;M38i@6N%M{SB>C8xn`H
)#>bffpmDFt0AFiEXm1=ntL6a`yTRdrFhFTcVBTe7GtRn^MIC1Nek{5Z;wAlP3UW<Z$!Z-y}%h)a+}TEUxDiv>4a0HWUZ{eHCX#HEGQIU(XYxPK<Knvco&8N
RbfSZvXZ>pM{-FnWk)^8Je+kcT<|@y^Y%Wg-$(k|W59i76hWXbqt*!=mN6|~AIWx=_-OL$G*SU5q-c|S@fy8zxZXGpJk9BA2eE&O4qCQg#c`gl6Aaa7S2Rby
$#vjFV>wMNKhGQF%mECY6G_=NA0ea!LsIMKJ2O)Q_%uLTnmhr!Ncm-&oxI|sM+!dTmh|F!nqAvG$R)-Fv^&G84#&kIV;arGcoAqfVInHgvpWUn1)m6~Y7}_v
*D?niL?f$GiFjhs3g9|bZ*<#7wol`cn-n`b>wz6MD9L&ey!+EX4BE#d04med*(1`EI1G@K-wtg7*MUf_MshUvNphK;K6<OV+)sdsE36&b+c^jIU<3ZD^F3SV
1(J#Nc4t`@`trRE$?E73t@9L`@jgGTR1ptM_N^E`1ZX{VOJqS;BOv?S6N`XOW}cHHlZkVkpFH~}d7$9%3W$x>&|7F?)!ML?I)EPIA8@<Nd~s2ed4b~Ja65|@
;v(h@Am<2Nvh3Vvx+btP)_99eaCyv#&x*QND-DII^B1I4U>3gL#@%q`)~*+gOiPUD<21!}uqT-{3hPb%qD+?XUL{UHe$*V+i*SQtElI@JlKo1pSC2proV?K%
1=vDQ4>yGx(#t6ZPB19ew!PkBe*dW1hDskS16UXLCF?T&&=dLqFgsEK>iI%gDC1Hy_k6-LVhCT0^%Mm?0!O^o@8JR#e(5~tgceAF5HoBv$Eq!<dg40fDc*Lh
`^FK#X%WHnYH-)*0Fo}m94X`~Q4uI=lvAHHOht)o0B%)>MRh|wZ=+)@S}nU!oqlq%vhiLb3Bg9AqcvKLb%9)OFAJ5kh7T!T5v9797{IIV$hd8HByxOau-7%n
*sALx0y8}Pftf{CN;vkLXR?3KI8%#Ba8MZrJ%Rfl5UOgfSo%ct?#fZrns$@~T;|FD{E_bY+~JG=`+A=uh&4)M;;&z3o6Y>az@qV7z{&}Nm2d*p*UWRNDGQbw
ZaK=FDJH60+7IU)vRk(;&N`5h(L85Dw8XwJSZs07L0T7EPu8~z7_%&B)nu8r9l((C@K#?t+I3m}+BPsmtDk8mVn*%}Th@9EL9qE<jTgf@Mi&O7q2Z}=enlCb
kr>&I%7f27(C^IEIRAo<ziVxUOw@Df*fTblY!4zzfZPTK?S{1xv?^EVOpu>IW3nPmaFRA&ZN!viPXzvo=i(nRi2{tqNKry%Dkw<b>HjWvvb3grwgFLIRJb;G
FLJh0XPohhMT8mNEjUn$xJ4KvQHA9L|E=9J26p#Ofzf<^F1nu752~`epVZ&6X8P4A*QE2Ga_=<-E-3_}cDqko?I<>-XMm8-$nES|g?D<afv5#YYCRp&&_#~)
B{ugV&%9Q8_wtS@OTM@ooINn(0V})P%0Nh3VtaH1j9fXS5`YM}6Zgon!u~t(A-uUFL&TwmMgxa2NM?3H3Lm5gDoiggigh29@G=KpO^MB~HT@1uM6H91ns+kM
qZrU!s5*6aU<&%>7>dl{mpab1ekb6>MvlC0jT(07=h*NSIUe@tv_0e7+@CZqP8C2zMeVlO%)*Onu0JiUFKlbda)xo8EXc~mOKtB8C;gD@cC9NW!-=wKuY|Mp
5uz*p5ka|RrzrWO0*LX)hkVNpDXjj~PVAA=P46WuB~?MSyMNG}7o05*%ybT#5>Cj`Qqn`gZe*)<%ejDD?41>oSj#{n;YbZ*89TwOBY~1>Rjfq8@zBmUhS%C`
Sg}KMzg;t*_3@nAW;r|9*(lo$`?24l*PK)bDo;HW2G<04^ud3QQt?86_TE7oPn%%70}$%3V4QWc@qZT#r24v<Q<OG5CZkie2dZcgGwYXxwK>bCpq-)BlRTc5
&Keou_^dpw?^by1$Dy4Lv#SIURj(YfH;o{yS`n@tnP^MUka;_|MBnS;;wI<Iz==;rv&8&5sZyM8tCu&aT8ikM*Im%LREq`lMDP<8y$qN`JfuF_8vScOBR9MS
E%FgyQsv%R1Iw)s>r7;R(&s&IWS_GRccN<U(0NL+A*AIN#lP<77~KOx&>U;o_8@4qK7wQ*rN5cG@W%!m+01l}2Q<};;omLNl98q5`q=a4vkW`QFJ3wmyrpQE
3TvPuA0XbCJ-VMKW4|iNZ=@<Mh|DU?$3?7}?^IN*?c<ZveWmPPg{&!a_g^qHKcEPnU_ObHC*-}bX~1Ab>19yrYz*^DTITaQo!U`W5H=5991@XZD_+0|s6&wu
(TADl6-@-^ZZ;PTa@jA*WVphw-IHqR6-9L7>@2T94d?1mQ-lf7eZ&q<kc_pkx(h69U0P-5fY7fDQHY0ZHLd{g|68<UP8_pp1|nP$;wQlw-SzQh(@FzN{-)wQ
=7t8d9q^<CJm{J~rtgJ@!0#rF@c6Yk=T#uB8Fj7`JmX+`td4i4Wm5coo;#fy1%q;bd=wa_E{*YmgoDu%onKz3LltGwH4d&2%cuduElw1Bi)tI@9n5f^!=)Fo
_;yL!JSmR|MC|(48n%@w<3a(Ti?S{(q|&dR2!ZEU9NUS*v$?FgUU_a(N!9UvUE;d5y1F|EEVZpoydd%2=z`Q>Qk9pUFqWB=y>J0BB}8<j#5LR}UT^Iu?#ajA
RI-5cs!%K1d5^#`LrD~8{~VhAcf-|AMJf;bT)xiN$8l9_ZbC6!CeO@GMoYNFfrXk?4AKKR8kQY9C%GZ=%8T&qhNQ-mvv5Hw3WwkLD|1KApKkV)OPzK9(uZhK
YF^0ZQFM;iLvdOtbusW~*e2W+r%;O|zxfcUoIETE|2RC}*EUuNzc&Dm<h9uT+nqp3VESzygJPmhx+Xe4i_l^$onI+d!joA<>xKlU^hn1lrk$>e$aaj#N2kZm
UO*Qhrbm3YUr)Zgnch1J117<p<8zgU&y!|>mg-%*4wNV);WO`eOhM^th2-L|(RQc(X|YE;bG&U6#;2DKA*$v*Yd)Kw{Uv_S=b-jw{UWp1&Wwd{6R-UNt2=bq
O<Swk2IgK?06S+dh-eccGgFs7D(Au8oA1S_;vp{=0*BS;uYEdy2l)>FCK9jN87i8dxh-re-K@F=M71=rKlDb&7k3IO;i|bhCz||F!-;M{k@+)*zfzY{oOT_>
Qjd9UYW1E;Zo@}l0=6_s66;)8pS2s6F1Rz*SDKFkJgB5Wtu~tw=7?qD^<RscUHGL3JWtcH)nzn+7y!Kn6{#ovgL}pM`>Bvb6C9IRV6KA1Ks`^fA=2fQ8pr<d
ImpXyaEhS2NTt9ED8Z|5VO^v&)uiDVRuy!rg`@wuiWCo7@4JN5-mX&V!AvmE`Y9)^ucoNC81RIU>uX$w%$=UNa0fa9P5^*7d*_s_>A}(OiLue?M&C&~!8OZ{
bn~S5+}!~_dj9Yky%buOt!Bs7%wls`Kd*{bS)<Zu@jRnZo9zf|?GAv-e@vBTrC~p^cld1q`YKrP5n>KLFCH$(4CI76dFXNoZt28Yk_SsfG-+_=JLc<4D!de7
af{P++Vz<SCwtr<aWTOSkjxQoYp}nsI^d6FWaTi1XE=kk+`M_W4J5m3mt)Y|G+M=BL|ThT<H&`sq(8%lz9Z`pxen1KXR9G1Q~{xp-kzT8&Tlo2jGtGTxZOiz
%hU2US>Ii*0g*DK7(U1O3}x4-JPk|h%#T+b4W_X(ELsP_*T!hI0Go4j__mo56DN{6*^ps{{Z@|fo7rK2BHh3s!%kFIN5L38!_DK4y5IL&6oTUP<+R2B6;QBq
PxU|ui#2}8f6g2<+#*OA%+Y)PR2}DiON%R0`@TOQ--6+}ByE?l!{L1ad#o_#>ZeVl)3%s_>SnUvV|8lyDw$F%ggU%nql8je5&e{~0rUPD4ZSi_t#pG*3W-nx
)JIia7zCt;3c)}iC_5+FrE>kOe7_DImj$w>=Ixr3{WEvk0U+0{S;n9nEQcALz`jvVL(10Pe_|Z17eBv}iUEK1O}a(f%~_~_@t`e+8Sg0S&yR)+z=_OyVlc9N
$G`Mca4#bNs^Ta|_i*^NwJ45=+#WZ7a32-_{a+5S5wu8=EQbh&qCPpU;IO${%(OZ9>932$s~%)jZ$r21zK1k?xPZE1phqTiWh#H)9%^B%)5`fH8>Q!+|30fJ
98$egX1G~nqEbF=+;h1$_1sV1CrTlu?@#|F$-9~e@mgIfM1O|MAb892O6H6Ea8*rRh}^zn?QEACG{ByzowP%Pn7^tfHX*R~*FrSv9G!Dd0x-KQ1TgY?7gJ)$
gXzqoYON`=m|6{o{))V1(-Qr<s7$oU;3(HUOmbWEYyP5}ag;UGVTeBpuhV6q{o=zZgqOZi=c|i!>QYoVIn1gZCRI%3u^KA3xTT6vmPfa6P&dsk`yA9-_Qhy>
z#ky<^m0jj0Wn~?N9mw?d+b`H?F5{HcEKuc-!$WuT{At#!9dr1O1PI;+IPevgLJs50hL08rx%?a$#Zi0EH0X<4AabGWu{R2S(Ol4=K3_U1ClTaGS^N5{hV$i
2H?9c?6=$S+^g0!3T$XsyC!3FSh{6*E~jY(xl4;Pnp#IYL+XEl{e8?-f1}lKm7)X|zcf%|`iuJ{q>hO@%mI`uCB28MV=IaK&eO<;3b$4>LJ-G~N!#EbT#^d{
@obGlkV17DpcxyavI1ULsh^Gwa0ghvU~wqq{{|`na2-!|lzWuR&nsyNqNMlAH5F%m2*KJf-N-;)L~)!qp#LRWO%@jh%fu0nHVymNn&M&iog2XDd|EW?ZmQV&
Ee(;aUDM|^#P+rt?oWP{%ziYQEjiLreL6<7$*4*<iGxi&g>Yb_0tTsr5TQ3n*1n~IZe*VLl9=v~GF*wKaby5Mv3D*~w!O4ju)Ab#MO)R7SZ61qzP1uh@~O1d
Duj1xL43f+q|or$jap8wz++M;Hjwq_mda9U6OZeYc5Z6BdJvT;53UO~jZ)X)bT5Kni?EczohN(zg^_KQT^Dk3KunD>W3w2oU9p;bYZ<i*rhdw#1MT|}RAB~;
;dXeZpQcr6FR8#Wg*-~UTqJn5%10Q(`|QDOv)Of#eLJk(zC9!%2h?J64zzSwB7RsSK`8T$sX-5TLRHCgGZxr-89dFHP<H9I(vh9Xdr(48si)MYG9s$qq*Rab
l&v6y+)o{+#lIU%5+K?nONwm9BKiA-_hmKJ&M#&$TBO5eZeVU3-F20BRE6MVkG1r;>hg0?zW8d;IMgq|kPg7hvKLC~L9(EwTb&np4ypFVRvn$VoH!eQvNaul
9jwE=ELsIzDOQnnw$#p1!hATXs)(APp<%>Ch2_tqwRnrQ!Dzzjx1XK#G~w$9OV4Os9U~tI^uU+b<7HR=w-)PlAN<32ejRqN@%D#JF5aDlxf`Z+GOC&%%#!iT
Bv?&zcdJL;?V`6mYZ3>4h+S>$9p7Q%%Eo{@m6f5taNfmIJC~%{&mimgpCd6_(8>ws?(3xzl?_WNEU%Cl(%<`Mz(NWE@4R?1dBbi5a^t{TJGn`W<tGbs8&6M^
P#gK0B_)}8oY*#mEm5Jrsz_?uEA&RF2+V{xIojV$`IZP{^V8-d_P7QTcjtkJ>sZSBf*+Yr!j{|$p*P0us1WmBa(@y78LPigxUh6|ID|?SiwpIh+<dJI9tIE=
u!?a0<aXS3@GL}psWF(ruFu8gw&pF@8R7BVV3q?BuS$mqFQ(Y-_M<{hlj)(}n!&g9>7XPEIEnMeIeeOCL1;52Y+BrGSG>HrOFFK<F7Q+gvLfcf2F*^Ai;QEA
7z1mfJ7jICRxCO?+c3IST-OxiBYC~u5l1z6YTB4TQc@Va$G+ILx;YQspTl&8<)RX#ufHXzwU?M<ncQCI|7pLL=HIs$hsgn#(;3@?;3>rCfCVF$fJ|yR7+V=f
ZM~2<5-r2QpRGENzyu5JiMNN;WdjEdUq=)_LDJZm{uDk8+Pz4mY%!b%?<S&<igo@xa33snaM|z0`he8UF?pM@H)j_gtdHQ8eC^@BCjjwwi*bRmaF+ca?$Yk9
*SxckP0UdS6cC=Yq+R!S)#|Z=KQYf9hgyjdX*ew`wzF)YpzjM@?ug$98386CV@-mZRPG%lx~2F(D#u<}S^9vh2V(+wQIsWekQAX&PURTc?hK}U8Q2K_%<a3Y
VH2wlg;BwhaA_n2biy=rXmQ052xdSnGxo-yjmOwbwmzV&*o&WTuOi{E?%e7!7AnhIO7Q2vU9hrC>ir_DUQVHlng_$P1;A>h&SP3Oo+bV{&`yWY0gZJN+Zhr@
p_T~-p9@#qa56{Gjc!3ex1>@Gp=53`a(K1?8IBQ!!c)luZ652v^=|Ha=n2rfk&r#OV1lpf$a!NSO!7&N+YB2veae4>BaR#lj2@C8hMih^@`>kEbMB2b2aP6l
mEm>Q%eesI9DBE%fQ97_+7)kbD5ZlMk;hA11z^^8L);Vq<uz9vz-c@<#NtgEy+6@5H71G11W$IU*F}-qB>!}Q?>3s@LkUM|n^b>X#0*_yLO_(D-?)Xu#($v9
psb&DE*Q{Eo#ZPc?Krb8T*Gy6hSmmT_w4jZnFBbMfQgoK6He9&N(@4)CFok;rZ;CD>nKF0F@oShs#^JZUCN%*vps&sd=FW?G?g#$!_Fi(s;pdd6D`X{+1c{!
OKz`+f|pl13HSo77qbJhp425L?;KKSI+Yd-C@dB~?8XzX4Y70~Z3sag53|lh>qaULN5YvmLMI7<+8)6y+x+aaB*1U<=Ya8c*?NLoM8+`TTM09)CCfd^?OpRS
?hf&18GL6PSd#*KuaL?%&VrHd2oo{nNjxGM2l$617ko*_`6WqPI07grexW2;rnWzozxZP~s42!8b71a-a)lbgujvqA2B>E@tVu;VX}M;0wZY@W`y1T6-^#`h
MpMmFq)x0WMy)|o)^P+<*EM2wvn_iq1}@`VK4M)4R12FUidqf75x;n)NMb=0s3iF~y!*y^`EUXh=0YX$9Iq4!a!<_#eXveKOpHZDjM+a`;hjYj4BW}Q##G{Z
4R&xk>A!yh-pRp*!6oBE0g(=^?Z3E<K)=~>nM<_Z_QJU4aJmwB9CSHy77*w9mSUPen2=CwmAf5-I00mfozrE`>#6Dun|Uf6*E|n~>#Q1ced5nFZxDqM<$cWn
;ys=I>k}VI>jfPpd#L=>-E1eP_tG4PnM2w`8qqKe{OpPF)Jc;6W*9<sv!N^z`uw07HIy<lhUWvr`c~tgQ=2efg+7-nlldqxHUo3PQVLAl$^2G})D6e7YASqZ
P`53S4bQ6I%`-5y{9;89_=qx?LJ&u5zQoaAauTVi6G)xGiX|Lm39#t^&6q2v9(r+UKf&(#0#BitA&%ua4a;ng2uD-C!(dlpL3oF`JOSZNKhGrrac<9(Nm?ko
5z-$41w5E{nB$en1psj<eF9xJ2ia+Fn+{VcTTND|dxIC3nh>8F7mYD_foNIF%-+l1lOFi!rJ%Nq$s+k_zTu&jQ_tkNoJzO<lzT?j%vXKm+%qJ{r#`n*z%z^F
t~){zqh`MNF79w=^`no7Fe&R836!=SBQ{mf*>wR>pxfQNsmc9%d-1x-Yz4JH0ncaO=*!2Ie-U$Av;hN4RZwf<Y1?Pm-ehcgI!aE6)y^RsgM>i@B;hiDdF7K(
)hw=+wpp_}3sp;YeN+pkxZHh-;T2ocW0ypSoZlmK*|klsKjUmDA5D|8InK6DUrpf~^P@|jwx`#%pNiYDh-miuaTYfo6$^kGv^8lbY?2*p>lG=I&?yL3RO}ku
aNl^h0SsSR)zmI=x>(k?a7%@6cohQdeI3F`WG7j^;UFpi`m8(dj+MCriSUOHKw2|g3}X4pl`;>tJ0uz=w^uGVdOPe8L!Q<mw^gdKzB3InPuva>7vGSG4QGc5
fefOdX?d`BWffI=9UH7~Lj+z`%DeU-=y#V>*oU+IfqCF~egJrfC<#sYpGq8|)ZJGS^^-YIMVtkaPF8B_-~oG<VqLm~`FZ2^jeA}gniC{YZxc3wz9vYCIeLwL
dKnY!6{$nc?(X$LLCT@1P6`+3b3a1Tu(}t~u_Q`Nob;hf+na?Xbd6U2acZG`_z?qC8CEgZEyU|AuzCT{VBW6||73CYuqdI;wJP|7HK2poA`shmdum>AXY4+V
d0|5M15WvarZ-zSv%5wA%%>e52B(0U!TILRXR<Io{8JK!3+lbnmFs`-BrolXJcIk!GtFiE<)m|{)q-cQ4v$;T)@=VtPLxKw*5QZy9=A7g9mc=f&5r4e^!b4R
SIe=?F}bE1WnmqFD<k96%d@njgd_@Y7wQw{jIL`u6xQ?ITdM@-#~K@}q=2~OjRo>ML$gGALHH|O@Cmh0|7Zw16qCaTzPH!X2kWy>E%;~(=HYwp*_WOAxs`et
hcHLzxm%Qid_gU}P@~V2u_h5+#y_<zI5UwQn2wk6ue94@%+$4(R;YJE?{BL1?>5qvh~eh+bg2B<h)rNyF^;blU-EWv7i*Lk5rN7U-=&ry)0u+hs}@>ex9Y&V
kKzlwSvU{KOEb<Pkx*V1fSQ{&vy2LNA73OwkY~VjNf`&I#?NpXuUTCvy()Imi8&NAz%ge=O`98AXN$|06$Gonpnc_<IM0kIBP|e$!)XaLDl-Hg?ZFehHx(fm
?_cHMNc~Viw-+(Ub@xh`I<`UR{hQYF({sb5eR46~gx1mFkFO!Hc~p|L_%CZJ%foUql=mi?W%GYr7`z2ni;x?2q;S+y@^+=)dvKS9=f|@lADo~^4#5}28p+$o
dH|E;h-Xu3g_>P#p;StM8dZUZw&K8QS}KlSvW`OVNL~V&t$vLA%&^L}T7lmm&a#pat+Y?*_;7N8!~>Zo4!$gUn_})J!2nJq;MV<OE-M{3mN{~NV_u}>E)*Z$
0p=pBf9UpKuM(^6!WQLTf%Lr2VyDxg3t~L<?^Z!uB&G1zBP0-3n0QHD5M>l~iU@Lc=_?I>!$$d1a^3kwDnfG0d5Om{B!0Sc*=ZJ8PzeB8^`a%WzTuXyLfqsz
1wE1^rHy9@Ricb~o+RQc+|}&xa)A8fwp14h=v*~UmpLPBClXl6cxFS6R<Ck05IiY7xB2G1lJ4@yu3R><GbmO+O|yk|Y@2{`+1KC84*kmo!2f3kKM5ZIr=tAt
u4+vu1q7scy<9gH15pC%b5sHfGyse_E_RqP6|RP-SOw&OA8pt4eh(0v6%2Gg%W^RdUSX;E;p3HspmKES<iDwWvcsN}8#@B0_?HSs{XpXfhx&On3>?#(!Pu&F
%QvS#GL45DdN67#2O6?M9eFMcf8WxM28!S3i~jJMry4w%u*S-eP}7J{f)NLl)A0($!|&!^gKEgxFl}b@D#vsak`PlRPO^iKe6bx5^E$XzGLxIamYv@RckIc(
&gfF}$TfuwOzNzYA1`wjB>9do!UNB5JHDPm#O?;FtQ?pAbdzT-`+Y~Cu_d5qK$H`8ze9I<W=^9-JkpC(U7tU5W8ZeZKV3}GNK}h%@TlL7{O-pf8?aE|lS@E*
$xNQ2w$#d?3A387(wDuHE4Ral9T>=*X#;F+r~7F2oX84@MS(aUE7h$lCg{_g<9^`Jv<OSxj6FFTHe#%7atLIhJ_*1xm7(wm6Hf97ioG7jlKI_dm=?|O;nSR5
jqd*-+<WOs2iz9EQ25~F&Wcoa*+=zH3Q*N7X<_X#!fzNGgg09$Ej92hVj7P*JY&=yCyHl5wojA=qEy=wF}wv)H4M#eX-*$oDC+c@1>2@ZZ~=Ir1akzD4$W%E
a4BT_pY|8P)~ke%8==ripd%KU$}MVjcG0m&Q0&VT&RFSez5`YuGq4~HBNDoR=)Ol_Gb=*sMXay64ZjV`j)7yTjvnCs5da^C{f=e?acYg_C@1W&!<py!qU#`{
u3md-EBKNRe#N~ln;OuV?Inh9oM`CA#)7pq11@&V8ShH6*y6>tj$uz?z&d6RHKTOfJ(K}2S2~(2ejqPJ14KpCnB-KpOn|l}Rv)K4(&^WImmeq(ZJgs~ps3;j
Xah2SMm5h6mb*rq1r0tz9>C|v#rb8{<>g!uDdm5q(mP{w7=@kyiWLz{eRpJ(qLORgs)Tqu<2n&lIp)n9jYTTEmLn5W2_<a0%xT%>SusQ09kS30wYNfvUeInn
Lw?t7`SO^6<X}KvnT;K_68Ea<q~xt-z<5&ln9H<2cv6bV-D}S4_e6jHs;$`PW+w?ZB(&xd;ycMkkJ~1uae|b~hwW0?oJ?zQUcW=BkDLql-<dA$ecFRzeyb)u
rZ=zEo(a@eE?gQ)x_8IZq>@~t&g8;F6Nw*}QM8jB$s&r;@p<A+ITpajxVjJYP(=tpEn1;Yei;C@Z|4W_I@!-|khUL=7{TMMu@&pc6J0Vcayp<nNdHxpAa<#V
-1)Phh%&^q9#B)c_~hP37h_qpO_zKQ-xHsw^m3KLzkg>c`09UAj5VoOh~9CBsSvsI+QIBK3bNE8jVzuX(^7vM(2C6{S^UAr8W&jCWW<Y+Di{#RfUZ_YW#q|>
T{D%bdknhy<P1$cUBSDKy97tJ(rY&eDB8U2B(>+;-}|87+3Li(7YB()jcKFmy1RMsdNSe?bCEUF%B`8Q-xv<;V&TnO=GcU`Yhvn}Z!beaZ&^jEF-K}7u@H;Y
))y6`1o>{Gwml@{tTW7UYCFzkLcF;tgZWev(IOM9yntT+-lZZXimKk&H7Xs?^Ygk7u2YT;RN4=+u8Daq<YW@=zm>Pgp<`TVlj?JVUE+OmeXB;O&D9d)ei<gN
B{X(!qD(2Vh10YKj?JMVewN&-zZTBR!JiT*P7aRKhN^Sr{our()9&Ii>Rnr=a%MC9c6eI*%>eExt@siwG=F1TDrUy^aljbjykIn*OnBR{*d48K_VJDA0dk4@
zU3UEQR^y{Fk0B-D3>elY_!r^rmAD@LIoj-&>I1VN-1N?IKWdfyypg13-${jk26h1eq?u@t$0Z*wBgMu@0cLlQI_F(VoVukG=8hCwE8vEHbkky3cV)%Th&>-
)0T7eVhvTGM_vcRr&lML4Fnpub4|s#_OAb37&sg)BxLzN^x9XosGYcwwU?G<P$yoWpgrLM9&%vfy6jdR|L%x8|L)$!fhup?>p^((K?d5R1*~8qd5qp8>r+(|
%CohSb3V*iX>sW+My?`73v>BqG5IzM35%CNpo?yjnDq*WU+fgv>u5A1BRSpZf@okLE(|*m&3*s9c2eDgSvDK)3!^|Om7Vd#=rVF<^QI)B<%e6kqRJ&~jm(|0
k5~L7xV#(rt-l_&v%GE|+VaO1q_-Y?Ep*Zv4`g2&ND{<6=Nit1jDvWz6x9KU@+VBtZm-UqV*vfKC%%!b;rIZ=J)D<A<&rX4Ov+E3OIx*M4bQ49ag8~@dPPW@
mV4kj=DY@gV~2eArqsi47sOAzdiK8z+VwN2m3mbh@paon3cZ)Da@|DO#+7Fd%~`!Ln0uzlH>X$^zK39e_R!5q%-u<BLqbdIYt@+rD5Q0XX-%(@+YX3e)p4B<
WAS3@SHcTintJA*AK7gtI$$AIaNeyJ=fT9$sreL?L)9U=>)<m^a#C-=I#ck7+Bs<iuX`;Xgkaw881Hlt-!Ag^079dIaVTGXs7iy9CBRlFk6CKomvKuc;$v#u
TAGcAagfm#>Zch-oE~7tmsWPd2?FY(JeL9yb|g<>`;4W+pz9VANF5Qb!RJ~A+8-ZpvG14<GL}`e;>1V#NvR5RK7n#W|8a4_GPp>WWs@a^5^;JS%F<VLYU&-V
(uZGmx@~C~=ddQ2>E_z5UNb%FFWjNP!L8BtrOx|9A|IKxxKqCT>nH#KhleZed?@(Q00HR50^_16ditKQvBYQl0ssI200dcD
```
