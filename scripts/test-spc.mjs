import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile,readdir,stat} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {feeIllustration} from '../site/fees.mjs';
import {pages} from '../site/pages.mjs';
const root=fileURLToPath(new URL('../public/spc-3/',import.meta.url));
test('all 28 pages and the missing-page document have working internal links and local assets',async()=>{
 const files=['index.html',...pages.map(([slug])=>slug+'/index.html'),'whitepaper/index.html','404.html'];
 assert.equal(files.length,29);
 for(const file of files){
  const html=await readFile(path.join(root,file),'utf8');
  assert.match(html,/<h1[ >]/);assert.match(html,/Financial (?:services|operations) are not enabled/);
  for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){
   const target=match[1];if(/^(https:|mailto:)/.test(target))continue;
   const [name,fragment]=target.split('#');let absolute=name.startsWith('/')?path.join(root,name.slice(1)):path.resolve(path.dirname(path.join(root,file)),name||path.basename(file));
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


test('whitepaper PDF, published source and launch disclosures agree',async()=>{
 const read=async name=>JSON.parse(await readFile(path.join(root,name),'utf8'));
 const source=await read('whitepaper-source.json');
 const manifest=await read('whitepaper-manifest.json');
 const readiness=await read('launch-readiness.json');
 const sha=data=>createHash('sha256').update(data).digest('hex');
 assert.equal(sha(JSON.stringify(source)),manifest.sourceSHA256);
 const pdf=await readFile(path.join(root,'assets/ORIO-SPC-3-Whitepaper.pdf'));
 assert.equal(pdf.subarray(0,5).toString(),'%PDF-');
 assert.equal(sha(pdf),manifest.pdfSHA256);
 assert.ok(manifest.pages>=15&&manifest.wordCount>=6000);
 assert.equal(source.financialExecutionEnabled,false);
 assert.equal(readiness.financialExecutionEnabled,false);
 assert.ok(JSON.stringify(source).includes('Stablecoins in African Mobile Payments'));
 const paper=await readFile(path.join(root,'whitepaper/index.html'),'utf8');
 for(const section of source.sections)assert.ok(paper.includes('id="'+section.id+'"'));
 const sitemap=await readFile(path.join(root,'sitemap.xml'),'utf8');
 assert.equal([...sitemap.matchAll(/<loc>/g)].length,28);
 assert.match(await readFile(path.join(root,'robots.txt'),'utf8'),/Sitemap: https:\/\/orio.io\/sitemap.xml/);
 assert.match(await readFile(path.join(root,'.well-known/security.txt'),'utf8'),/Contact: mailto:contact@orio.io/);
});
