document.addEventListener("DOMContentLoaded",function(){const t=document.querySelector("[name=csrfmiddlewaretoken]").value;var e=new Splide("#secondary-slider",{width:"100%",fixedWidth:100,fixedHeight:100,gap:6,rewind:!0,pagination:!1,focus:"center",isNavigation:!0,updateOnMove:!0,trimSpace:!0});e.mount(),new Splide("#primary-slider",{width:"100%",heightRatio:1,type:"fade",speed:100,pagination:!1,arrows:!1}).sync(e).mount();var n=document.querySelectorAll(".lg_item");for(let e=0;e<n.length;e++){const a=n[e];$(`#${a.id}`).zoom({url:a.getAttribute("data-zoom-image"),magnify:.8})}let o=null;if(document.querySelectorAll(".current-attribute").forEach((e,t)=>{console.log(e.clientWidth),(0===t||e.clientWidth>o)&&(o=e.clientWidth)}),console.log("[ MAX ]",o),document.querySelectorAll(".attribute-names").forEach(e=>{e.style.minWidth=`${o+8}px`}),currentPath=window.location.pathname.split("/").filter(e=>""!=e),currentPath.includes("variable")){Object.entries||(Object.entries=function(e){for(var t=Object.keys(e),n=t.length,o=new Array(n);n--;)o[n]=[t[n],e[t[n]]];return o});const l=new Object,d=document.querySelector(".attribute-container");d.querySelectorAll(".attribute-row").forEach((e,t)=>{l[`${e.getElementsByTagName("p")[0].innerText}`]=e.querySelector(".current-attribute").innerText}),console.log("[selected]",l);const s=new URL(`${window.location.origin}${window.location.pathname}`)||Window.URL(`${window.location.origin}${window.location.pathname}`);d.querySelectorAll(".attribute-row").forEach(e=>{const r=e.querySelector("p").innerText;e.querySelectorAll(".attribute").forEach(e=>{let t=s;for(var[n,o]of Object.entries(l))n!==r?t.searchParams.set(n,o):n===r&&t.searchParams.set(n,e.innerText);e.setAttribute("href",`${window.location.origin}${window.location.pathname}?query=getit&${t.searchParams.toString()}`),console.log(`${window.location.origin}${window.location.pathname}?query=getit&${t.searchParams.toString()}`)})})}if("none"!==window.getComputedStyle(document.getElementById("cart_row_lg")).display){const u=document.querySelector("#increase_quantity_lg"),m=document.querySelector("#decrease_quantity_lg");console.log("Running lg");const h=document.querySelectorAll(".product_quantity");u.addEventListener("click",function(){h.forEach(e=>{e.value=parseInt(e.value)+1})}),m.addEventListener("click",function(){h.forEach(e=>{e.value=parseInt(e.value)-1})})}else if("none"!==window.getComputedStyle(document.getElementById("cart_row_md")).display){const p=document.querySelector("#increase_quantity_md"),y=document.querySelector("#decrease_quantity_md");console.log("Running md");const w=document.querySelectorAll(".product_quantity");p.addEventListener("click",function(){w.forEach(e=>{e.value=parseInt(e.value)+1})}),y.addEventListener("click",function(){w.forEach(e=>{e.value=parseInt(e.value)-1})})}else{const g=document.querySelector("#increase_quantity"),v=document.querySelector("#decrease_quantity");document.querySelector("#product_quantity");console.log("Running mormal");const f=document.querySelectorAll(".product_quantity");g.addEventListener("click",function(){f.forEach(e=>{e.value=parseInt(e.value)+1},{passive:!0})}),v.addEventListener("click",function(){f.forEach(e=>{e.value=parseInt(e.value)-1},{passive:!0})})}containerHeight=document.querySelector("#product-container").getClientRects()[0].height;let r=null;function c(e){const t=new Splide(`#${e}`,{type:"slide",pagination:!1,autoplay:!1,width:"100%",fixedWidth:"240px",gap:10,breakpoints:{1024:{focus:"center"}}});t.mount()}r=currentPath.includes("normal")?{id:currentPath[1],ptype:"normal",for:"viewed"}:{id:currentPath[2],ptype:"variable",for:"viewed"};let i=!1;document.addEventListener("scroll",function(){console.log("scroll"),innerHeight+scrollY>containerHeight-10&&!0!==i&&(i=!0,document.querySelector("#inject-box").innerHTML='<h1 class="tw-mb-14 tw-py-4 tw-text-center tw-font-mono tw-text-2xl tw-font-normal tw-text-green-500"><div class="preloader-wrapper big active"> <div class="spinner-layer spinner-blue-only"> <div class="circle-clipper left"> <div class="circle"></div> </div> <div class="gap-patch"> <div class="circle"></div> </div> <div class="circle-clipper right"> <div class="circle"></div> </div> </div> </div></h1>',fetch(window.location.pathname,{method:"POST",mode:"cors",cache:"no-cache",headers:{"Content-Type":"application/json","X-CSRFToken":t},body:JSON.stringify(r)}).then(e=>e.text()).then(e=>{document.querySelector("#inject-box").innerHTML=e,document.querySelector("#recommend-box").innerHTML='<h1 class="tw-mb-14 tw-py-4 tw-text-center tw-font-mono tw-text-2xl tw-font-normal tw-text-green-500">Fetching Items....</h1>',fetch(window.location.pathname,{method:"POST",mode:"cors",cache:"no-cache",headers:{"Content-Type":"application/json","X-CSRFToken":t},body:JSON.stringify({for:"recommend"})}).then(e=>e.text()).then(e=>{document.querySelector("#recommend-box").innerHTML=e,c("recommend_slider_4141")}).catch(e=>alert(e.message)),c("section_slider_4141")}).catch(e=>console.error(e)))},{passive:!0})});