function toggleLanguage() {
    const lang = document.documentElement.lang === 'ru' ? 'en' : 'ru'; 
    document.documentElement.lang = lang;


    const elements = document.querySelectorAll('[data-ru], [data-en]');


    elements.forEach(element => {
        const key = lang === 'ru' ? 'data-ru' : 'data-en'; 
        if (element.hasAttribute(key)) {
            element.innerText = element.getAttribute(key); 
        }
    });

    const submitButtons = document.querySelectorAll('input[type="submit"], button');
    submitButtons.forEach(button => {
        const key = lang === 'ru' ? 'data-ru' : 'data-en'; 
        if (button.hasAttribute(key)) {
            button.value = button.getAttribute(key);  
            button.innerText = button.getAttribute(key);  
        }
    });


    const langToggleButton = document.getElementById('langToggle');
    if (langToggleButton) {
        langToggleButton.innerText = lang === 'ru' ? 'En' : 'Ru';  
    }
}
