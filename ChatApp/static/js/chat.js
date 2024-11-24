 // 入力量に合わせてtextareaの高さを変更
 const textarea = document.querySelector(".send-msg textarea[type='text']");
 function countLine() {
     textarea.style.height = textarea.scrollHeight + 'px';
 }
 textarea.addEventListener('input', countLine);

 // 編集アイコン（.js-edit-open）を押したらtextareaを表示
 const edits = document.querySelectorAll(".js-edit-open");
 edits.forEach(function (edit) {
     edit.addEventListener('click', () => {
         const chatting = edit.previousElementSibling;
         const editArea = edit.nextElementSibling;

         chatting.style.display = 'none';
         editArea.style.display = 'block';
         edit.style.visibility = 'hidden';
         edit.style.opacity = '0';
     });
 });
