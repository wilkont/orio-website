import {feeIllustration,formatUnits} from './fees.mjs';
const amount=document.getElementById('amount'),range=document.getElementById('range'),scenario=document.getElementById('scenario');
function update(){
 try{
  const values=feeIllustration(amount.value,scenario.value);
  amount.setAttribute('aria-invalid','false');
  for(const name of ['fee','company','holders'])document.getElementById(name).textContent=formatUnits(values[name])+' USDC';
  document.getElementById('amount-help').textContent='Illustration only. Network gas is additional and is not estimated here.';
  document.querySelector('.allocation-bar span:first-child').style.width=scenario.value==='ordinary'?'20%':'100%';
  document.querySelector('.allocation-bar span:last-child').style.width=scenario.value==='ordinary'?'80%':'0%';
  document.getElementById('company-rule').textContent=scenario.value==='ordinary'?'20% of collected fee, rounded down':'100% of collected fee';
  document.getElementById('holder-rule').textContent=scenario.value==='ordinary'?'Remainder of collected fee':'No eligible holder allocation';
 }catch(error){
  amount.setAttribute('aria-invalid','true');
  for(const name of ['fee','company','holders'])document.getElementById(name).textContent='—';
  document.getElementById('amount-help').textContent=error.message;
 }
}
amount.addEventListener('input',update);scenario.addEventListener('change',update);
range.addEventListener('input',()=>{amount.value=range.value;update();});update();
const steps={convert:['Appreciate before minting.','The approved purchase sequence appreciates existing eligible holders before minting the new purchaser’s tokens. Zero-holder purchases allocate the complete conversion fee to the company.','Approved policy · production integration pending'],hold:['A transparent allocation mechanism.','Eligible conversion activity can increase the reference redemption price. No extra ORIO is minted for appreciation, and outcomes are not guaranteed.','Approved policy · no guaranteed return'],redeem:['A common opening price.','Redemptions within a batch use the same opening price and exclude redeemed tokens from their own appreciation. Full redemption allocates its complete fee to the company.','Locally tested · live redemptions unavailable']};
const tabs=[...document.querySelectorAll('[role=tab]')],panel=document.getElementById('step-panel');
function select(tab){tabs.forEach(t=>{t.setAttribute('aria-selected',String(t===tab));t.tabIndex=t===tab?0:-1;});const s=steps[tab.dataset.step];panel.querySelector('h3').textContent=s[0];panel.querySelector('p').textContent=s[1];panel.querySelector('.step-status').textContent=s[2];panel.setAttribute('aria-labelledby',tab.id);}
tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>select(tab));tab.addEventListener('keydown',event=>{const j=event.key==='ArrowRight'?(i+1)%tabs.length:event.key==='ArrowLeft'?(i+tabs.length-1)%tabs.length:event.key==='Home'?0:event.key==='End'?tabs.length-1:null;if(j===null)return;event.preventDefault();select(tabs[j]);tabs[j].focus();});});
select(tabs[0]);
