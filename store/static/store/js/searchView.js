document.querySelector('#mainSearchBar_pc_btn').addEventListener('click', function(event) {
    event.preventDefault()
    console.log('clicked');
    if (document.querySelector('#mainSearchBar_pc').value !== '') {
        document.querySelector('#mainSearchBar_pc').submit()
    }
})

document.querySelector('#mainSearchBar_mob_btn').addEventListener('click', function() {
    console.log('clicked');
    if (document.querySelector('#mainSearchBar_mob').value !== ' ' || document.querySelector('#mainSearchBar_mob').value !== '') {
        document.querySelector('#mainSearchBar_mob').submit()
    }
})


// ------------------------------------

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

function addToCart(event) {
    let heartCart = event.target
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


document.querySelectorAll('.cart_btn').forEach(el => {
    el.addEventListener('click', (event) => {
        debugger
        addToCart(event)
    })
})