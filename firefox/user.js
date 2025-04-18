// Домашняя страница и новое окно
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // Включить поддержку userChrome.css
user_pref("browser.startup.page", 0); // При запуске открывать пустую страницу (0), вместо домашней (1) или последних вкладок (3)

// Отключить рекламный контент на стартовой странице Firefox и очистить топ-сайты по умолчанию
user_pref("browser.newtabpage.activity-stream.showSponsored", false); // Отключить спонсируемые истории
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false); // Отключить спонсируемые сайты
user_pref("browser.newtabpage.activity-stream.default.sites", ""); // Очистить список сайтов по умолчанию

// Встроенный калькулятор в адресной строке
user_pref("browser.urlbar.suggest.calculator", true); // Включить подсказки калькулятора при вводе математических выражений
