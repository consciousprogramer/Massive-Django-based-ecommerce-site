document.addEventListener('DOMContentLoaded',function(){
    const url = '/get_meta_data'
    let counter = 0
    const path_array = window.location.pathname.split("/").filter(el => el != "")
    if (path_array.includes('change') || path_array.includes('add')) {
        console.log('Nothing To Clear');
    }else{
        console.log('Clearing session');
        sessionStorage.clear()
    }
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const pageMetaDataField = document.querySelector('#id_Meta_data')
    pageMetaDataField.style.display = 'none'
    let highlightInput = null
    if(path_array[2] === 'product' || path_array[2] === 'productwithvariant'){
        highlightInput = document.querySelector('#id_Highlights')
        highlightInput.style.display = 'none'
    }

    // Dispatch initial request to check if ADD or CHANGE
    if(path_array.includes("change")){
        debugger
        if (path_array[2] === 'product' || path_array[2] === 'productwithvariant') {
            if (sessionStorage.getItem('highlightStr') !== null) {
                injectGUI(sessionStorage.getItem('highlightStr').split(','),false,'product',true)
                console.log('Loding Higlights from session');
            }else{
                const allHighlights = highlightInput.value.split(',')
                injectGUI(allHighlights,false,'product',true)
                console.log('Higlights not in session');
            }

            if (sessionStorage.getItem('pageMetaData') !== null) {
                injectGUI(JSON.parse(sessionStorage.getItem('pageMetaData')),true,path_array[2])
                console.log('Loding pageMetaData from session');
            }else{
                injectGUI(JSON.parse(pageMetaDataField.value),true,path_array[2])
                console.log('pageMetaData not in session');
            }
            // code before sessionStorage
            // injectGUI(JSON.parse(pageMetaDataField.value),true,path_array[2])
            // const allHighlights = highlightInput.value.split(',')
            // injectGUI(allHighlights,false,'product',true)
        } else if(path_array[2] === 'product_type') {
            // if (sessionStorage.getItem('highlightStr') !== null) {
            //     injectGUI(sessionStorage.getItem('highlightStr').split(','),true,path_array[2])
            //     console.log('Loding Higlights from session');
            // }else{
            //     injectGUI(allHighlights,true,path_array[2])
            //     console.log('Higlights not in session');
            // }
            injectGUI(pageMetaDataField.value.split(','),true,path_array[2])
        }
    }else{
        // if on ADD Page Then
        // path_array[3] = on which page!
        // debugger
        if (path_array[2] === 'product' || path_array[2] === 'productwithvariant') {
            if (sessionStorage.getItem('highlightStr') !== null) {
                injectGUI(sessionStorage.getItem('highlightStr').split(','),false,'product',true)
                console.log('Loding Higlights from session');
            }else{
                injectGUI(['','','',''],false,path_array[2],true)
                console.log('Higlights not in session');
            }
            if (sessionStorage.getItem('pageMetaData') !== null) {
                injectGUI(JSON.parse(sessionStorage.getItem('pageMetaData')),true,path_array[2])
                console.log('Loding pageMetaData from session');
            }else{
                injectGUI(['','','',''],false,path_array[2])
                console.log('pageMetaData not in session');
            }
            // code before sessionStorage
            // injectGUI(['','',''],false,path_array[2])
            // injectGUI(['','','',''],false,path_array[2],true)
        } else {
            if (sessionStorage.getItem('pageMetaData') !== null) {
                injectGUI(sessionStorage.getItem('pageMetaData').split(','),false,path_array[2])
                console.log('Loding Higlights from session');
            }else{
                injectGUI(['','','',''],false,path_array[2])
                console.log('Higlights not in session');
            }
            // code before sessionStorage
            // injectGUI(['','','',''],false,path_array[2])
        }
    }

    function injectGUI(recivedData,initial,page,forHighlights=null){
        let container = document.createElement('div')
        if (!forHighlights) {
            try {
                document.querySelector('.container').remove()
                } catch (e) {
                console.log('No item to remove')
                }
            container.setAttribute('class','container')
        }else{
            container.setAttribute('class','forhighlights-container')
        }
        if (path_array[2] === 'product' || path_array[2] === 'productwithvariant') {
            if (initial === true) {
              //recivedData is an object
              for (let question in recivedData) {
                  let row = setRow(question,recivedData[question],page)
                  container.append(row)
                }
                // let data_keys = Object.keys(recivedData)
                // data_keys.forEach(question => {
                //     let row = setRow(data_keys,recivedData[data_keys],page)
                //     container.append(row)
                // })
            }else if(initial === false) {
              // recivedData is a list
            //   forHighlights will always be exceuted in the initial === false block
              if (forHighlights === true) {
                recivedData.forEach(question => {
                    let row = setRow(question,null,page,forHighlights)
                    container.append(row)
                })
              } else {
                recivedData.forEach(question => {
                    let row = setRow(question,null,page)
                    container.append(row)
                })
              }
            }
        }else if(page === 'product_type'){
            //this recicedData will always be a  list
            recivedData.forEach(question => {
                container.append(setRow(question,null,page))
          })
        }

        let btn = document.createElement('button')
        btn.setAttribute('class','btn')
        btn.innerText = '+ ADD'
        container.append(btn)
        btn.addEventListener('click',function (event) {
            event.preventDefault()
            if (forHighlights) {
                event.currentTarget.before(setRow(null,null,page,true))
            } else {
                event.currentTarget.before(setRow(null,null,page))
            }
        })
        if (forHighlights) {
            highlightInput.before(container)            
        } else {
            pageMetaDataField.before(container)
        }
    }
 
    // set's Row accordingly
    function setRow(question=null,answer=null,page,forHighlights=null) {
        // debugger
        let row = document.createElement('div')
        row.setAttribute('class','row')
        row.setAttribute('id',`row-${counter}`)
        let cross = document.createElement('button')
        cross.setAttribute('class','cancel_btn')
        cross.setAttribute('id',`${counter}`)
        cross.innerText = 'X'
        counter++
        cross.addEventListener('click',function (event) {
            event.preventDefault()
            document.getElementById(`row-${event.currentTarget.id}`).remove()
        })
        let question_input = document.createElement('input')
        question_input.setAttribute('class','input gui_input')
        if (path_array[2] === 'product' || path_array[2] === 'productwithvariant') {
            if (forHighlights) {
                if (question !== null) {
                    question_input.setAttribute('value',question)
                }
                row.append(question_input,cross)
            } else {
                let answer_input = question_input.cloneNode()
                if (answer !== null) {
                    answer_input.setAttribute('value',answer)   
                }
                if (question !== null) {
                    question_input.setAttribute('value',question)
                }
                row.append(question_input,answer_input,cross)
            }
        }else if(page === 'product_type'){
            if (question !== null) {
                question_input.setAttribute('value',question)
            }
            row.append(question_input,cross)
        }
        return row
    }

    function saveData(page) {
        if(path_array[2] === 'product' || path_array[2] === 'productwithvariant'){
            let ifAnyError = null
            const allInputs = document.querySelectorAll('.container .gui_input')
            const allInputsLength = allInputs.length
            const finalData = new Object()
            for(let i = 0;i < allInputsLength - 1;i++){
                if(i%2 === 0){
                    if(allInputs[i].value !== "" && allInputs[i + 1].value !== ""){
                        finalData[allInputs[i].value] = allInputs[i + 1].value
                    }else{
                        if(allInputs[i].value === "" && allInputs[i + 1].value === ""){
                            allInputs[i].style.border = borderStyle
                            allInputs[i + 1].style.border = borderStyle
                        }else if(allInputs[i + 1].value === ""){
                            allInputs[i + 1].style.border = borderStyle
                        }
                        ifAnyError = true
                    }
                }
            }
            const allHighlightInput = document.querySelectorAll('.forhighlights-container .gui_input')
            let highlightStr = ''
            for (let i = 0; i < allHighlightInput.length; i++) {
                if(allHighlightInput[i].value !== ''){
                    if (i === 0) {
                        highlightStr = allHighlightInput[i].value
                    } else {
                        highlightStr = `${highlightStr},${allHighlightInput[i].value}`
                    }
                }
            }
            highlightInput.value = highlightStr
            saveToSession('highlightStr',highlightStr)
            if(ifAnyError){
                alert('Please delete empty boxes! then try again')
            }
            const finalJSON = JSON.stringify(finalData)
            pageMetaDataField.value = finalJSON
            saveToSession('pageMetaData',finalJSON)
            console.log(finalJSON,highlightStr);
        }else if(page === 'product_type'){
            let allInputs = document.querySelectorAll('.gui_input')
            let allInputsLength = allInputs.length
            let finalData = ''
            for (let i = 0;i < allInputsLength;i++) {
                if(i === 0){
                    if(allInputs[i].value !== ""){
                        finalData = finalData + allInputs[i].value
                    }
                }else{
                    if(allInputs[i].value !== ""){
                        finalData = finalData + `,${allInputs[i].value}`
                    }
                }
            }
            pageMetaDataField.value = finalData
            saveToSession('pageMetaData',finalData)
            console.log(finalData);
        }
    }

    document.querySelector('.submit-row input').addEventListener('mouseenter',function name(event) {
        // event.preventDefault()
        saveData(path_array[2])
    })

    if(path_array[2] === 'product' || path_array[2] === 'productwithvariant'){
        django.jQuery('#id_Type').on('select2:select', function (event) {
            var data = event.params.data;
            console.log(data.id);
            fetch(url,{
                method:"POST",
                mode:'cors',
                cache:'no-cache',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body:JSON.stringify({'for':'add','page':path_array[2],'pk':data.id})
            }).then(response => response.json())
              .then(data => {
                //   console.log('[Data]',data['list']);
                  injectGUI(data['list'],false,'product')
              })
              .catch(error => console.error(error))
            
        });
        // document.querySelector('#id_Type').addEventListener('change',function (event) {
        //     fetch(url,{
        //         method:"POST",
        //         mode:'cors',
        //         cache:'no-cache',
        //         headers:{
        //             'Content-Type':'application/json',
        //             'X-CSRFToken':csrftoken,
        //         },
        //         body:JSON.stringify({'for':'add','page':path_array[2],'pk':event.currentTarget.value})
        //     }).then(response => response.json())
        //       .then(data => {
        //           console.log('[Data]',data['list']);
        //           injectGUI(data['list'],false,'product')
        //       })
        //       .catch(error => console.error(error))
        // })

        
    }
    
    document.querySelectorAll('select').forEach(el => {
        el.classList.add('min-width-legit')
    })
    document.querySelectorAll('input[type="text"]').forEach(el => {
        if (el.type !== 'submit') {
            el.classList.add('min-width-legit')
        }
    })
    document.querySelectorAll('input[type="number"]').forEach(el => {
        if (el.type !== 'submit') {
            el.classList.add('min-width-legit')
        }
    })
    let a = 'margin-top: 0rem;border-top: 4px solid steelblue;padding: 4px 2px;font-size: 1.2rem;color: steelblue;'
    let b = 'margin-top: 2rem;border-top: 2px solid steelblue;padding: 4px 2px;font-size: 1.2rem;color: steelblue;'
    document.querySelectorAll('.djn-drag-handler').forEach((el,index) => {
        if (index === 0) {
            el.setAttribute('style',a)
        } else {
            el.setAttribute('style',b)
        }
    })


    function saveToSession(key,data){
        try {
            sessionStorage.setItem(key,data) 
        } catch (error) {
            alert(`Error occured name:${error.name} & message:${error.message}`)
        }
    }

    function checkDetails(borderStyle='1px solid red') {
        console.log('CHECKING');
        debugger
        const borderValid = '2px solid #00ff00'
        document.querySelectorAll('input').forEach(el => {
            if(el.type !== 'hidden' && el.type !== 'submit'){
                if(el.value === "" ||el.value === null){
                    el.style.border = borderStyle
                }else{
                    el.style.border = borderValid
                }
            }
        })
        document.querySelectorAll('select').forEach(el => {
            if(el.type !== 'hidden'){
                console.log('[select] ',el.id);
                if (!el.id.includes('from')) {
                    if(el.value === "" ||el.value === null){
                        el.style.border = borderStyle
                    }else{
                        el.style.border = borderValid
                    }
                }
            }
        })
        document.querySelectorAll('p.selector-filter input').forEach(el => {
            el.style.border = '1px solid grey'
        })
        document.querySelectorAll('span.select2-selection__rendered').forEach(el => {
            if (el.innerText === "") {
                console.log(el.innerText)
                el.style.border = borderStyle
            }else{
                el.style.border = borderValid
            }
        })
        document.querySelectorAll('textarea').forEach(el => {
            if(el.type !== 'hidden'){
                if(el.value === "" ||el.value === null){
                    el.style.border = borderStyle
                }else{
                    el.style.border = borderValid
                }
            }
        })
    }
    setTimeout(() => {
        // checkDetails()
    }, 2000);
    // checkDetails()
    // LOAD EVENT END
  })


