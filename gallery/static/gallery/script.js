document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    // ハンバーガーメニューのクリックイベント
    hamburger.addEventListener('click', function() {
        // クリックされたことをコンソールで確認
        console.log('Hamburger clicked');
        
        // クラスの切り替え
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // メニューの外側をクリックした時にメニューを閉じる
    document.addEventListener('click', function(event) {
        if (!hamburger.contains(event.target) && !navLinks.contains(event.target)) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });

    // 各メニューリンクをクリックした時にメニューを閉じる
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
});