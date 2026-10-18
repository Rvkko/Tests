// Local QA practice target. Synthetic credentials/data; not a production store.
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {newStore,setQuantity,snapshot,checkout}=require('./store.cjs');const sessions=new Map();
function send(res,status,data){res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(data))}
const server=http.createServer(async(req,res)=>{
 if(req.url==='/'||req.url==='/app.js') {const file=path.join(__dirname,'../demo',req.url==='/'?'index.html':'app.js');res.writeHead(200,{'Content-Type':req.url==='/'?'text/html':'text/javascript'});fs.createReadStream(file).pipe(res);return;}
 if(!req.url.startsWith('/api/')){res.writeHead(404).end();return;}
 let data={};try{let body='';for await(const chunk of req){body+=chunk;if(body.length>10000){send(res,413,{error:'Request too large'});return}}if(body)data=JSON.parse(body)}catch{send(res,400,{error:'Invalid JSON'});return;}
 if(req.url==='/api/login'&&req.method==='POST'){
  if(data.email!=='qa@example.test'||data.password!=='PracticeOnly!42'){send(res,401,{error:'Email or password is incorrect'});return}
  // Bound the memory used by this local exercise server.
  if(sessions.size>500)sessions.delete(sessions.keys().next().value);
  const id=crypto.randomBytes(24).toString('hex');sessions.set(id,newStore());res.setHeader('Set-Cookie',`qa_session=${id}; HttpOnly; SameSite=Strict; Path=/`);send(res,200,{name:'QA Learner'});return;
 }
 const id=/(?:^|;\s*)qa_session=([^;]+)/.exec(req.headers.cookie||'')?.[1],store=sessions.get(id);
 if(!store){send(res,401,{error:'Sign in to continue'});return}
 try{
  if(req.url==='/api/logout'&&req.method==='POST'){sessions.delete(id);res.setHeader('Set-Cookie','qa_session=; Max-Age=0; HttpOnly; SameSite=Strict; Path=/');send(res,200,{ok:true});return}
  if(req.url==='/api/store'&&req.method==='GET'){send(res,200,snapshot(store));return}
  if(req.url==='/api/cart'&&req.method==='POST'){setQuantity(store,data.id,data.quantity);send(res,200,snapshot(store));return}
  if(req.url==='/api/checkout'&&req.method==='POST'){send(res,200,{order:checkout(store),...snapshot(store)});return}
  send(res,404,{error:'Unknown route'});
 }catch(error){send(res,400,{error:error.message})}
});
server.listen(4190,'127.0.0.1',()=>console.log('QA practice store: http://127.0.0.1:4190'));
