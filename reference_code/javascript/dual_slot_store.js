/*
 * Elvenar Offline Lab 04 - two-slot snapshot store.
 * Pure JS / QuickJS / Node. This is NOT an Android Storage Access Framework adapter.
 * Only an adapter with atomicWrite (write temporary then atomic rename) may be used.
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.ElvenarLab04Store=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const SCHEMA='elvenar-lab04-snapshot-v1';
const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
const H0=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
const bad=code=>{const e=new Error(code);e.code=code;throw e;};
const isObj=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
const clone=v=>JSON.parse(JSON.stringify(v));
function utf8(s){
  const bytes=[];
  for(let i=0;i<s.length;i++){
    let c=s.charCodeAt(i);
    if(c>=0xd800&&c<=0xdbff){
      const low=s.charCodeAt(i+1);
      if(low>=0xdc00&&low<=0xdfff){c=0x10000+((c-0xd800)<<10)+(low-0xdc00);i++;}
      else c=0xfffd;
    }else if(c>=0xdc00&&c<=0xdfff)c=0xfffd;
    if(c<128)bytes.push(c);
    else if(c<2048)bytes.push((c>>6)|192,(c&63)|128);
    else if(c<65536)bytes.push((c>>12)|224,((c>>6)&63)|128,(c&63)|128);
    else bytes.push((c>>18)|240,((c>>12)&63)|128,((c>>6)&63)|128,(c&63)|128);
  }
  return bytes;
}
const r=(a,n)=>(a>>>n)|(a<<(32-n));
function sha256(text){
  if(typeof text!=='string')bad('HASH_TEXT_REQUIRED');
  const data=utf8(text),bitLength=data.length*8;
  if(!Number.isSafeInteger(bitLength))bad('HASH_SIZE_LIMIT');
  data.push(128);
  while((data.length%64)!==56)data.push(0);
  const hi=Math.floor(bitLength/0x100000000),lo=bitLength>>>0;
  for(let sh=24;sh>=0;sh-=8)data.push((hi>>>sh)&255);
  for(let sh=24;sh>=0;sh-=8)data.push((lo>>>sh)&255);
  const h=H0.slice(),w=new Array(64);
  for(let off=0;off<data.length;off+=64){
    for(let i=0;i<16;i++){const k=off+4*i;w[i]=((data[k]<<24)|(data[k+1]<<16)|(data[k+2]<<8)|data[k+3])>>>0;}
    for(let i=16;i<64;i++){
      const s0=r(w[i-15],7)^r(w[i-15],18)^(w[i-15]>>>3);
      const s1=r(w[i-2],17)^r(w[i-2],19)^(w[i-2]>>>10);
      w[i]=(w[i-16]+s0+w[i-7]+s1)>>>0;
    }
    let [a,b,c,d,e,f,g,j]=h;
    for(let i=0;i<64;i++){
      const s1=r(e,6)^r(e,11)^r(e,25),ch=(e&f)^(~e&g);
      const t1=(j+s1+ch+K[i]+w[i])>>>0;
      const s0=r(a,2)^r(a,13)^r(a,22),maj=(a&b)^(a&c)^(b&c);
      const t2=(s0+maj)>>>0;
      j=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;
    }
    const out=[a,b,c,d,e,f,g,j];
    for(let i=0;i<8;i++)h[i]=(h[i]+out[i])>>>0;
  }
  return h.map(x=>x.toString(16).padStart(8,'0')).join('');
}
function validSnapshot(payload) {
  if(!isObj(payload)||!isObj(payload.game)||!isObj(payload.ledger)
    ||!isObj(payload.game.city_map)||!Array.isArray(payload.game.city_map.entities)
    ||!isObj(payload.game.resources)||!isObj(payload.game.resources.resources))
    bad('INVALID_GAME_SNAPSHOT');
  // Player/session credentials must not get into exported offline saves.
  const secret=/(?:password|passwd|(?:auth\w*|refresh|access|session)\w*token|credential|authorization|cookie|privatekey)/i;
  const stack=[payload];
  while(stack.length){
    const obj=stack.pop();
    if(!obj||typeof obj!=='object')continue;
    for(const [k,v] of Object.entries(obj)){
      if(secret.test(k))bad('SESSION_SECRET_IN_SNAPSHOT');
      if(v&&typeof v==='object')stack.push(v);
    }
  }
}
function envelope(revision,payload){
  if(!Number.isSafeInteger(revision)||revision<1)bad('BAD_REVISION');
  validSnapshot(payload);
  const body=JSON.stringify(payload);
  return {schema:SCHEMA,revision,payload:body,sha256:sha256(SCHEMA+'\n'+revision+'\n'+body)};
}
function decode(text){
  let e,payload;
  try{e=JSON.parse(text);}catch(_){bad('CORRUPT_ENVELOPE');}
  if(!isObj(e)||e.schema!==SCHEMA||!Number.isSafeInteger(e.revision)||e.revision<1||
    typeof e.payload!=='string'||typeof e.sha256!=='string')bad('INVALID_ENVELOPE');
  if(sha256(SCHEMA+'\n'+e.revision+'\n'+e.payload)!==e.sha256)bad('SNAPSHOT_HASH_MISMATCH');
  try{payload=JSON.parse(e.payload);}catch(_){bad('CORRUPT_PAYLOAD');}
  validSnapshot(payload);
  return {revision:e.revision,payload:clone(payload),raw:JSON.stringify(e)};
}
function createStore(io){
  if(!isObj(io)||typeof io.read!=='function'||typeof io.atomicWrite!=='function')
    bad('ATOMIC_STORAGE_ADAPTER_REQUIRED');
  const files=['slot_a.json','slot_b.json'];
  function inspect(){
    let seen=0,broken=0,valid=[];
    for(const name of files){
      const text=io.read(name);
      if(text===null||text===undefined)continue;
      seen++;
      try{valid.push(decode(text));}catch(_){broken++;}
    }
    valid.sort((x,y)=>y.revision-x.revision);
    if(seen>0&&!valid.length)bad('NO_VALID_SNAPSHOT');
    return {current:valid[0]||null,invalid:broken,seen};
  }
  function load(){const i=inspect();return i.current?{revision:i.current.revision,payload:i.current.payload,recovered:i.invalid>0}:null;}
  function save(payload,expectedRevision){
    if(!Number.isSafeInteger(expectedRevision)||expectedRevision<0)bad('REVISION_REQUIRED');
    const prev=inspect().current,rev=prev?prev.revision:0;
    if(rev!==expectedRevision)bad('STALE_REVISION');
    const next=envelope(rev+1,clone(payload));
    const file=files[rev%2]; // a for revision 1; b for revision 2
    io.atomicWrite(file,JSON.stringify(next));
    return {revision:next.revision,sha256:next.sha256};
  }
  function exportCurrent(){const i=inspect().current;if(!i)bad('NO_SNAPSHOT');return i.raw;}
  function importSnapshot(text,allowOverwrite){
    const incoming=decode(text),current=inspect().current;
    if(current&&!allowOverwrite)bad('CONFIRM_OVERWRITE_REQUIRED');
    // Always write to a slot; revision must grow when importing into an existing install.
    const rev=current?current.revision+1:1;
    const dest=envelope(rev,incoming.payload);
    io.atomicWrite(files[(rev-1)%2],JSON.stringify(dest));
    return {revision:rev,importedOriginalRevision:incoming.revision};
  }
  return Object.freeze({load,save,exportCurrent,importSnapshot});
}
return {SCHEMA,sha256,decode,createStore};
});

