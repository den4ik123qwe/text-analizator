"""
АНАЛИЗАТОР ТОНАЛЬНОСТИ ТЕКСТОВ С GUI ИНТЕРФЕЙСОМ
Использует Tkinter (встроенная библиотека Python)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import tkinter.font as tkfont
from collections import Counter


class SentimentAnalyzerGUI:
    """Графический интерфейс анализатора тональности"""

    # Словари для анализа
    POSITIVE_WORDS = {
        'хороший', 'отличный', 'прекрасный', 'замечательный', 'великолепный',
        'удобный', 'простой', 'легкий', 'понятный', 'классный', 'супер',
        'отлично', 'хорошо', 'прекрасно', 'замечательно', 'великолепно',
        'люблю', 'нравится', 'обожаю', 'восхищаюсь', 'рекомендую',
        'спасибо', 'благодарю', 'рад', 'счастлив', 'доволен', 'удовлетворен',
        'лучший', 'идеальный', 'бесподобный', 'незаменимый', 'полезный',
        'эффективный', 'быстрый', 'качественный', 'профессиональный',
        'восхитительный', 'превосходный', 'исключительный', 'фантастический',
        'надежный', 'стабильный', 'проверенный', 'оптимальный'
    }

    NEGATIVE_WORDS = {
        'плохой', 'ужасный', 'отвратительный', 'кошмарный', 'скучный',
        'сложный', 'трудный', 'неудобный', 'непонятный', 'слабый',
        'плохо', 'ужасно', 'отвратительно', 'кошмарно', 'скучно',
        'ненавижу', 'не нравится', 'разочарован', 'жаль', 'печально',
        'грустно', 'злой', 'сердит', 'разозлен', 'недоволен',
        'худший', 'ужаснейший', 'отвратительнейший', 'бесполезный',
        'неэффективный', 'медленный', 'некачественный', 'непрофессиональный',
        'ужасающий', 'отвратный', 'мерзкий', 'паршивый', 'никудышный',
        'неисправный', 'бракованный', 'дефектный', 'низкосортный'
    }

    INTENSIFIERS = {
        'очень': 1.5,
        'крайне': 2.0,
        'чрезвычайно': 2.0,
        'невероятно': 2.0,
        'необычайно': 1.8,
        'особенно': 1.3,
        'довольно': 1.2,
        'весьма': 1.2,
        'слишком': 1.5,
        'абсолютно': 1.8,
        'совершенно': 1.8,
        'полностью': 1.5,
        'неимоверно': 1.9,
        'исключительно': 1.6
    }

    NEGATIONS = {'не', 'нет', 'ни', 'без', 'отсутствует', 'никак'}

    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор тональности текстов")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')

        # Настройка стилей
        self.setup_styles()

        # Результаты анализа
        self.results = []

        # Создание интерфейса
        self.create_widgets()

    def setup_styles(self):
        """Настройка стилей для виджетов"""
        self.style = ttk.Style()

        # Цвета
        self.COLORS = {
            'bg': '#f0f0f0',
            'positive': '#4CAF50',
            'negative': '#F44336',
            'neutral': '#2196F3',
            'light_bg': '#ffffff',
            'border': '#cccccc',
            'text': '#333333'
        }

    def create_widgets(self):
        """Создание всех элементов интерфейса"""

        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            title_frame,
            text="📊 АНАЛИЗАТОР ТОНАЛЬНОСТИ ТЕКСТОВ",
            font=tkfont.Font(family="Arial", size=18, weight="bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['text']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Введите текст для анализа тональности",
            font=tkfont.Font(family="Arial", size=11),
            bg=self.COLORS['bg'],
            fg='#666666'
        )
        subtitle_label.pack(pady=(5, 0))

        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.COLORS['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Левая панель (ввод текста)
        left_panel = tk.Frame(main_container, bg=self.COLORS['light_bg'], relief=tk.RAISED, borderwidth=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Правая панель (результаты)
        right_panel = tk.Frame(main_container, bg=self.COLORS['light_bg'], relief=tk.RAISED, borderwidth=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # ===== ЛЕВАЯ ПАНЕЛЬ =====

        # Заголовок левой панели
        left_title = tk.Label(
            left_panel,
            text="ВВОД ТЕКСТА",
            font=tkfont.Font(family="Arial", size=12, weight="bold"),
            bg=self.COLORS['light_bg'],
            fg=self.COLORS['text']
        )
        left_title.pack(pady=15)

        # Поле для ввода текста
        input_frame = tk.Frame(left_panel, bg=self.COLORS['light_bg'])
        input_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.text_input = scrolledtext.ScrolledText(
            input_frame,
            height=15,
            width=40,
            font=tkfont.Font(family="Arial", size=11),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)

        # Примеры текстов
        examples_frame = tk.Frame(left_panel, bg=self.COLORS['light_bg'])
        examples_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        examples_label = tk.Label(
            examples_frame,
            text="Примеры для быстрого теста:",
            font=tkfont.Font(family="Arial", size=10),
            bg=self.COLORS['light_bg'],
            fg='#666666'
        )
        examples_label.pack(anchor=tk.W)

        examples_buttons_frame = tk.Frame(examples_frame, bg=self.COLORS['light_bg'])
        examples_buttons_frame.pack(fill=tk.X, pady=(5, 0))

        example_texts = [
            ("😊 Позитивный", "Это очень хороший и качественный продукт, я доволен покупкой!"),
            ("😠 Негативный", "Ужасный сервис, все очень плохо и неудобно."),
            ("😐 Нейтральный", "Продукт нормальный, но есть небольшие проблемы.")
        ]

        for emoji, text in example_texts:
            btn = tk.Button(
                examples_buttons_frame,
                text=emoji,
                command=lambda t=text: self.load_example(t),
                font=tkfont.Font(family="Arial", size=10),
                bg='#e0e0e0',
                relief=tk.RAISED,
                borderwidth=1,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=(0, 5))

        # Кнопки управления
        buttons_frame = tk.Frame(left_panel, bg=self.COLORS['light_bg'])
        buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        analyze_btn = tk.Button(
            buttons_frame,
            text="🔍 АНАЛИЗИРОВАТЬ ТЕКСТ",
            command=self.analyze_text,
            font=tkfont.Font(family="Arial", size=11, weight="bold"),
            bg=self.COLORS['positive'],
            fg='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        analyze_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ ОЧИСТИТЬ",
            command=self.clear_text,
            font=tkfont.Font(family="Arial", size=10),
            bg='#ff9800',
            fg='white',
            relief=tk.RAISED,
            borderwidth=1,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT)

        # ===== ПРАВАЯ ПАНЕЛЬ =====

        # Заголовок правой панели
        right_title = tk.Label(
            right_panel,
            text="РЕЗУЛЬТАТЫ АНАЛИЗА",
            font=tkfont.Font(family="Arial", size=12, weight="bold"),
            bg=self.COLORS['light_bg'],
            fg=self.COLORS['text']
        )
        right_title.pack(pady=15)

        # Контейнер для результатов
        results_container = tk.Frame(right_panel, bg=self.COLORS['light_bg'])
        results_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Верхняя часть результатов
        top_results_frame = tk.Frame(results_container, bg=self.COLORS['light_bg'])
        top_results_frame.pack(fill=tk.X, pady=(0, 15))

        # Виджеты для отображения тональности
        self.sentiment_label = tk.Label(
            top_results_frame,
            text="Тональность: --",
            font=tkfont.Font(family="Arial", size=14, weight="bold"),
            bg=self.COLORS['light_bg'],
            fg=self.COLORS['text']
        )
        self.sentiment_label.pack(anchor=tk.W)

        self.score_label = tk.Label(
            top_results_frame,
            text="Оценка: 0.000",
            font=tkfont.Font(family="Arial", size=12),
            bg=self.COLORS['light_bg'],
            fg='#666666'
        )
        self.score_label.pack(anchor=tk.W, pady=(5, 0))

        # Цветной индикатор тональности
        self.sentiment_bar = tk.Canvas(
            top_results_frame,
            height=20,
            bg='#e0e0e0',
            highlightthickness=0
        )
        self.sentiment_bar.pack(fill=tk.X, pady=(10, 0))
        self.draw_sentiment_bar(0)  # Начальное состояние

        # Детализированные результаты
        details_frame = tk.LabelFrame(
            results_container,
            text="ДЕТАЛИ АНАЛИЗА",
            font=tkfont.Font(family="Arial", size=10, weight="bold"),
            bg=self.COLORS['light_bg'],
            fg=self.COLORS['text'],
            relief=tk.GROOVE,
            borderwidth=1
        )
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Поле для детальных результатов
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            height=10,
            width=40,
            font=tkfont.Font(family="Arial", size=10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Статистика
        stats_frame = tk.Frame(results_container, bg=self.COLORS['light_bg'])
        stats_frame.pack(fill=tk.X, pady=(15, 0))

        self.stats_label = tk.Label(
            stats_frame,
            text="Проанализировано текстов: 0",
            font=tkfont.Font(family="Arial", size=10),
            bg=self.COLORS['light_bg'],
            fg='#666666'
        )
        self.stats_label.pack(anchor=tk.W)

        # Кнопка очистки истории
        clear_history_btn = tk.Button(
            stats_frame,
            text="📊 ОЧИСТИТЬ ИСТОРИЮ",
            command=self.clear_history,
            font=tkfont.Font(family="Arial", size=9),
            bg='#9E9E9E',
            fg='white',
            relief=tk.RAISED,
            borderwidth=1,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        clear_history_btn.pack(anchor=tk.E, pady=(5, 0))

    def load_example(self, text):
        """Загрузка примера текста"""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, text)

    def clean_text(self, text):
        """Очистка текста для анализа"""
        text = text.lower()
        for char in '!?.,:;()[]{}"\'«»':
            text = text.replace(char, ' ')
        return text

    def analyze_sentiment(self, text):
        """Основной алгоритм анализа тональности"""
        original_text = text
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()

        if not words:
            return None

        score = 0
        positive_count = 0
        negative_count = 0
        positive_words = []
        negative_words = []

        i = 0
        while i < len(words):
            word = words[i]
            word_score = 0
            intensifier = 1.0

            # Проверяем усилители
            if word in self.INTENSIFIERS and i + 1 < len(words):
                intensifier = self.INTENSIFIERS[word]
                i += 1
                if i >= len(words):
                    break
                word = words[i]

            # Проверяем отрицания
            is_negated = False
            if i > 0 and words[i - 1] in self.NEGATIONS:
                is_negated = True

            # Проверяем позитивные слова
            if word in self.POSITIVE_WORDS:
                if is_negated:
                    word_score = -1 * intensifier
                    negative_count += 1
                    negative_words.append(f"не {word}")
                else:
                    word_score = 1 * intensifier
                    positive_count += 1
                    positive_words.append(word)

            # Проверяем негативные слова
            elif word in self.NEGATIVE_WORDS:
                if is_negated:
                    word_score = 1 * intensifier
                    positive_count += 1
                    positive_words.append(f"не {word}")
                else:
                    word_score = -1 * intensifier
                    negative_count += 1
                    negative_words.append(word)

            score += word_score
            i += 1

        # Нормализация оценки
        total_words = len(words)
        normalized_score = score / total_words if total_words > 0 else 0

        # Определение категории
        if normalized_score > 0.2:
            sentiment = "ПОЗИТИВНЫЙ"
            color = self.COLORS['positive']
            emoji = "😊"
        elif normalized_score > 0.05:
            sentiment = "СЛАБО ПОЗИТИВНЫЙ"
            color = "#8BC34A"  # светлозеленый
            emoji = "🙂"
        elif normalized_score < -0.2:
            sentiment = "НЕГАТИВНЫЙ"
            color = self.COLORS['negative']
            emoji = "😠"
        elif normalized_score < -0.05:
            sentiment = "СЛАБО НЕГАТИВНЫЙ"
            color = "#FF9800"  # оранжевый
            emoji = "😐"
        else:
            sentiment = "НЕЙТРАЛЬНЫЙ"
            color = self.COLORS['neutral']
            emoji = "😐"

        # Формируем результат
        result = {
            'text': original_text[:200] + "..." if len(original_text) > 200 else original_text,
            'full_text': original_text,
            'score': round(score, 2),
            'normalized_score': round(normalized_score, 3),
            'sentiment': sentiment,
            'emoji': emoji,
            'color': color,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'positive_list': positive_words[:10],  # первые 10 слов
            'negative_list': negative_words[:10],
            'total_words': total_words,
            'char_count': len(original_text)
        }

        return result

    def analyze_text(self):
        """Обработка нажатия кнопки анализа"""
        text = self.text_input.get(1.0, tk.END).strip()

        if not text:
            messagebox.showwarning("Внимание", "Пожалуйста, введите текст для анализа!")
            return

        # Анализируем текст
        result = self.analyze_sentiment(text)

        if result is None:
            messagebox.showwarning("Внимание", "Не удалось проанализировать текст!")
            return

        # Добавляем в историю
        self.results.append(result)

        # Обновляем интерфейс
        self.update_results_display(result)

        # Обновляем статистику
        self.update_statistics()

    def update_results_display(self, result):
        """Обновление отображения результатов"""
        # Обновляем метки
        self.sentiment_label.config(
            text=f"{result['emoji']} Тональность: {result['sentiment']}",
            fg=result['color']
        )

        self.score_label.config(
            text=f"Оценка: {result['normalized_score']} (слов: {result['total_words']}, символов: {result['char_count']})"
        )

        # Обновляем цветную шкалу
        self.draw_sentiment_bar(result['normalized_score'])

        # Обновляем детализированную информацию
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)

        details = f"""
📝 ТЕКСТ:
{result['full_text'][:500]}{'...' if len(result['full_text']) > 500 else ''}

📊 РЕЗУЛЬТАТЫ:
• Общая оценка: {result['score']}
• Нормализованная оценка: {result['normalized_score']}
• Категория: {result['sentiment']}

📈 СТАТИСТИКА:
• Всего слов: {result['total_words']}
• Позитивных слов: {result['positive_words']}
• Негативных слов: {result['negative_words']}

🔍 ОБНАРУЖЕННЫЕ СЛОВА:
"""

        if result['positive_list']:
            details += f"• Позитивные: {', '.join(result['positive_list'])}\n"

        if result['negative_list']:
            details += f"• Негативные: {', '.join(result['negative_list'])}\n"

        self.details_text.insert(1.0, details)
        self.details_text.config(state=tk.DISABLED)

    def draw_sentiment_bar(self, score):
        """Рисование цветной шкалы тональности"""
        self.sentiment_bar.delete("all")

        width = self.sentiment_bar.winfo_width()
        if width < 10:  # Если холст еще не отрисован
            width = 300

        height = 20

        # Фон
        self.sentiment_bar.create_rectangle(0, 0, width, height, fill='#e0e0e0', outline='')

        # Цветная полоса в зависимости от оценки
        # Оценка от -1 до 1, преобразуем в координаты от 0 до width
        center_x = width / 2
        bar_width = abs(score) * (width / 2)

        if score > 0:
            # Позитивная (зеленая) часть
            x1 = center_x
            x2 = center_x + bar_width
            color = self.COLORS['positive']
        elif score < 0:
            # Негативная (красная) часть
            x1 = center_x - bar_width
            x2 = center_x
            color = self.COLORS['negative']
        else:
            # Нейтральная
            x1 = center_x - 1
            x2 = center_x + 1
            color = self.COLORS['neutral']

        self.sentiment_bar.create_rectangle(x1, 0, x2, height, fill=color, outline='')

        # Центральная линия
        self.sentiment_bar.create_line(center_x, 0, center_x, height, fill='#333333', width=2)

        # Подписи
        self.sentiment_bar.create_text(10, height / 2, text="-1 (негатив)", anchor=tk.W, fill='#666666',
                                       font=('Arial', 8))
        self.sentiment_bar.create_text(width - 10, height / 2, text="+1 (позитив)", anchor=tk.E, fill='#666666',
                                       font=('Arial', 8))

        # Текущее значение
        if abs(score) > 0.01:  # Не показываем для нулевых значений
            value_x = center_x + (score * width / 2)
            self.sentiment_bar.create_oval(value_x - 4, height / 2 - 4, value_x + 4, height / 2 + 4, fill='white',
                                           outline='#333333', width=2)

    def update_statistics(self):
        """Обновление статистики"""
        total = len(self.results)

        if total == 0:
            self.stats_label.config(text="Проанализировано текстов: 0")
            return

        # Подсчет категорий
        sentiments = [r['sentiment'] for r in self.results]
        pos_count = sum(1 for s in sentiments if 'ПОЗИТИВ' in s)
        neg_count = sum(1 for s in sentiments if 'НЕГАТИВ' in s)
        neu_count = total - pos_count - neg_count

        self.stats_label.config(
            text=f"Проанализировано текстов: {total} "
                 f"(😊: {pos_count}, 😐: {neu_count}, 😠: {neg_count})"
        )

    def clear_text(self):
        """Очистка поля ввода"""
        self.text_input.delete(1.0, tk.END)

    def clear_history(self):
        """Очистка истории анализа"""
        if not self.results:
            messagebox.showinfo("Информация", "История анализа пуста!")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить историю анализа?"):
            self.results = []

            # Сброс интерфейса
            self.sentiment_label.config(
                text="Тональность: --",
                fg=self.COLORS['text']
            )
            self.score_label.config(text="Оценка: 0.000")
            self.draw_sentiment_bar(0)

            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            self.details_text.config(state=tk.DISABLED)

            self.update_statistics()

            messagebox.showinfo("Успех", "История анализа очищена!")


def main():
    """Основная функция для запуска приложения"""
    root = tk.Tk()
    app = SentimentAnalyzerGUI(root)

    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Запрет изменения размера
    root.resizable(True, True)

    root.mainloop()


if __name__ == "__main__":
    main()