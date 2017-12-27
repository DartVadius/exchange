const ENDPOINT = '/data';
const $d       = nbInit()

var   editedTR  = null;
var   $editData = null;

function jsonPost(url, data)
{
    return new Promise((resolve, reject) => {
        var x = new XMLHttpRequest();   
        x.onerror = () => reject(new Error('jsonPost failed'))
        //x.setRequestHeader('Content-Type', 'application/json');
        x.open("POST", url, true);
        x.send(JSON.stringify(data))

        x.onreadystatechange = () => {
            if (x.readyState == XMLHttpRequest.DONE && x.status == 200){
                resolve(JSON.parse(x.responseText))
            }
            else if (x.status != 200){
                reject(new Error('status is not 200'))
            }
        }
    })
}

jsonPost("/data", {a: 'b'})
    .then(data => console.log(data), error => console.log(error))

function c(func, data){ //rpc call
    return jsonPost(ENDPOINT,{func, data})
}

function getContent() {
    c('GetContentList', {}).then(data => {
        //$d.contentHead = data[0] && Object.keys(data[0])
        //$d.content     = data.map(rec => Object.values(rec).map(field => typeof field == 'object' ? JSON.stringify(field) : field))
        $d.content     = data.map(rec => {rec.data = JSON.stringify(rec.data); return rec;})
        $d.del = {onclick: function(evt){
            if (confirm('Delete?')){
                let td  = this.parentElement
                let row = td.parentElement.rowIndex -1
                c('DeleteContent',data[row].id).then(getContent, error => console.log(error))
            }
        }}

        $d.edit = {onclick: function(evt){
                if (editedTR){
                    let row = editedTR.rowIndex -1
                    data[row].template = editedTR.children[1].children[0].value
                    data[row].url      = editedTR.children[2].children[0].value
                    let d = {};
                    for (let i=0;i<$editData.editData.length;i++){
                        d[$editData.editData[i].key] =  JSON.parse('"' + $editData.editData[i].value + '"')
                    }
                    data[row].data     = d
                    c('UpdateContent', data[row]).then(getContent, error => console.log(error))
                    editedTR  = null;
                    $editData = null;
                }
                else {
                    editedTR = this.parentElement.parentElement;
                    let row = editedTR.rowIndex -1
                    editedTR.children[1].innerHTML = "<input type='text' value='" + data[row].template + "' id='template'>"
                    editedTR.children[2].innerHTML = "<input type='text' value='" + data[row].url + "' id='url'>"

                    $editData = nbInit(editedTR.children[3].children[1])
                    editedTR.children[3].children[1].style.display = 'block';
                    editedTR.children[3].children[0].style.display = 'none';
                    let d = JSON.parse(data[row].data)
                    $editData.editData = Object.keys(d).map((key) => ({key, value: JSON.stringify(d[key]).slice(1,-1)}))
                }
            }
        }
/*        $d['content|dom'] = {ondblclick: function(evt){
            let td  = evt.toElement.tagName == 'INPUT' ? evt.toElement.parentElement : evt.toElement;
            let key = Object.keys(data[0])[td.cellIndex]
            let row = td.parentElement.rowIndex -1
            if (td.children.length){
                data[row][key] = td.children[0].value
                td.innerHTML   = td.children[0].value
                c('UpdateContent', data[row]).then(data => console.log(data), error => console.log(error))
            }
            else {
                input = document.createElement('INPUT')
                input.value = td.innerHTML
                td.innerHTML = '';
                td.appendChild(input)
                //td.innerHTML = "<input value='" + td.innerHTML + "'>"
            }
        }} */
    }, error => console.log(error))
}

$d.newContent = {
    onclick: function(){
        c('NewContent',{}).then(getContent, error => console.log(error))
    }
}

getContent()
