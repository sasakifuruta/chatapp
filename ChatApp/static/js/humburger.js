// メニュー外をクリックしたらハンバーガーメニューを閉じる
document.addEventListener('click', (event)=>{
    const menuCheck = document.getElementById('menu-btn-check');
    const menuContent = document.getElementById('js-menuContent');
    const menuBtn = document.getElementById('js-menuBtn');
    console.log(event.target)
    if (!menuCheck.contains(event.target) && !menuContent.contains(event.target) && !menuBtn.contains(event.target)){
        menuCheck.checked = false;
    }
});