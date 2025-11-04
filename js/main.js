// 頁面載入完成後執行
document.addEventListener('DOMContentLoaded', function() {
    console.log('網頁載入完成');
    
    // 為功能特點添加動畫效果
    const features = document.querySelectorAll('.feature');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    features.forEach(feature => {
        feature.style.opacity = '0';
        feature.style.transform = 'translateY(20px)';
        feature.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(feature);
    });
    
    // 添加平滑滾動效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 顯示載入時間
    window.addEventListener('load', function() {
        const loadTime = (window.performance.now() / 1000).toFixed(2);
        console.log(`頁面載入時間: ${loadTime} 秒`);
    });
    
    // 添加導航菜單切換功能
    function setupNavigation() {
        const menuToggle = document.querySelector('.menu-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (menuToggle && navMenu) {
            menuToggle.addEventListener('click', function() {
                navMenu.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });
        }
    }
    
    setupNavigation();
    
    // 添加表單提交處理
    function setupFormHandling() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // 在這裡添加表單驗證和提交邏輯
                const formData = new FormData(this);
                
                // 模擬表單提交
                setTimeout(() => {
                    alert('表單提交成功！');
                    this.reset();
                }, 1000);
            });
        });
    }
    
    setupFormHandling();
    
    console.log('JavaScript 功能初始化完成');
});