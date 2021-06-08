// CODE FOR ADD TO CART
document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    function updateUi() {
        function doUpdate() {
            document.querySelectorAll('.cart_btn').forEach(el => {
                    el.innerHTML = '<i class="fab fa-opencart fa-lg"></i> View Cart'
                })
                // 
            document.querySelector('#heart-cart').classList.remove('hover:tw-text-red-500', 'hover:tw-border-yellow-400', 'tw-text-red-300', 'tw-border-gray-300')

            // 
            document.querySelector('#heart-cart').classList.add('tw-text-red-500', 'tw-border-yellow-400')
        }
        debugger
        if (!userId && !customerId) {
            let currentPath = window.location.pathname.split('/').filter(el => el != "")
            if (currentPath.includes('normal')) {
                pid = currentPath[2]
                if (cart.prodList.includes(pid)) {
                    doUpdate()
                    document.querySelector('#heart-cart').setAttribute('data-action', 'view_cart')
                }
            } else if (currentPath.includes('variable')) {
                pid = currentPath[2]
                vid = currentPath[3]
                if (cart.varList.includes(vid)) {
                    doUpdate()
                    document.querySelector('#heart-cart').setAttribute('data-action', 'view_cart')
                }
            }
        } else {
            doUpdate()
        }
    }
    // Update UI on page load
    if (!userId && !customerId) {
        updateUi()
    }
    // document.querySelectorAll('.cart_btn').addEventListener('click',(e) => {

    // })

    function updateQueryPrams(get_or_set = 'set') {
        // generates new query params according
        // to the current cart Items
        let varQueryStr = ''
        let prodQueryStr = ''
        cart.cartItems.forEach((obj) => {
            if (obj.variantId === null) {
                if (prodQueryStr.length === 0) {
                    prodQueryStr = `${obj.productId}_${obj.quantity}`
                } else {
                    prodQueryStr = `${obj.productId}_${obj.quantity}-${prodQueryStr}`
                }
            } else {
                if (varQueryStr.length === 0) {
                    varQueryStr = `${obj.variantId}_${obj.quantity}`
                } else {
                    varQueryStr = `${obj.variantId}_${obj.quantity}-${varQueryStr}`
                }
            }
        })
        if (varQueryStr.length === 0 && prodQueryStr.length === 0) {
            finalStr = ''
        } else if (varQueryStr.length === 0 && prodQueryStr.length !== 0) {
            finalStr = `?prodlist=${prodQueryStr}`
        } else if (varQueryStr.length !== 0 && prodQueryStr.length === 0) {
            finalStr = `?varlist=${varQueryStr}`
        } else {
            finalStr = `?varlist=${varQueryStr}&prodlist=${prodQueryStr}`
        }
        console.log(finalStr);
        if (get_or_set === 'set') {
            window.location.href = `${window.origin}${cartPageUrl}${finalStr}`
        } else {
            return finalStr
        }
    }

    function addToCart(event) {
        let heartCart = document.querySelector('#heart-cart')
            // this logic is for adding to cart
        if (heartCart.getAttribute('data-action') === 'add') {
            itemDetails = new Object()
            if (currentPath.includes('normal')) {
                itemDetails.productId = currentPath[2]
                itemDetails.variantId = null
                itemDetails.ptype = 'normal'
                itemDetails.quantity = parseInt(document.getElementById('product_quantity_lg').value) >= 1 ? document.getElementById('product_quantity_lg').value : 1
                itemDetails.time = String(new Date().getTime()).slice(0, 10)
            } else if (currentPath.includes('variable')) {
                itemDetails.productId = currentPath[2]
                itemDetails.variantId = currentPath[3]
                itemDetails.ptype = 'variable'
                itemDetails.quantity = parseInt(document.getElementById('product_quantity_lg').value) >= 1 ? document.getElementById('product_quantity_lg').value : 1
                itemDetails.time = String(new Date().getTime()).slice(0, 10)
            }
            console.log(itemDetails);
            if (userId && customerId) {
                // id data-action = 'add' and Authed user
                // send data for saving on server
                fetch('/additemtocart/', {
                    method: "POST",
                    mode: 'cors',
                    cache: 'no-cache',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify(itemDetails)
                }).then(response => {
                    console.log(response);
                    if (response.ok == true) {
                        heartCart.setAttribute('data-action', 'view_cart')
                        document.getElementById('tr_cart_modal').click()
                        document.getElementById('prod_name').innerText = document.getElementById('product_name').innerText
                        updateUi()
                    }
                    // now server knows u added 
                    // this items to the cart so it has the  data, 
                    // so it will render page next time knowing that
                }).catch(error => {
                    alert(error.message)
                })
                console.log('Sending');
            } else {
                // if data-action = 'add' and Un-authed user
                debugger
                if (currentPath[1] === 'normal') {
                    // if on normal page and data-action = 'add' and Un-authed user
                    if (cart.prodList.includes(itemDetails.productId) === false) {
                        // cart.prodList.push(`${itemDetails.productId}_${itemDetails.quantity}`)
                        cart.prodList.push(`${itemDetails.productId}`)
                        cart.cartItems.push(itemDetails)
                        localStorage.setItem('cart', JSON.stringify(cart))
                        console.log('Saved In LocalStorage');
                        heartCart.setAttribute('data-action', 'view_cart')
                        document.getElementById('tr_cart_modal').click()
                        document.getElementById('prod_name').innerText = document.getElementById('product_name').innerText
                        updateUi()
                    } else {
                        // this can be use less code
                        console.log('Item already in cart!');
                        window.location.href = `${window.location.origin}/view/cart`
                    }

                } else if (currentPath[1] === 'variable') {
                    // if on variable page and data-action = 'add' and Un-authed user
                    if (cart.varList.includes(itemDetails.variantId) === false) {
                        // cart.varList.push(`${itemDetails.variantId}_${itemDetails.quantity}`)
                        cart.varList.push(`${itemDetails.variantId}`)
                        cart.cartItems.push(itemDetails)
                        localStorage.setItem('cart', JSON.stringify(cart))
                        console.log('Saved In LocalStorage');
                        heartCart.setAttribute('data-action', 'view_cart')
                        document.getElementById('tr_cart_modal').click()
                        document.getElementById('prod_name').innerText = document.getElementById('product_name').innerText
                        updateUi()
                    } else {
                        // this can be use less code
                        console.log('Item already in cart!');
                        window.location.href = `${window.location.origin}/view/cart`
                    }
                }
            }
        } else {
            // logic for viewing cart
            // if data-action === 'view-cart'
            if (userId && customerId) {
                console.log('[authed]going to cart page');
                window.location.href = `${window.location.origin}/view/cart`
            } else {
                updateQueryPrams()
            }
        }
    }
    document.querySelector('#heart-cart').addEventListener('click', (event) => {
        debugger
        addToCart(event)
    })

    document.querySelectorAll('.cart_btn').forEach(el => {
        el.addEventListener('click', (event) => {
            debugger
            addToCart(event)
        })
    })
})