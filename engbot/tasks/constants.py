EXPIRE_TIME_TO_NOTICE_LEARN = 86400  # 1 day
EXPIRE_TIME_TO_ASKING_TRANSLATE = 86400  # 1 day

TIME_ASKING_TRANSLATE = {"hour": 14, "minute": 30}

MORNING_TIME = (7, 8)
EVENING_TIME = (16, 17)

NOTICE_INTERVAL_HOUR = 12

TEXT_FOR_NOTICE = (
    "🤟🏻 Вы давно не записывали новые слова\n\n💡 Не забывайте - регулярные занятия способствуют обучению.",
    "📢 Продолжайте пополнять свой словарный запас\n\n✏️ Запишите новое слово /new",
)

TEXT_FOR_ASKING = "👋 Хей я тут взял слово, из тех что ты записывал, сможешь его вспомнить, не подсматривая?🇬🇧\n\n{eng_word} - {translate}\n\n📕 Не забывай повторять записанные слова загляни в свой словарь /words"
