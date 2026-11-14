const UNIT=1000000n;
export function feeIllustration(amount,scenario='ordinary') {
  if(typeof amount!=='string'||! /^(0|[1-9][0-9]{0,6})(\.[0-9]{1,6})?$/.test(amount))throw new Error('Enter a decimal amount with up to six places.');
  if(!['ordinary','zero-holder','full-redemption'].includes(scenario))throw new Error('Invalid scenario.');
  const [whole,fraction='']=amount.split('.');
  const gross=BigInt(whole)*UNIT+BigInt(fraction.padEnd(6,'0'));
  if(gross<=0n||gross>1000000n*UNIT)throw new Error('Enter more than zero and at most 1,000,000 USDC.');
  const fee=(gross+99n)/100n;
  const company=scenario==='ordinary'?fee/5n:fee;
  return {gross:gross.toString(),fee:fee.toString(),company:company.toString(),holders:(fee-company).toString()};
}
export function formatUnits(value){const n=BigInt(value);return (n/UNIT).toLocaleString('en-US')+'.'+(n%UNIT).toString().padStart(6,'0');}
