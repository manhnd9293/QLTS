let lineNo = 0;
let input_view = document.getElementById('input_view');
let search_view = document.getElementById('search_view');
let select_view = document.getElementById('select_view');
document.getElementById('temp').classList.add('hidden');

let addButton = document.querySelector("#add_line");
addButton.addEventListener('click', (e)=>{
    displaySearch(e);
    
});

function displaySearch(e){
    search_view.classList.remove('hidden');
    input_view.classList.add('hidden');
}
let current_item = null;
document.getElementById('search_but').addEventListener('click', async function(e){
    sw = document.getElementById('search_word').value;
    let response = await fetch('/api/search/' + sw);
    let json_res = await response.json();
    // json_res = JSON.parse(json_res)
    console.log(json_res[0]);
    search_view.classList.add('hidden');
    select_view.classList.remove('hidden');
    for(let item of json_res){
        item = JSON.parse(item);
        console.log(item);
        let clone = document.querySelector("#s_temp").cloneNode(true);
        clone.querySelector('.s_id').textContent = item.id;
        clone.querySelector('.s_name span').textContent = item.ten_tai_san;
        clone.querySelector('.s_name span').textContent = item.ten_tai_san;
        clone.querySelector('.s_dv').textContent = item.don_vi_tinh;
        clone.querySelector('.s_sl').textContent = item.so_luong;
       
        clone.querySelector('.choose button').addEventListener('click', function(){
            input_view.classList.remove('hidden');
            select_view.classList.add('hidden');
            let cloneALine = document.querySelector('#temp').cloneNode(true);
            cloneALine.querySelector('.no').textContent = String(++lineNo);
            cloneALine.querySelector('.id').textContent = item.id;
            cloneALine.querySelector('.type').textContent = item.loai_tai_san;
            cloneALine.querySelector('.name').textContent = item.ten_tai_san;
            cloneALine.querySelector('.state').textContent = item.hien_trang;
            cloneALine.querySelector('.unit').textContent = item.don_vi_tinh;
            cloneALine.classList.remove('hidden');
            document.querySelector('tbody').append(cloneALine);
            document.querySelector('#select_table .data').innerHTML = '';
        });

        clone.classList.remove('hidden');
        clone.classList.add('data');
        document.querySelector('#select_table tbody').append(clone);
    }

});
document.getElementById('select_back').addEventListener('click', function(){
    search_view.classList.remove('hidden');
    select_view.classList.add('hidden');
})