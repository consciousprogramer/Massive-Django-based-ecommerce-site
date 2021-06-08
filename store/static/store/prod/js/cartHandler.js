document.addEventListener("DOMContentLoaded",function(){const t=document.querySelector("[name=csrfmiddlewaretoken]").value;function a(){function e(){document.querySelectorAll(".cart_btn").forEach(t=>{t.innerHTML='<i class="fab fa-opencart fa-lg"></i> View Cart'}),document.querySelector("#heart-cart").classList.remove("hover:tw-text-red-500","hover:tw-border-yellow-400","tw-text-red-300","tw-border-gray-300"),document.querySelector("#heart-cart").classList.add("tw-text-red-500","tw-border-yellow-400")}if(userId||customerId)e();else{let t=window.location.pathname.split("/").filter(t=>""!=t);t.includes("normal")?(pid=t[2],cart.prodList.includes(pid)&&(e(),document.querySelector("#heart-cart").setAttribute("data-action","view_cart"))):t.includes("variable")&&(pid=t[2],vid=t[3],cart.varList.includes(vid)&&(e(),document.querySelector("#heart-cart").setAttribute("data-action","view_cart")))}}function e(){let e=document.querySelector("#heart-cart");"add"===e.getAttribute("data-action")?(itemDetails=new Object,currentPath.includes("normal")?(itemDetails.productId=currentPath[2],itemDetails.variantId=null,itemDetails.ptype="normal",itemDetails.quantity=1<=parseInt(document.getElementById("product_quantity_lg").value)?document.getElementById("product_quantity_lg").value:1,itemDetails.time=String((new Date).getTime()).slice(0,10)):currentPath.includes("variable")&&(itemDetails.productId=currentPath[2],itemDetails.variantId=currentPath[3],itemDetails.ptype="variable",itemDetails.quantity=1<=parseInt(document.getElementById("product_quantity_lg").value)?document.getElementById("product_quantity_lg").value:1,itemDetails.time=String((new Date).getTime()).slice(0,10)),console.log(itemDetails),userId&&customerId?(fetch("/additemtocart/",{method:"POST",mode:"cors",cache:"no-cache",headers:{"Content-Type":"application/json","X-CSRFToken":t},body:JSON.stringify(itemDetails)}).then(t=>{console.log(t),1==t.ok&&(e.setAttribute("data-action","view_cart"),document.getElementById("tr_cart_modal").click(),document.getElementById("prod_name").innerText=document.getElementById("product_name").innerText,a())}).catch(t=>{alert(t.message)}),console.log("Sending")):"normal"===currentPath[1]?!1===cart.prodList.includes(itemDetails.productId)?(cart.prodList.push(`${itemDetails.productId}`),cart.cartItems.push(itemDetails),localStorage.setItem("cart",JSON.stringify(cart)),console.log("Saved In LocalStorage"),e.setAttribute("data-action","view_cart"),document.getElementById("tr_cart_modal").click(),document.getElementById("prod_name").innerText=document.getElementById("product_name").innerText,a()):(console.log("Item already in cart!"),window.location.href=`${window.location.origin}/view/cart`):"variable"===currentPath[1]&&(!1===cart.varList.includes(itemDetails.variantId)?(cart.varList.push(`${itemDetails.variantId}`),cart.cartItems.push(itemDetails),localStorage.setItem("cart",JSON.stringify(cart)),console.log("Saved In LocalStorage"),e.setAttribute("data-action","view_cart"),document.getElementById("tr_cart_modal").click(),document.getElementById("prod_name").innerText=document.getElementById("product_name").innerText,a()):(console.log("Item already in cart!"),window.location.href=`${window.location.origin}/view/cart`))):userId&&customerId?(console.log("[authed]going to cart page"),window.location.href=`${window.location.origin}/view/cart`):function(t="set"){let e="",a="";if(cart.cartItems.forEach(t=>{null===t.variantId?a=0===a.length?`${t.productId}_${t.quantity}`:`${t.productId}_${t.quantity}-${a}`:e=0===e.length?`${t.variantId}_${t.quantity}`:`${t.variantId}_${t.quantity}-${e}`}),finalStr=0===e.length&&0===a.length?"":0===e.length&&0!==a.length?`?prodlist=${a}`:0!==e.length&&0===a.length?`?varlist=${e}`:`?varlist=${e}&prodlist=${a}`,console.log(finalStr),"set"!==t)return finalStr;window.location.href=`${window.origin}${cartPageUrl}${finalStr}`}()}userId||customerId||a(),document.querySelector("#heart-cart").addEventListener("click",t=>{e()}),document.querySelectorAll(".cart_btn").forEach(t=>{t.addEventListener("click",t=>{e()})})});