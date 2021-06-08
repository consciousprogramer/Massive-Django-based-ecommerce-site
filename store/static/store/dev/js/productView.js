// Initialization of the Lightgallery
// lightGallery(document.getElementById('lightgallery'),{
//     loop:false,
//     download:false,
//     mode:'lg-slide',
//     thumbMargin:10,
//     thumbWidth:100,
//     thumbContHeight:100,
//     scale:1,
//     selector:'.lg_item'
// }); 


// Initialization of the splide slider
document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    var secondarySlider = new Splide('#secondary-slider', {
        width: '100%',
        fixedWidth: 100,
        fixedHeight: 100,
        gap: 6,
        // cover   :true,
        rewind: true,
        pagination: false,
        focus: 'center',
        isNavigation: true,
        updateOnMove: true,
        trimSpace: true,
    })
    secondarySlider.mount()

    var primarySlider = new Splide('#primary-slider', {
        width: '100%',
        heightRatio: 1,
        type: 'fade',
        speed: 100,
        pagination: false,
        arrows: false,
        // cover      : true,
    });
    primarySlider.sync(secondarySlider).mount()


    // POST Load ZOOM---------------
    const lgItems = document.querySelectorAll('.lg_item')
        // for (let i = 0; i < lgItems.length; i++) {
        //     const element = lgItems[i];
        //     element.addEventListener('mouseenter',function(event){
        //         console.log(event.target.getAttribute('data-fetched'));
        //         if(event.target.getAttribute('data-fetched') == 'false'){
        //             event.target.setAttribute('data-fetched','true')
        //             $(`#${element.id}`).zoom({url:element.getAttribute('data-zoom-image'),magnify:1})
        //             console.log('added');
        //         }
        //     })
        // }

    // PRE Load ZOOM-------------------------
    for (let i = 0; i < lgItems.length; i++) {
        const element = lgItems[i];
        $(`#${element.id}`).zoom({ url: element.getAttribute('data-zoom-image'), magnify: 0.8 })
    }
    // PRE Load ZOOM-------------------------


    // make all attribute of equal length--------------------------
    let attrMaxwidth = null
    document.querySelectorAll('.current-attribute').forEach((el, index) => {
        console.log(el.clientWidth);
        if (index === 0) {
            attrMaxwidth = el.clientWidth
        } else if (el.clientWidth > attrMaxwidth) {
            attrMaxwidth = el.clientWidth
        }
    })
    console.log('[ MAX ]', attrMaxwidth);
    document.querySelectorAll('.attribute-names').forEach((el) => {
            el.style.minWidth = `${attrMaxwidth + 8}px`
        })
        // make all attribute of equal length-------------------------



    // Starts Variant selection procedure
    currentPath = window.location.pathname.split('/').filter(el => el != "")
    if (currentPath.includes('variable')) {
        if (!Object.entries) {
            Object.entries = function(obj) {
                var ownProps = Object.keys(obj),
                    i = ownProps.length,
                    resArray = new Array(i); // preallocate the Array
                while (i--)
                    resArray[i] = [ownProps[i], obj[ownProps[i]]];

                return resArray;
            };
        }
        const selectedAttrs = new Object()
        const attributeContainer = document.querySelector('.attribute-container')
        attributeContainer.querySelectorAll('.attribute-row').forEach((el, index) => {
            selectedAttrs[`${el.getElementsByTagName('p')[0].innerText}`] = el.querySelector('.current-attribute').innerText
        })
        console.log('[selected]', selectedAttrs);
        const url = new URL(`${window.location.origin}${window.location.pathname}`) || Window.URL(`${window.location.origin}${window.location.pathname}`)
        attributeContainer.querySelectorAll('.attribute-row').forEach(el => {
            const rowAttr = el.querySelector('p').innerText
                // const allUnselectedAnchor = el.querySelectorAll('.attribute')
            el.querySelectorAll('.attribute').forEach(el => {
                let cpyUrl = url
                for (const [attr, rowVal] of Object.entries(selectedAttrs)) {
                    if (attr !== rowAttr) {
                        // console.log('[not case]',attr,rowVal);
                        cpyUrl.searchParams.set(attr, rowVal)
                    } else if (attr === rowAttr) {
                        // console.log('[match case]',attr,rowVal);
                        cpyUrl.searchParams.set(attr, el.innerText)
                    }
                }
                el.setAttribute('href', `${window.location.origin}${window.location.pathname}?query=getit&${cpyUrl.searchParams.toString()}`)
                console.log(`${window.location.origin}${window.location.pathname}?query=getit&${cpyUrl.searchParams.toString()}`)
            })
        })
    }


    // cart quantity handler
    if (window.getComputedStyle(document.getElementById('cart_row_lg')).display !== 'none') {
        const increase_btn = document.querySelector('#increase_quantity_lg')
        const decrease_btn = document.querySelector('#decrease_quantity_lg')
        console.log('Running lg');
        const product_quantity = document.querySelectorAll('.product_quantity')
        increase_btn.addEventListener('click', function() {
            product_quantity.forEach(el => {
                el.value = parseInt(el.value) + 1
            })
        })
        decrease_btn.addEventListener('click', function() {
            product_quantity.forEach(el => {
                el.value = parseInt(el.value) - 1
            })
        })
    } else if (window.getComputedStyle(document.getElementById('cart_row_md')).display !== 'none') {
        const increase_btn = document.querySelector('#increase_quantity_md')
        const decrease_btn = document.querySelector('#decrease_quantity_md')
        console.log('Running md');
        const product_quantity = document.querySelectorAll('.product_quantity')
        increase_btn.addEventListener('click', function() {
            product_quantity.forEach(el => {
                el.value = parseInt(el.value) + 1
            })
        })
        decrease_btn.addEventListener('click', function() {
            product_quantity.forEach(el => {
                el.value = parseInt(el.value) - 1
            })
        })
    } else {
        const increase_btn = document.querySelector('#increase_quantity')
        const decrease_btn = document.querySelector('#decrease_quantity')
        const items_quanity_input = document.querySelector('#product_quantity')
        console.log('Running mormal');
        const product_quantity = document.querySelectorAll('.product_quantity')
        increase_btn.addEventListener('click', function() {
            product_quantity.forEach(el => {
                el.value = parseInt(el.value) + 1
            }, { passive: true })
        })
        decrease_btn.addEventListener('click', function() {
            product_quantity.forEach(el => {
                el.value = parseInt(el.value) - 1
            }, { passive: true })
        })
    }

    // html injection
    containerHeight = document.querySelector('#product-container').getClientRects()[0].height
    let bodyObj = null
    if (currentPath.includes('normal')) {
        bodyObj = {
            'id': currentPath[1],
            'ptype': 'normal',
            'for': 'viewed'
        }
    } else {
        bodyObj = {
            'id': currentPath[2],
            'ptype': 'variable',
            'for': 'viewed'
        }
    }


    function createSlider(id) {
        const idStr = `#${id}`
        const sectionSlider = new Splide(idStr, {
            type: 'slide',
            pagination: false,
            autoplay: false,
            width: '100%',
            fixedWidth: '240px',
            gap: 10,
            breakpoints: {
                1024: {
                    focus: 'center'
                }
            }
        })
        sectionSlider.mount()
    }


    function recommendRequest() {
        document.querySelector('#recommend-box').innerHTML = `<h1 class="tw-mb-14 tw-py-4 tw-text-center tw-font-mono tw-text-2xl tw-font-normal tw-text-green-500">Fetching Items....</h1>`
        fetch(window.location.pathname, {
                method: "POST",
                mode: 'cors',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'for': 'recommend' })
            }).then(response => response.text())
            .then(html => {
                document.querySelector('#recommend-box').innerHTML = html
                createSlider('recommend_slider_4141')
            }).catch(error => alert(error.message))
    }

    let requested = false
    document.addEventListener('scroll', function() {
        console.log('scroll');
        if (innerHeight + scrollY > containerHeight - 10) {
            if (requested !== true) {
                requested = true
                document.querySelector('#inject-box').innerHTML = `<h1 class="tw-mb-14 tw-py-4 tw-text-center tw-font-mono tw-text-2xl tw-font-normal tw-text-green-500"><div class="preloader-wrapper big active"> <div class="spinner-layer spinner-blue-only"> <div class="circle-clipper left"> <div class="circle"></div> </div> <div class="gap-patch"> <div class="circle"></div> </div> <div class="circle-clipper right"> <div class="circle"></div> </div> </div> </div></h1>`
                fetch(window.location.pathname, {
                        method: "POST",
                        mode: 'cors',
                        cache: 'no-cache',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify(bodyObj)
                    }).then(response => response.text())
                    .then(html => {
                        document.querySelector('#inject-box').innerHTML = html
                        recommendRequest()
                        createSlider('section_slider_4141')
                    })
                    .catch(error => console.error(error))
            }
        }
    }, { passive: true })


});