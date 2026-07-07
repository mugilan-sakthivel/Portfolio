const u="https://gist.githubusercontent.com/mugilan-sakthivel/7430d2ac7a323ef732c8d31d08e0e68b/raw/location.json";
fetch(u,{cache:"no-store"}).then(r=>r.ok?r.json():null).then(d=>{if(!d)return;if(d.tz)window.__LOC_TZ=d.tz;const el=document.querySelector("[data-v2-loc]");if(el&&d.city)el.textContent="in "+d.city;}).catch(()=>{});
