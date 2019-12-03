let lineNo = 0;
let input_view = document.getElementById('input_view');
let search_view = document.getElementById('search_view');
let select_view = document.getElementById('select_view');

let addButton = document.querySelector("#add_line");
addButton.addEventListener('click', (e)=>{
    document.getElementById('temp').classList.add('hidden');
    displaySearch(e);
    
});

function displaySearch(e){
    search_view.classList.remove('hidden');
    input_view.classList.add('hidden');
}

let current_item = null;
document.getElementById('back_search').addEventListener('click', () =>{
    search_view.classList.add('hidden');
    input_view.classList.remove('hidden');
    document.getElementById('search_word').value = '';
});

document.getElementById('search_but').addEventListener('click', async function(e){
    sw = document.getElementById('search_word').value;
    let response = await fetch('/api/search/' + sw);
    let json_res = await response.json();
    // json_res = JSON.parse(json_res)
    search_view.classList.add('hidden');
    select_view.classList.remove('hidden');
    for(let item of json_res){
        item = JSON.parse(item);
        // console.log(item);
        let clone = document.querySelector("#s_temp").cloneNode(true);
        clone.querySelector('.s_id').textContent = item.id;
        clone.querySelector('.s_name span').textContent = item.ten_tai_san;
        clone.querySelector('.s_name span').textContent = item.ten_tai_san;
        clone.querySelector('.s_dv').textContent = item.don_vi_tinh;
        clone.querySelector('.s_sl').textContent = item.so_luong;
       
        clone.querySelector('.choose button').addEventListener('click', function(){
            input_view.classList.remove('hidden');
            select_view.classList.add('hidden');
            //fill a line in input view with selected data and append it to form
            let cloneALine = document.querySelector('#temp').cloneNode(true);
            cloneALine.querySelector('.no').textContent = String(++lineNo);
            cloneALine.querySelector('.id').textContent = item.id;
            cloneALine.querySelector('.type').textContent = item.loai_tai_san;
            cloneALine.querySelector('.name').textContent = item.ten_tai_san;
            cloneALine.querySelector('.state').textContent = item.hien_trang;
            cloneALine.querySelector('.unit').textContent = item.don_vi_tinh;
            cloneALine.classList.remove('hidden');
            document.querySelector('tbody').append(cloneALine);
            // clear data in search view and data view for next search
            document.getElementById('search_word').value = '';
            removeSelectData()
        });

        clone.classList.remove('hidden');
        clone.classList.add('data');
        document.querySelector('#select_table tbody').append(clone);
    }

});
document.getElementById('select_back').addEventListener('click', function(){
    search_view.classList.remove('hidden');
    select_view.classList.add('hidden');
    removeSelectData();
})

function removeSelectData(){
    let data = document.querySelectorAll('#select_table .data');
    for (let line of data){
        line.parentNode.removeChild(line);
    }
}