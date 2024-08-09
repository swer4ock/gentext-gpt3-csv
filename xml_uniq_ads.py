import requests
from lxml import etree
import openai
import time
import os

# Установите ваш API-ключ OpenAI
openai.api_key = "_api_"

# Путь к XML-файлу
xml_url = "https://aichatnow.ru/kolesa/merged.xml"

# Путь к файлу отчета
report_file_path = "report.txt"

# Инициализация переменных для отчета
total_characters_sent = 0
total_characters_received = 0
total_descriptions_processed = 0
total_descriptions = 0

# Загрузка XML с сайта
response = requests.get(xml_url)

if response.status_code == 200:
    try:
        # Используем библиотеку lxml для парсинга XML
        root = etree.fromstring(response.content)

        # Подсчитываем общее количество описаний
        total_descriptions = len(root.findall('.//Ad/Description'))

        # Ищем все теги Description и изменяем их с помощью OpenAI
        for ad_tag in root.findall('.//Ad'):
            description_tag = ad_tag.find('./Description')
            if description_tag is not None:
                original_text = description_tag.text.strip()

                # Попытка отправки запроса к модели с задержкой
                try:
                    # Формируем запрос в соответствии с требуемой структурой
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=[
                            {"role": "system", "content": "Сделай текст на русском языке пожалуйста. Спасибо! Ты супер! Текст в стиле лучших спикеров!"},
                            {"role": "user", "content": original_text},
                            {"role": "assistant", "content": "Теперь добавьте к тексту описание для копирайтинга."}
                        ]
                    )

                    rewritten_text = completion['choices'][0]['message']['content'].strip()

                    # Дополнительный текст
                    additional_text = """
                    У нас вы найдете высококачественную складскую технику и оборудование! 🏗️
                    ☎ Уточняйте наличие и цену по телефону! Поставим в бронь.
                    ⏰ График работы с 9:00-18:00
                    💳 Оплата наличными, кредитной картой, безналичным расчетом! 💸
                    🚚 Отправка в другие города РФ транспортными компаниями
                    ☎ По всем вопросам звоните в любое удобное для Вас время
                    📲 Пишите в WhatsApp ✉

                    🔧 В ассортименте представлены:
                    Погрузчики 🚜
                    Тележки и штабелеры 🚧
                    Вилочные подъемники 🏗️
                    Системы хранения и стеллажи 📦
                    Оборудование для упаковки товаров 📦
                    ✅ Мы гарантируем качество нашей продукции и предоставляем гарантию на всю технику.
                    👩‍🔧 Оказываем услуги по монтажу и обслуживанию оборудования.
                    👨‍🎓 Обучение и консультации по использованию техники.

                    Выбирайте надежное оборудование для вашего бизнеса! 🌟
                    """

                    # Добавляем дополнительный текст к измененному тексту
                    rewritten_text += additional_text

                    # Заменяем исходный текст в XML на измененный текст
                    description_tag.text = rewritten_text

                    # Обновляем значения переменных отчета
                    total_characters_sent += len(original_text)
                    total_characters_received += len(rewritten_text)
                    total_descriptions_processed += 1

                    # Выводим информацию о текущем цикле
                    print(f"Cycle {total_descriptions_processed}/{total_descriptions}:")
                    print(f"Original Text Length: {len(original_text)} characters")
                    print(f"Rewritten Text Length: {len(rewritten_text)} characters")
                    print(f"Total Characters Sent: {total_characters_sent} characters")
                    print(f"Total Characters Received: {total_characters_received} characters")
                    print(f"Total Descriptions Processed: {total_descriptions_processed}/{total_descriptions}")
                    print("----------------------")

                except Exception as e:
                    print(f"An error occurred: {str(e)}")

                    # Добавляем задержку в 30 секунд перед повторной попыткой
                    time.sleep(30)

        # Теперь root содержит измененный XML

        # Получаем текущую директорию
        current_directory = os.getcwd()

        # Создаем путь к файлу в текущей директории
        updated_xml_path = os.path.join(current_directory, "updated_file.xml")

        # Сохраняем измененный XML в файл
        with open(updated_xml_path, 'wb') as xml_file:
            xml_file.write(etree.tostring(root, encoding="utf-8"))

        print(f"Updated XML saved to {updated_xml_path}")

        # Сохраняем отчет в файл
        with open(report_file_path, 'w') as report_file:
            report_file.write(f"Total Characters Sent: {total_characters_sent} characters\n")
            report_file.write(f"Total Characters Received: {total_characters_received} characters\n")
            report_file.write(f"Total Descriptions Processed: {total_descriptions_processed}/{total_descriptions}\n")

        print(f"Report saved to {report_file_path}")

    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
else:
    print(f"Failed to fetch XML from {xml_url}. Status code: {response.status_code}")
