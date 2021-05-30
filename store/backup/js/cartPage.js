const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
let quantChangeTimer = null
let changeQuantity = null

function updateLSItems(id, ptype, changeType) {
    debugger
    cart.cartItems = cart.cartItems.map(item => {
        const newItem = {...item }
        if (changeType === 'plus') {
            ptype === 'normal' ? (item.ptype === ptype && item.productId === id) ? newItem.quantity = +newItem.quantity + +changeQuantity : console.log('no update') : (item.ptype === ptype && item.variantId === id) ? newItem.quantity = +newItem.quantity + +changeQuantity : console.log('no update')
        } else {
            ptype === 'normal' ? (item.ptype === ptype && item.productId === id) ? newItem.quantity = +newItem.quantity - +changeQuantity : console.log('no update') : (item.ptype === ptype && item.variantId === id) ? newItem.quantity = +newItem.quantity - +changeQuantity : console.log('no update')
        }
        return newItem
    })
    changeQuantity = null
}

function handleQuantChange(id, ptype, changeType) {
    if (!userId && !customerId) {
        updateLSItems(id, ptype, changeType)
        localStorage.setItem('cart', JSON.stringify(cart))
        changeQuantity = null
        window.location.search = genQueryStr()
    } else {
        debugger
        fetch('/view/cart/', {
                method: 'UPDATE',
                mode: "same-origin",
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'ptype': ptype, 'itemId': id, 'change': changeQuantity, 'changeType': changeType })
            }).then(response => {
                if (response.ok) {
                    changeQuantity = null
                    window.location.reload()
                } else {
                    alert('Quantity not changed')
                }
            })
            .catch(error => console.error(error))
    }
}


document.querySelectorAll('.quant-btn').forEach((el) => {
    el.addEventListener('click', (event) => {
        const forInput = document.getElementById(event.target.getAttribute('data-for'))
        const itemId = forInput.getAttribute('data-id')
        const ptype = forInput.getAttribute('data-cardtype')
        console.log(event.target.getAttribute('data-for'));
        if (event.target.getAttribute('data-action') === 'plus') {
            forInput.value = +forInput.value + 1
            changeQuantity++
            // clear timeout
            // debugger
            quantChangeTimer !== null ? clearTimeout(quantChangeTimer) : null
                // set New timeout
            quantChangeTimer = setTimeout(() => {
                handleQuantChange(itemId, ptype, 'plus')
            }, 1000);
        } else {
            if (+forInput.value > 1) {
                forInput.value = +forInput.value - 1
                changeQuantity++
                // clear timeout
                // debugger
                quantChangeTimer !== null ? clearTimeout(quantChangeTimer) : null
                    // set New timeout
                quantChangeTimer = setTimeout(() => {
                    handleQuantChange(itemId, ptype, 'minus')
                }, 800);
            }
        }

    })
})

function genQueryStr() {
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
        return ''
    } else if (varQueryStr.length === 0 && prodQueryStr.length !== 0) {
        return `?prodlist=${prodQueryStr}`
    } else if (varQueryStr.length !== 0 && prodQueryStr.length === 0) {
        return `?varlist=${varQueryStr}`
    } else {
        return `?varlist=${varQueryStr}&prodlist=${prodQueryStr}`
    }
}


function removeCartItem(id, authStatus, ptype) {
    if (authStatus === true) {
        window.location.reload()
    } else {
        let removeIndex = null
        let toBreak = false
        if (ptype === 'normal') {
            cart.cartItems.forEach((item, cindex) => {
                if (toBreak === false) {
                    if (item.productId === id && item.ptype === 'normal') {
                        console.log(`removing card-${id} type=normal`);
                        toRun = true
                        document.querySelectorAll("[data-cardtype='normal']").forEach((el) => {
                            if (toRun === true) {
                                if (el.getAttribute('data-id') === id) {
                                    toBreak = true
                                    toRun = false
                                    el.remove()
                                }
                            }
                        })
                    }
                    if (toBreak === true) {
                        if (removeIndex === null) {
                            removeIndex = cindex
                        }
                    }
                } else {
                    return
                }
            })
        } else {
            cart.cartItems.forEach((item, cindex) => {
                if (toBreak === false) {
                    if (item.variantId === id && item.ptype === 'variable') {
                        console.log(`removing card-${id} type=variable`);
                        document.querySelectorAll("[data-cardtype='variable']").forEach((el) => {
                            if (el.getAttribute('data-id') === id) {
                                toBreak = true
                                el.remove()
                            }
                        })
                    }
                    if (toBreak === true) {
                        if (removeIndex === null) {
                            removeIndex = cindex
                        }
                    }
                } else {
                    return
                }
            })
        }
        debugger
        cart.cartItems.splice(removeIndex, 1)
        if (ptype === 'variable') {
            cart.varList = cart.varList.filter(el => el !== id)
        } else {
            cart.prodList = cart.prodList.filter(el => el !== id)
        }
        localStorage.setItem('cart', JSON.stringify(cart))
        window.location.search = genQueryStr()
    }
}

document.querySelectorAll('.remove-btn').forEach((el) => {
    el.addEventListener('click', (event) => {
        const itemId = event.target.getAttribute('data-item-id')
        const ptype = event.target.getAttribute('data-ptype')
        let confirmed = confirm('Are you sure you want to remove this item!')
        if (confirmed === true) {
            if (userId && customerId) {
                fetch('/view/cart/', {
                        method: "POST",
                        mode: "same-origin",
                        cache: 'no-cache',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({ 'ptype': ptype, 'itemId': itemId })
                    }).then(response => {
                        if (response.ok) {
                            debugger
                            removeCartItem(itemId, authStatus = true, ptype)
                        } else {
                            alert('Item Not Removed')
                        }
                    })
                    .catch(error => console.error(error))
            } else {
                removeCartItem(itemId, authStatus = false, ptype)
            }
        } else {
            setTimeout(() => {
                alert('Item Not Removed!')
            }, 300);
        }
    })
})