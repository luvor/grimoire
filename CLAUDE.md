# Grimoire — Инструкции для агентов

## Что это

Grimoire (グリモワール) — статический сайт-платформа для публикации лонгридов на GitHub Pages. Каждая статья — глубокое исследование идеи с фактами, визуализацией, схемами и красивой вёрсткой.

**GitHub Pages URL**: `https://luvor.github.io/grimoire/`
**Репозиторий**: `luvor/grimoire`

## Структура проекта

```
/
├── index.html                    # Главная страница с карточками статей
├── assets/
│   ├── css/
│   │   ├── main.css              # Основные стили, темы, карточки
│   │   └── article.css           # Стили статей (типографика, TOC, и т.д.)
│   ├── js/
│   │   ├── main.js               # Тема, анимации, навигация
│   │   └── article.js            # Прогресс чтения, TOC, время чтения
│   ├── images/                   # Общие изображения сайта
│   └── fonts/                    # Локальные шрифты (если нужны)
├── articles/
│   └── {article-slug}/           # Каждая статья в своей папке
│       ├── index.html            # HTML статьи
│       ├── cover.svg             # Обложка (SVG предпочтительно)
│       ├── research.md           # Результаты исследования
│       ├── concept.md            # Концепт (если применимо)
│       └── images/               # Изображения статьи
├── templates/
│   └── article.html              # Шаблон для новых статей
└── CLAUDE.md                     # Эти инструкции
```

## Как добавить новую статью

### Шаг 1: Подготовка

1. Создай папку: `articles/{article-slug}/`
2. Скопируй шаблон: `templates/article.html` → `articles/{article-slug}/index.html`

### Шаг 2: Исследование (ОБЯЗАТЕЛЬНО)

Каждая статья должна быть подкреплена исследованием. Используй следующий процесс:

1. **Сбор фактов** — используй WebSearch и WebFetch для поиска:
   - Научные данные и статистика
   - Исторический контекст
   - Мнения экспертов
   - Конкретные примеры и кейсы
   - Даты, имена, числа

2. **Структурирование** — сохрани результаты в `research.md`:
   ```markdown
   # Исследование: {Тема}

   ## Ключевые факты
   - Факт 1 (источник)
   - Факт 2 (источник)

   ## Исторический контекст
   ...

   ## Экспертные мнения
   ...

   ## Статистика и данные
   ...

   ## Источники
   1. URL или название
   ```

3. **Верификация** — перепроверь ключевые утверждения через несколько источников

### Шаг 3: Написание статьи

Структура лонгрида:

1. **Захватывающий ввод** — начни с провокационного вопроса или факта. Используй класс `drop-cap` для первого параграфа.
2. **Контекст проблемы** — почему это важно
3. **Глубокий анализ** — факты, данные, примеры
4. **Концепт/решение** (если применимо) — что предлагается
5. **Заключение** — ключевые выводы

#### Стиль текста:
- Пиши ярко, не академично
- Короткие параграфы (3-4 предложения)
- Используй риторические вопросы
- Приводи конкретные примеры
- Вставляй цитаты и факты

### Шаг 4: Визуализация

#### SVG-схемы
Создавай SVG-диаграммы прямо в HTML. Используй цвета из CSS custom properties:
```html
<figure class="diagram">
  <svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <!-- Используй цвета: #d4a574 (акцент), #e8e6e3 (текст), #14141f (фон) -->
  </svg>
  <figcaption>Описание диаграммы</figcaption>
</figure>
```

#### Изображения
- Обложка: SVG с абстрактной композицией (800x500 минимум)
- В статье: используй `<figure>` с `<figcaption>`
- Для широких изображений: класс `figure-wide` или `figure-full`
- Для сравнений: класс `image-compare`
- Для галерей: класс `image-gallery`

#### Создание SVG обложек
Обложка должна быть абстрактной, стильной, отражать тему статьи. Используй:
- Геометрические формы
- Градиенты с цветами палитры
- Минимализм
- Размер: viewBox="0 0 1200 700"

### Шаг 5: HTML-вёрстка

Замени плейсхолдеры в шаблоне:
- `{{ARTICLE_TITLE}}` — заголовок
- `{{ARTICLE_SUBTITLE}}` — подзаголовок
- `{{ARTICLE_EXCERPT}}` — короткое описание (1-2 предложения)
- `{{CATEGORY}}` — категория (например, "Спорт & Дизайн")
- `{{DATE}}` — дата публикации
- `{{COVER_IMAGE_URL}}` — URL обложки для OG
- `{{ARTICLE_CONTENT}}` — контент статьи
- `{{TAGS}}` — теги: `<span class="article-tag">тег</span>`

#### HTML-элементы статьи:

```html
<!-- Обычный параграф -->
<p>Текст</p>

<!-- Параграф с буквицей (первый в статье) -->
<p class="drop-cap">Первый параграф статьи...</p>

<!-- Цитата -->
<blockquote>
  <p>Текст цитаты</p>
  <cite>Автор</cite>
</blockquote>

<!-- Pull-quote (выделенная цитата на всю ширину) -->
<div class="pull-quote">
  <p>Важная мысль, которую нужно выделить</p>
</div>

<!-- Информационный блок -->
<div class="info-box">
  <div class="info-box-title">Факт</div>
  <p>Интересный факт или пояснение</p>
</div>

<!-- Боковая заметка -->
<span class="sidenote-marker">*</span>
<aside class="sidenote">Дополнительная информация</aside>

<!-- Сноска в тексте -->
<sup><a href="#fn-1" class="footnote-ref" id="fnref-1">1</a></sup>

<!-- Широкое изображение -->
<figure class="figure-wide">
  <img src="images/photo.jpg" alt="Описание">
  <figcaption>Подпись к изображению</figcaption>
</figure>

<!-- Полноэкранное изображение -->
<figure class="figure-full">
  <img src="images/photo.jpg" alt="Описание">
  <figcaption>Подпись</figcaption>
</figure>

<!-- Сравнение (до/после) -->
<div class="image-compare">
  <figure>
    <span class="compare-label">До</span>
    <img src="images/before.jpg" alt="До">
  </figure>
  <figure>
    <span class="compare-label">После</span>
    <img src="images/after.jpg" alt="После">
  </figure>
</div>

<!-- SVG-диаграмма -->
<figure class="diagram">
  <svg viewBox="0 0 800 400">...</svg>
  <figcaption>Описание схемы</figcaption>
</figure>
```

### Шаг 6: Обновление главной страницы

Добавь карточку статьи в `index.html` в секцию `.articles-grid`:

```html
<article class="article-card">
  <a href="articles/{slug}/" class="card-inner">
    <div class="card-image">
      <img src="articles/{slug}/cover.svg" alt="Заголовок" loading="lazy">
      <span class="card-category">Категория</span>
    </div>
    <div class="card-content">
      <div class="card-meta">
        <span>Дата</span>
        <span class="card-meta-divider"></span>
        <span>X минут чтения</span>
      </div>
      <h3 class="card-title">Заголовок статьи</h3>
      <p class="card-excerpt">Краткое описание...</p>
      <div class="card-footer">
        <span class="card-read-more">
          Читать
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </span>
        <span class="card-number">XX</span>
      </div>
    </div>
  </a>
</article>
```

### Шаг 7: Публикация

```bash
git add .
git commit -m "Новая статья: {название}"
git push origin main
```

GitHub Pages автоматически обновится.

## Дизайн-система

### Цвета (CSS custom properties)
- `--color-accent: #d4a574` — золотой акцент (тёмная тема)
- `--color-accent: #8b5e3c` — коричневый акцент (светлая тема)
- Все цвета доступны через `var(--color-*)` в main.css

### Шрифты
- Заголовки: `Cormorant Garamond` (var(--font-display))
- Основной текст: `Source Serif 4` (var(--font-body))
- Код: `JetBrains Mono` (var(--font-mono))
- Японский: `Noto Serif JP`

### Принципы
1. **Контент-первый** — текст должен быть читаемым и красивым
2. **Визуально насыщенный** — SVG-схемы, фотографии, диаграммы
3. **Два режима** — тёмная и светлая тема
4. **Мобильный** — адаптивная вёрстка
5. **Без фреймворков** — чистый HTML/CSS/JS для GitHub Pages

## Рекомендации по качеству

- Минимум 1500 слов на статью
- Минимум 3 визуализации (SVG, изображения, диаграммы)
- Все факты должны быть проверены
- Обязательна секция с источниками
- Текст должен быть живым, не сухим
- Каждая статья — это мини-расследование
