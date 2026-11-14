import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile,readdir,stat} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {feeIllustration} from '../site/fees.mjs';
import {pages} from '../site/pages.mjs';
const root=fileURLToPath(new URL('../public/spc-3/',import.meta.url));
test('all 26 pages have working internal links and local assets',async()=>{
 const files=['index.html',...pages.map(([slug])=>slug+'/index.html')];
 assert.equal(files.length,26);
 for(const file of files){
  const html=await readFile(path.join(root,file),'utf8');
  assert.match(html,/<h1[ >]/);assert.match(html,/Financial (?:services|operations) are not enabled/);
  for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){
   const target=match[1];if(/^(https:|mailto:)/.test(target))continue;
   const [name,fragment]=target.split('#');let absolute=path.resolve(path.dirname(path.join(root,file)),name||path.basename(file));
   assert.ok(absolute===root.slice(0,-1)||absolute.startsWith(root),'Link leaves static release');
   if((await stat(absolute)).isDirectory())absolute=path.join(absolute,'index.html');
   if(fragment)assert.ok((await readFile(absolute,'utf8')).includes('id="'+fragment+'"'),file+' missing '+fragment);
  }
  assert.ok(!/https?:\/\/[^"\s]+\.(?:js|css)/.test(html),'No external executable dependencies');
 }
 assert.match(await readFile(path.join(root,'styles.css'),'utf8'),/prefers-reduced-motion/);
 assert.ok(!(await readFile(path.join(root,'styles.css'),'utf8')).includes('@import'));
});
test('approved illustrative fees conserve every micro-unit across scenarios',()=>{
 assert.deepEqual(feeIllustration('1000'),{gross:'1000000000',fee:'10000000',company:'2000000',holders:'8000000'});
 assert.equal(feeIllustration('1000','zero-holder').company,'10000000');
 assert.equal(feeIllustration('1000','full-redemption').holders,'0');
 for(let i=1;i<=1000;i++){
  for(const scenario of ['ordinary','zero-holder','full-redemption']){
   const x=feeIllustration('0.'+i.toString().padStart(6,'0'),scenario);
   assert.equal(BigInt(x.company)+BigInt(x.holders),BigInt(x.fee));
   assert.equal(BigInt(x.fee),(BigInt(x.gross)+99n)/100n);
   if(scenario==='ordinary')assert.equal(BigInt(x.company),BigInt(x.fee)/5n);
  }
 }
 for(const bad of [1000,'1e3','NaN','-1','0','00.1','0.0000001','1000000.000001','1\n'])assert.throws(()=>feeIllustration(bad));
});
