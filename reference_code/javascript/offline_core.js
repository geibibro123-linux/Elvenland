/*
 * Elvenar Offline Lab 04 - pure transaction planning component.
 * No IL2CPP hooks, no network calls. Intended for a separately verified native adapter.
 * Original game values are never guessed, initialized or globally replaced.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ElvenarLab04Core = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const TARGET_ID = 'R_Elves_Premium_Residential_1';
  const CLIENT = '1.244.0';
  const error = (code) => { const e = new Error(code); e.code = code; throw e; };
  const isObj = x => x !== null && typeof x === 'object' && !Array.isArray(x);
  const clone = x => JSON.parse(JSON.stringify(x));
  const int = x => Number.isSafeInteger(x) && x >= 0;
  const validTransactionId = x => typeof x==='string' && /^[a-zA-Z0-9._:-]{8,128}$/.test(x)
    && !['__proto__','prototype','constructor'].includes(x);
  function context(c) {
    if (!isObj(c) || c.mode !== 'offline' || c.clientVersion !== CLIENT || c.allowNetworkFallback !== false)
      error('INVALID_OFFLINE_CONTEXT');
  }
  function costsFromDefinition(d) {
    const v = d && d.requirements && d.requirements.resources && d.requirements.resources.resources;
    if (!isObj(v)) error('UNVERIFIED_BUILDING_COSTS');
    for (const [k,n] of Object.entries(v)) if (!k || !int(n)) error('INVALID_RESOURCE_COST');
    return v;
  }
  function effectiveDefinition(d, c) {
    context(c);
    if (!isObj(d) || typeof d.id !== 'string') error('INVALID_BUILDING_DEFINITION');
    const copy = clone(d);
    if (d.id !== TARGET_ID) return copy;
    // This must be supplied from a verified original live config, not just the asset ID.
    if (c.verifiedTargetId !== TARGET_ID || c.targetConfigVerified !== true)
      error('TARGET_CONFIG_NOT_VERIFIED');
    const costs = costsFromDefinition(copy);
    if (!Object.prototype.hasOwnProperty.call(costs, 'premium')) error('NO_PREMIUM_COST');
    if (costs.premium === 2) return copy;
    if (costs.premium !== 80) error('BASE_PRICE_UNEXPECTED');
    costs.premium = 2;
    return copy;
  }
  function validateEntity(entity,request) {
    if (!isObj(entity) || !int(entity.id) || typeof entity.cityentity_id!=='string'
      || entity.cityentity_id !== request.cityEntityId
      || !Number.isSafeInteger(entity.x) || !Number.isSafeInteger(entity.y)
      || entity.x!==request.x || entity.y!==request.y
      || !int(entity.level) || entity.level===0 || !isObj(entity.state))
      error('INVALID_TRUSTED_ENTITY');
  }
  function preparePlacement(s, definition, request, adapter, c) {
    context(c);
    if (!isObj(s) || !isObj(s.city_map) || !Array.isArray(s.city_map.entities) ||
        !isObj(s.resources) || !isObj(s.resources.resources))
      error('MISSING_GAME_STATE');
    if (!isObj(request) || !Number.isSafeInteger(request.requestId) || request.requestId<0
      || typeof request.requestClass!=='string' || typeof request.requestMethod!=='string'
      || !validTransactionId(request.transactionId)
      || !Number.isSafeInteger(request.x) || !Number.isSafeInteger(request.y))
      error('INVALID_REQUEST');
    if (!isObj(definition) || request.cityEntityId !== definition.id)
      error('BUILDING_ID_MISMATCH');
    if (!isObj(adapter) || typeof adapter.validatePlacement!=='function'
        || typeof adapter.buildNativeEntity!=='function')
      error('NATIVE_RULES_ADAPTER_REQUIRED');
    const definitionForTransaction=effectiveDefinition(definition,c);
    const costs=clone(costsFromDefinition(definitionForTransaction));
    // Never subtract or create a city entity twice: native adapter owns execution.
    for (const [k,n] of Object.entries(costs)) {
      const available=s.resources.resources[k];
      if(!int(available) || available < n) error('INSUFFICIENT_'+k);
    }
    const before=clone(s);
    if(adapter.validatePlacement(before,clone(request),clone(definitionForTransaction))!==true)
      error('PLACEMENT_NOT_VALIDATED');
    const entity=adapter.buildNativeEntity(clone(request),clone(definitionForTransaction));
    validateEntity(entity,request);
    if(s.city_map.entities.some(e=>e && e.id===entity.id)) error('ENTITY_ID_COLLISION');
    return {requestId:request.requestId,requestClass:request.requestClass,
      requestMethod:request.requestMethod,transactionId:request.transactionId,
      entity:clone(entity),costs,definition:definitionForTransaction};
  }
  function simulateAtomicPurchase(state,plan,ledger) {
    // Host-side reference only; actual native gameplay must provide a separate adapter.
    if(!isObj(ledger)) error('INVALID_LEDGER');
    if(!isObj(plan) || !validTransactionId(plan.transactionId) || !isObj(plan.costs)
      || !isObj(plan.entity)) error('INVALID_PLAN');
    if(Object.prototype.hasOwnProperty.call(ledger,plan.transactionId)) {
      const old=ledger[plan.transactionId];
      if(old.entityId!==plan.entity.id || old.requestId!==plan.requestId)
        error('TRANSACTION_ID_COLLISION');
      return {state:clone(state),ledger:clone(ledger),replayed:true};
    }
    if(state.city_map.entities.some(e=>e && e.id===plan.entity.id))
      error('ENTITY_ID_COLLISION');
    const result=clone(state);
    for(const [k,n] of Object.entries(plan.costs)) {
      if(!int(n)||!int(result.resources.resources[k])||result.resources.resources[k]<n)
        error('INSUFFICIENT_'+k);
      result.resources.resources[k]-=n;
    }
    result.city_map.entities.push(clone(plan.entity));
    const newLedger=clone(ledger);
    newLedger[plan.transactionId]={entityId:plan.entity.id,requestId:plan.requestId};
    return {state:result,ledger:newLedger,replayed:false};
  }
  return {TARGET_ID, CLIENT, effectiveDefinition, preparePlacement, simulateAtomicPurchase};
});

