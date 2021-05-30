// let sectionSlider = new Splide('#section_slider_1',{
//     type:'slide',
//     pagination:false,
//     autoplay:false,
//     width:'100%',
//     fixedWidth:'240px',
//     gap:10,
//     breakpoints:{
//         1024:{
//             focus:'center'
//         }
//     }
// })

// sectionSlider.mount()

const allSplide = document.querySelectorAll('.splide')

for (let i = 0; i < allSplide.length; i++) {
    const element = allSplide[i];
    const sectionSlider = new Splide(`#${element.id}`,{
        type:'slide',
        pagination:false,
        autoplay:false,
        width:'100%',
        fixedWidth:'240px',
        gap:10,
        breakpoints:{
            1024:{
                focus:'center'
            }
        }
    })
    sectionSlider.mount()
}

const brandSlider = new Splide('#brand_slider',{
    type:'slide',
    pagination:false,
    autoplay:false,
    width:'100%',
    fixedWidth:'176px',
    gap:10,
    breakpoints:{
        1024:{
            focus:'center'
        }
    }
}).mount()