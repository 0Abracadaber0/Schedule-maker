function toggleLanguage() {
    // Переключаем язык между 'ru' и 'en'
    const lang = document.documentElement.lang === 'ru' ? 'en' : 'ru';
    document.documentElement.lang = lang;

    // Сохраняем выбранный язык в localStorage
    localStorage.setItem('preferredLanguage', lang);

    // Обновляем текст всех элементов с атрибутами data-ru или data-en
    const elements = document.querySelectorAll('[data-ru], [data-en]');
    elements.forEach(element => {
        const key = lang === 'ru' ? 'data-ru' : 'data-en'; 
        if (element.hasAttribute(key)) {
            element.innerText = element.getAttribute(key); 
        }
    });

    // Обновляем текст на кнопках и submit-элементах
    const submitButtons = document.querySelectorAll('input[type="submit"], button');
    submitButtons.forEach(button => {
        const key = lang === 'ru' ? 'data-ru' : 'data-en'; 
        if (button.hasAttribute(key)) {
            button.value = button.getAttribute(key);  
            button.innerText = button.getAttribute(key);  
        }
    });

    // Обновляем текст кнопки переключения языка
    const langToggleButton = document.getElementById('langToggle');
    if (langToggleButton) {
        langToggleButton.innerText = lang === 'ru' ? 'En' : 'Ru'; // Изменяем текст на кнопке
    }
}

// Инициализация языка при загрузке страницы на основе значения в localStorage
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLanguage'); // Получаем сохранённый язык из localStorage
    const defaultLang = savedLang ? savedLang : 'ru'; // Если язык не найден, по умолчанию выбираем 'ru'
    document.documentElement.lang = defaultLang;

    // Обновляем текст всех элементов с атрибутами data-ru или data-en
    const elements = document.querySelectorAll('[data-ru], [data-en]');
    elements.forEach(element => {
        const key = defaultLang === 'ru' ? 'data-ru' : 'data-en'; 
        if (element.hasAttribute(key)) {
            element.innerText = element.getAttribute(key); // Устанавливаем текст на основе языка
        }
    });

    // Обновляем текст на кнопках
    const submitButtons = document.querySelectorAll('input[type="submit"], button');
    submitButtons.forEach(button => {
        const key = defaultLang === 'ru' ? 'data-ru' : 'data-en'; 
        if (button.hasAttribute(key)) {
            button.value = button.getAttribute(key);
            button.innerText = button.getAttribute(key);
        }
    });

    // Обновляем текст на кнопке переключения языка
    const langToggleButton = document.getElementById('langToggle');
    if (langToggleButton) {
        langToggleButton.innerText = defaultLang === 'ru' ? 'En' : 'Ru';
    }
});
