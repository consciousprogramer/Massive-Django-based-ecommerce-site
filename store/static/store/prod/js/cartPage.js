const csrftoken=document.querySelector("[name=csrfmiddlewaretoken]").value;let quantChangeTimer=null,changeQuantity=null;function updateLSItems(a,n,r){cart.cartItems=cart.cartItems.map(t=>{const e={...t};return"plus"===r?"normal"===n?t.ptype===n&&t.productId===a?e.quantity=+e.quantity+ +changeQuantity:console.log("no update"):t.ptype===n&&t.variantId===a?e.quantity=+e.quantity+ +changeQuantity:console.log("no update"):"normal"===n?t.ptype===n&&t.productId===a?e.quantity=+e.quantity-+changeQuantity:console.log("no update"):t.ptype===n&&t.variantId===a?e.quantity=+e.quantity-+changeQuantity:console.log("no update"),e}),changeQuantity=null}function handleQuantChange(t,e,a){userId||customerId?fetch("/view/cart/",{method:"UPDATE",mode:"same-origin",cache:"no-cache",headers:{"Content-Type":"application/json","X-CSRFToken":csrftoken},body:JSON.stringify({ptype:e,itemId:t,change:changeQuantity,changeType:a})}).then(t=>{t.ok?(changeQuantity=null,window.location.reload()):alert("Quantity not changed")}).catch(t=>console.error(t)):(updateLSItems(t,e,a),localStorage.setItem("cart",JSON.stringify(cart)),changeQuantity=null,window.location.search=genQueryStr())}function genQueryStr(){let e="",a="";return cart.cartItems.forEach(t=>{null===t.variantId?a=0===a.length?`${t.productId}_${t.quantity}`:`${t.productId}_${t.quantity}-${a}`:e=0===e.length?`${t.variantId}_${t.quantity}`:`${t.variantId}_${t.quantity}-${e}`}),0===e.length&&0===a.length?"":0===e.length&&0!==a.length?`?prodlist=${a}`:0!==e.length&&0===a.length?`?varlist=${e}`:`?varlist=${e}&prodlist=${a}`}function removeCartItem(r,t,e){if(!0===t)window.location.reload();else{let a=null,n=!1;"normal"===e?cart.cartItems.forEach((t,e)=>{!1===n&&(t.productId===r&&"normal"===t.ptype&&(console.log(`removing card-${r} type=normal`),toRun=!0,document.querySelectorAll("[data-cardtype='normal']").forEach(t=>{!0===toRun&&t.getAttribute("data-id")===r&&(n=!0,toRun=!1,t.remove())})),!0===n&&null===a&&(a=e))}):cart.cartItems.forEach((t,e)=>{!1===n&&(t.variantId===r&&"variable"===t.ptype&&(console.log(`removing card-${r} type=variable`),document.querySelectorAll("[data-cardtype='variable']").forEach(t=>{t.getAttribute("data-id")===r&&(n=!0,t.remove())})),!0===n&&null===a&&(a=e))}),cart.cartItems.splice(a,1),"variable"===e?cart.varList=cart.varList.filter(t=>t!==r):cart.prodList=cart.prodList.filter(t=>t!==r),localStorage.setItem("cart",JSON.stringify(cart)),window.location.search=genQueryStr()}}document.querySelectorAll(".quant-btn").forEach(t=>{t.addEventListener("click",t=>{const e=document.getElementById(t.target.getAttribute("data-for")),a=e.getAttribute("data-id"),n=e.getAttribute("data-cardtype");console.log(t.target.getAttribute("data-for")),"plus"===t.target.getAttribute("data-action")?(e.value=+e.value+1,changeQuantity++,null!==quantChangeTimer&&clearTimeout(quantChangeTimer),quantChangeTimer=setTimeout(()=>{handleQuantChange(a,n,"plus")},1e3)):1<+e.value&&(e.value=+e.value-1,changeQuantity++,null!==quantChangeTimer&&clearTimeout(quantChangeTimer),quantChangeTimer=setTimeout(()=>{handleQuantChange(a,n,"minus")},800))})}),document.querySelectorAll(".remove-btn").forEach(t=>{t.addEventListener("click",t=>{const e=t.target.getAttribute("data-item-id"),a=t.target.getAttribute("data-ptype");!0===confirm("Are you sure you want to remove this item!")?userId&&customerId?fetch("/view/cart/",{method:"POST",mode:"same-origin",cache:"no-cache",headers:{"Content-Type":"application/json","X-CSRFToken":csrftoken},body:JSON.stringify({ptype:a,itemId:e})}).then(t=>{t.ok?removeCartItem(e,authStatus=!0,a):alert("Item Not Removed")}).catch(t=>console.error(t)):removeCartItem(e,authStatus=!1,a):setTimeout(()=>{alert("Item Not Removed!")},300)})});