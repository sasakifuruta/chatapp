// プロフィール画像ファイル選択時のプレビュー
// 画像をアップロードした時に発火
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('file_upload').addEventListener('change', (e) => {
        defaultIcon = document.getElementById('default-icon');
        jsPreview = document.getElementById("jsPreview");

        const file = e.target.files[0];
        console.log(file)
        if (file) {
            const fileReader = new FileReader();
            fileReader.onload = (event) => {
                jsPreview.style.display = 'block';
                jsPreview.src = event.target.result;
                defaultIcon.style.display = 'none';
            }
            fileReader.readAsDataURL(file);
        }
    })
});