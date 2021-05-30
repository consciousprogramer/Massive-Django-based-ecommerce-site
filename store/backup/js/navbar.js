document.querySelector('#mainSearchBar_pc_btn').addEventListener('click',function (){
    console.log('clicked');
    if(document.querySelector('#mainSearchBar_pc input').value.length >= 3){
        document.querySelector('#mainSearchBar_pc').submit()
    }
})

document.querySelector('#mainSearchBar_mob_btn').addEventListener('click',function (){
    console.log('clicked');
    if(document.querySelector('#mainSearchBar_mob input').value.length >= 3){
        document.querySelector('#mainSearchBar_mob').submit()
    }
})