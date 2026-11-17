/*
 * Elvenar Offline Lab 04 - LOCAL SESSION COORDINATOR CONTRACT
 * This is host-testable orchestration, NOT an IL2CPP or Android integration.
 * Does not contact any network and never turns an unsupported action into success.
 * A verified native bridge is REQUIRED before use by an Android game client.
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.ElvenarLab04Session=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const REQUIRED_STARTUP_FIELDS=Object.freeze([
  'ancient_wonder_phases','unlocked_items','featureFlags','featureTechnologies',
  'knowledgePointPackages','resourceSets','seasonal_events','player_relics',
  'premium_prices','production_boost','relic_boost_good','idsOfUnavailableChests',
  'effects','army_details','city_culture','city_map','city_population','features',
  'guild','resources','resources_cap','settings','runningBattle','runningDiplomacy',
  'trade_fee_percentage','trade_ratios','user_data','decayTimer','mapSize','season',
  'privacyVO','craftingSettings','guildBannerConfig','tournamentProvinceUnlockTime',
  'runningScout','cauldron','lastUsedGobletResult'
]);
const bad=code=>{const e=new Error(code);e.code=code;throw e;};
const obj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
const clone=x=>JSON.parse(JSON.stringify(x));
const int=x=>Number.isSafeInteger(x)&&x>=0;
function inventory(data){
  if(!obj(data))bad('STARTUP_OBJECT_REQUIRED');
  return {required:REQUIRED_STARTUP_FIELDS.length,
    present:REQUIRED_STARTUP_FIELDS.filter(k=>Object.prototype.hasOwnProperty.call(data,k)),
    missing:REQUIRED_STARTUP_FIELDS.filter(k=>!Object.prototype.hasOwnProperty.call(data,k))};
}
function createSession(deps){
  if(!obj(deps)||deps.mode!=='offline'||deps.clientVersion!=='1.244.0'
     ||deps.allowNetworkFallback!==false)bad('INVALID_OFFLINE_CONTEXT');
  const {store,core,network,bridge}=deps;
  if(!store||typeof store.load!=='function'||typeof store.save!=='function'
     ||!core||typeof core.preparePlacement!=='function'||typeof core.simulateAtomicPurchase!=='function'
     ||!network||typeof network.createOfflineRouter!=='function')bad('LOCAL_COMPONENTS_REQUIRED');
  const methods=['verifyInitialState','verifyLoadedState','getBuildingDefinition',
    'validatePlacement','prepareNativeEntity','verifyTransition','applyCommittedState'];
  if(!obj(bridge)||methods.some(k=>typeof bridge[k]!=='function'))bad('NATIVE_BRIDGE_REQUIRED');
  // The original FakeCityMapController.RequestPlaceBuilding can mutate state;
  // it must NEVER be called here as a pre-commit entity factory.
  if(bridge.canPrepareWithoutMutation!==true)bad('SIDE_EFFECT_FREE_NATIVE_PREPARATION_REQUIRED');
  const context={mode:'offline',clientVersion:deps.clientVersion,allowNetworkFallback:false,
    verifiedTargetId:deps.verifiedTargetId,targetConfigVerified:deps.targetConfigVerified===true};
  let current=null, revision=-1, poisoned=false, busy=false;
  const ensureActive=()=>{if(poisoned)bad('RESTART_REQUIRED_AFTER_NATIVE_FAILURE');if(!current)bad('LOCAL_SESSION_NOT_STARTED');};
  const router=network.createOfflineRouter({
    'CityMapService.placeBuilding':r=>{
      ensureActive();
      const request=clone(r);
      if(typeof request.transactionId!=='string'||!request.transactionId)bad('LOCAL_TRANSACTION_ID_REQUIRED');
      const existing=Object.prototype.hasOwnProperty.call(current.ledger,request.transactionId)
        ? current.ledger[request.transactionId] : null;
      if(existing){
        // Replay is allowed only when request selector and the original placement match.
        if(existing.requestId!==request.requestId||existing.cityEntityId!==request.cityEntityId
          ||existing.x!==request.x||existing.y!==request.y)bad('TRANSACTION_ID_COLLISION');
        return {requestId:r.requestId,requestClass:r.requestClass,requestMethod:r.requestMethod,
          responseData:{local:true,entityId:existing.entityId,replayed:true}};
      }
      const def=bridge.getBuildingDefinition(request.cityEntityId);
      if(!obj(def))bad('ORIGINAL_BUILDING_CONFIG_REQUIRED');
      const plan=core.preparePlacement(current.game,def,request,{
        validatePlacement:(state,req,definition)=>bridge.validatePlacement(state,req,definition),
        buildNativeEntity:(req,definition)=>bridge.prepareNativeEntity(req,definition)
      },context);
      const result=core.simulateAtomicPurchase(current.game,plan,current.ledger);
      if(result.replayed)bad('UNEXPECTED_REPLAY');
      if(bridge.verifyTransition(current.game,result.state,plan)!==true)bad('NATIVE_TRANSITION_NOT_VERIFIED');
      const updated={game:result.state,ledger:result.ledger};
      updated.ledger[request.transactionId]={...updated.ledger[request.transactionId],
        cityEntityId:request.cityEntityId,x:request.x,y:request.y};
      // Must commit before returning a success. A failed write cannot mutate native state.
      const next=store.save(updated,revision);
      current=updated;revision=next.revision;
      // If native apply fails after durable commit, block all further operations.
      // A restart must restore the committed snapshot before any new request.
      try{if(bridge.applyCommittedState(clone(current.game),next.revision)!==true)
         bad('NATIVE_STATE_APPLY_FAILED');}
      catch(e){poisoned=true;bad('RESTART_REQUIRED_AFTER_NATIVE_FAILURE');}
      return {requestId:r.requestId,requestClass:r.requestClass,requestMethod:r.requestMethod,
        responseData:{local:true,entityId:plan.entity.id,replayed:false}};
    }
  },'offline');
  function boot(originalStartup){
    if(current||poisoned)bad('SESSION_ALREADY_INITIALIZED');
    const saved=store.load();
    if(saved){
      if(!obj(saved.payload)||!obj(saved.payload.game)||!obj(saved.payload.ledger))bad('INVALID_STORED_SESSION');
      if(bridge.verifyLoadedState(clone(saved.payload.game))!==true)bad('SAVED_CITY_NOT_VERIFIED');
      try{if(bridge.applyCommittedState(clone(saved.payload.game),saved.revision)!==true)
        bad('NATIVE_STATE_APPLY_FAILED');}
      catch(e){poisoned=true;bad('RESTART_REQUIRED_AFTER_NATIVE_FAILURE');}
      current=clone(saved.payload);revision=saved.revision;
      return {source:'saved',revision,recovered:saved.recovered};
    }
    const found=inventory(originalStartup);
    if(found.missing.length)bad('INCOMPLETE_ORIGINAL_STARTUP');
    if(bridge.verifyInitialState(clone(originalStartup))!==true)bad('INITIAL_CITY_NOT_VERIFIED');
    const newPayload={game:clone(originalStartup),ledger:{}};
    const next=store.save(newPayload,0);
    try{if(bridge.applyCommittedState(clone(newPayload.game),next.revision)!==true)
      bad('NATIVE_STATE_APPLY_FAILED');}
    catch(e){poisoned=true;bad('RESTART_REQUIRED_AFTER_NATIVE_FAILURE');}
    current=newPayload;revision=next.revision;
    return {source:'original_verified',revision};
  }
  function dispatch(req){
    ensureActive();
    if(busy)bad('CONCURRENT_ACTION_BLOCKED');
    busy=true;
    try{return router.dispatch(req);}finally{busy=false;}
  }
  function status(){return {started:!!current,poisoned,revision,mode:'offline'};}
  return Object.freeze({boot,dispatch,status});
}
return {REQUIRED_STARTUP_FIELDS,inventory,createSession};
});

