document.addEventListener("DOMContentLoaded",function(){let s=0;const u=window.location.pathname.split("/").filter(e=>""!=e);u.includes("change")||u.includes("add")?console.log("Nothing To Clear"):(console.log("Clearing session"),sessionStorage.clear());const t=document.querySelector("[name=csrfmiddlewaretoken]").value,c=document.querySelector("#id_Meta_data");c.style.display="none";let d=null;function o(e,t,o,l=null){let n=document.createElement("div");if(l)n.setAttribute("class","forhighlights-container");else{try{document.querySelector(".container").remove()}catch(e){console.log("No item to remove")}n.setAttribute("class","container")}if("product"===u[2]||"productwithvariant"===u[2])if(!0===t)for(var a in e){a=i(a,e[a],o);n.append(a)}else!1===t&&(!0===l?e.forEach(e=>{e=i(e,null,o,l);n.append(e)}):e.forEach(e=>{e=i(e,null,o);n.append(e)}));else"product_type"===o&&e.forEach(e=>{n.append(i(e,null,o))});let r=document.createElement("button");r.setAttribute("class","btn"),r.innerText="+ ADD",n.append(r),r.addEventListener("click",function(e){e.preventDefault(),l?e.currentTarget.before(i(null,null,o,!0)):e.currentTarget.before(i(null,null,o))}),(l?d:c).before(n)}function i(t=null,o=null,e,l=null){let n=document.createElement("div");n.setAttribute("class","row"),n.setAttribute("id",`row-${s}`);let a=document.createElement("button");a.setAttribute("class","cancel_btn"),a.setAttribute("id",`${s}`),a.innerText="X",s++,a.addEventListener("click",function(e){e.preventDefault(),document.getElementById(`row-${e.currentTarget.id}`).remove()});let r=document.createElement("input");if(r.setAttribute("class","input gui_input"),"product"===u[2]||"productwithvariant"===u[2])if(l)null!==t&&r.setAttribute("value",t),n.append(r,a);else{let e=r.cloneNode();null!==o&&e.setAttribute("value",o),null!==t&&r.setAttribute("value",t),n.append(r,e,a)}else"product_type"===e&&(null!==t&&r.setAttribute("value",t),n.append(r,a));return n}"product"!==u[2]&&"productwithvariant"!==u[2]||(d=document.querySelector("#id_Highlights"),d.style.display="none"),u.includes("change")?"product"===u[2]||"productwithvariant"===u[2]?(null!==sessionStorage.getItem("highlightStr")?(o(sessionStorage.getItem("highlightStr").split(","),!1,"product",!0),console.log("Loding Higlights from session")):(o(d.value.split(","),!1,"product",!0),console.log("Higlights not in session")),null!==sessionStorage.getItem("pageMetaData")?(o(JSON.parse(sessionStorage.getItem("pageMetaData")),!0,u[2]),console.log("Loding pageMetaData from session")):(o(JSON.parse(c.value),!0,u[2]),console.log("pageMetaData not in session"))):"product_type"===u[2]&&o(c.value.split(","),!0,u[2]):"product"===u[2]||"productwithvariant"===u[2]?(null!==sessionStorage.getItem("highlightStr")?(o(sessionStorage.getItem("highlightStr").split(","),!1,"product",!0),console.log("Loding Higlights from session")):(o(["","","",""],!1,u[2],!0),console.log("Higlights not in session")),null!==sessionStorage.getItem("pageMetaData")?(o(JSON.parse(sessionStorage.getItem("pageMetaData")),!0,u[2]),console.log("Loding pageMetaData from session")):(o(["","","",""],!1,u[2]),console.log("pageMetaData not in session"))):null!==sessionStorage.getItem("pageMetaData")?(o(sessionStorage.getItem("pageMetaData").split(","),!1,u[2]),console.log("Loding Higlights from session")):(o(["","","",""],!1,u[2]),console.log("Higlights not in session")),document.querySelector(".submit-row input").addEventListener("mouseenter",function(e){!function(e){if("product"===u[2]||"productwithvariant"===u[2]){let t=null;const s=document.querySelectorAll(".container .gui_input");var l=s.length;const i=new Object;for(let e=0;e<l-1;e++)e%2==0&&(""!==s[e].value&&""!==s[e+1].value?i[s[e].value]=s[e+1].value:(""===s[e].value&&""===s[e+1].value?(s[e].style.border=borderStyle,s[e+1].style.border=borderStyle):""===s[e+1].value&&(s[e+1].style.border=borderStyle),t=!0));var n=document.querySelectorAll(".forhighlights-container .gui_input");let o="";for(let e=0;e<n.length;e++)""!==n[e].value&&(o=0===e?n[e].value:`${o},${n[e].value}`);d.value=o,g("highlightStr",o),t&&alert("Please delete empty boxes! then try again");var a=JSON.stringify(i);g("pageMetaData",c.value=a),console.log(a,o)}else if("product_type"===e){var o=document.querySelectorAll(".gui_input"),r=o.length;let t="";for(let e=0;e<r;e++)0===e?""!==o[e].value&&(t+=o[e].value):""!==o[e].value&&(t+=`,${o[e].value}`);c.value=t,g("pageMetaData",t),console.log(t)}}(u[2])}),"product"!==u[2]&&"productwithvariant"!==u[2]||django.jQuery("#id_Type").on("select2:select",function(e){e=e.params.data;console.log(e.id),fetch("/get_meta_data",{method:"POST",mode:"cors",cache:"no-cache",headers:{"Content-Type":"application/json","X-CSRFToken":t},body:JSON.stringify({for:"add",page:u[2],pk:e.id})}).then(e=>e.json()).then(e=>{o(e.list,!1,"product")}).catch(e=>console.error(e))}),document.querySelectorAll("select").forEach(e=>{e.classList.add("min-width-legit")}),document.querySelectorAll('input[type="text"]').forEach(e=>{"submit"!==e.type&&e.classList.add("min-width-legit")}),document.querySelectorAll('input[type="number"]').forEach(e=>{"submit"!==e.type&&e.classList.add("min-width-legit")});function g(e,t){try{sessionStorage.setItem(e,t)}catch(e){alert(`Error occured name:${e.name} & message:${e.message}`)}}document.querySelectorAll(".djn-drag-handler").forEach((e,t)=>{0===t?e.setAttribute("style","margin-top: 0rem;border-top: 4px solid steelblue;padding: 4px 2px;font-size: 1.2rem;color: steelblue;"):e.setAttribute("style","margin-top: 2rem;border-top: 2px solid steelblue;padding: 4px 2px;font-size: 1.2rem;color: steelblue;")}),setTimeout(()=>{},2e3)});