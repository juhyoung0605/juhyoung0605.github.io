// 네비게이션의 스크롤에 스무스함을 더하기
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);

        window.scrollTo({
            top: targetSection.offsetTop - 50,
            behavior: 'smooth'
        });
    });
});

// 웹사이트 입장시 콘솔 메세지지
console.log("Welcome to my portfolio website! 🚀");
