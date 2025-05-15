user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true); // Включить поддержку userChrome.css

// Отключить рекламный контент на стартовой странице Firefox и очистить топ-сайты по умолчанию
user_pref("browser.newtabpage.activity-stream.showSponsored", false); // Отключить спонсируемые истории
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false); // Отключить спонсируемые сайты
user_pref("browser.newtabpage.activity-stream.default.sites", ""); // Очистить список сайтов по умолчанию

// Встроенный калькулятор в адресной строке
user_pref("browser.urlbar.suggest.calculator", true); // Включить подсказки калькулятора при вводе математических выражений

// Восстанавливать последнюю сессию при запуске
user_pref("browser.startup.page", 3); // 0=пустая, 1=домашняя, 2=последние, 3=восстановить

// Сохранять сессию чаще (в миллисекундах)
user_pref("sessionstore.interval", 15000); // 15 секунд

// Увеличить лимит сохраняемых закрытых вкладок
user_pref("browser.sessionstore.max_tabs_undo", 50);

// Сохранять все вкладки принудительно (даже если Firefox завершился аварийно)
user_pref("browser.sessionstore.resume_from_crash", true);

// Не пропускать вкладки при восстановлении
user_pref("browser.sessionstore.privacy_level", 0); // 0=сохранять всё, 2=не сохранять данные форм

// Увеличить глубину истории сессий (если нужно)
user_pref("browser.sessionstore.max_serialize_back", 5); // сколько предыдущих сессий хранить

// Восстановление сессии
user_pref("browser.sessionstore.restore_on_demand", true); // загружать вкладки по требованию
user_pref("browser.sessionstore.max_concurrent_tabs", 0); // не ограничивать параллельную загрузку (но работает в связке с restore_on_demand)

// Отключение фоновой загрузки
user_pref("browser.sessionstore.restore_pinned_tabs_on_demand", true); // не загружать закрепленные вкладки
user_pref("browser.sessionstore.restore_hidden_tabs_on_demand", true); // не загружать скрытые вкладки

// Оптимизация (чтобы Firefox не нагружал интернет)
user_pref("network.http.max-persistent-connections-per-server", 4); // ограничить параллельные соединения
user_pref("browser.tabs.unloadOnLowMemory", true); // выгружать неактивные вкладки при нехватке памяти
