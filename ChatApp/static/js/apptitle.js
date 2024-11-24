// ========================
// 新規登録ボタン モーダル
// ========================
// 要素を取得
const signupModal = document.getElementById('js-signupModal');
const signupModalOpen = document.getElementById('js-signupModal-open');
const signupModalClose = document.getElementById('js-signupModal-close');

// 「新規登録」ボタンをクリックしてモーダルを開く
function sModalOpen() {
    signupModal.classList.add('is-active');
}
signupModalOpen.addEventListener('click', sModalOpen);
// 閉じるボタンをクリックしてモーダルを閉じる
function sModalClose() {
    signupModal.classList.remove('is-active');
}
signupModalClose.addEventListener('click', sModalClose);
// モーダルの外側をクリックしてモーダルを閉じる
function sModalOut(e) {
    if (e.target == signupModal) {
        signupModal.classList.remove('is-active');
    }
}
addEventListener('click', sModalOut);



// ========================
// ログインボタン モーダル
// ========================
// 要素を取得
const loginModal = document.getElementById('js-loginModal');
const loginModalOpen = document.getElementById('js-loginModal-open');
const loginModalClose = document.getElementById('js-loginModal-close');

// 「ログイン」ボタンをクリックしてモーダルを開く
function lModalOpen() {
    loginModal.classList.add('is-active');
}
loginModalOpen.addEventListener('click', lModalOpen);
// 閉じるボタンをクリックしてモーダルを閉じる
function lModalClose() {
    loginModal.classList.remove('is-active');
}
loginModalClose.addEventListener('click', lModalClose);
// モーダルの外側をクリックしてモーダルを閉じる
function lModalOut(e) {
    if (e.target == loginModal) {
        loginModal.classList.remove('is-active');
    }
}
addEventListener('click', lModalOut);