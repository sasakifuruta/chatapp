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


// ================
// チャットを更新
// ===============
document.getElementById('send-button').addEventListener('click', function(){
	event.preventDefault();  // フォーム送信を防ぐ

	const messageInput = document.getElementById('message-input');
	const message = messageInput.value;
	const cidInput = document.getElementById('cid-input');
	const cid = cidInput.value;
	console.log(cid);
	console.log('押したよ')

	// メッセージが空なら送信しない
	if (message.trim()=== '') return;

	const xhr = new XMLHttpRequest();
	xhr.open('POST', '/post_message', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')

	xhr.onload = function() {
		if(xhr.status === 200){
			const response = JSON.parse(xhr.responseText);
			console.log(xhr.responseText);
			if(response.status === 'success'){
				updateChat(response.messages);
				messageInput.value = '';
			}else {
				alert(response.message);
			}
		};
	}
	// サーバーへ送信
	xhr.send(`message=${encodeURIComponent(message)}&cid=${cid}`);
});

function updateChat(messages) {
	const chatContainer = document.getElementById('chat-container');
	chatContainer.innerHTML = '';

	messages.forEach(function(message, user_id) {
		console.log(message.uid)
		console.log(user_id)
		const msgDiv = document.createElement('div');
		msgDiv.classList.add('msgs-area');
		msgDiv.classList.add(message.uid == user_id ? 'right' : 'left');

            msgDiv.innerHTML = `
                <figure class="icon-img">
                    <div class="avatar">
                        ${message.profile_img ? 
                            `<img class="user-avatar profile" src="/static/${message.profile_img}">` :
                            `<i class="user-avatar default-icon fa-solid fa-circle-user"></i>`
                        }
                    </div>
                    <figcaption class="icon-name">${message.user_name}</figcaption>
                </figure>
                <div class="chatting">
                    <p class="chat-text">${message.content}</p>
                </div>
            `;
            chatContainer.appendChild(msgDiv);
	});
}
