from django import forms
from django.utils.safestring import mark_safe
import json


class TestCaseStepsWidget(forms.Widget):
    """
    Кастомный виджет для редактирования inner_content — визуально как список шагов,
    с возможностью переключения на JSON-редактор (в виде табов) и Drag & Drop.
    """
    class Media:
        # Добавляем SortableJS для Drag & Drop
        js = (
            "admin/js/Sortable.min.js", # Вам нужно скачать этот файл
            "admin/js/testcase_step.js",
        )
        css = {"all": ("admin/css/testcase_step.css",)}

    def render(self, name, value, attrs=None, renderer=None):
        # 1. Обработка входящего значения (из базы)
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except Exception:
                value = []
        elif not value:
            value = []

        json_value = json.dumps(value, ensure_ascii=False, indent=2)

        html = [
            # 1. Заголовок поля
            '<div class="form-row field-inner_content">',
            '<div>', # Обертка для табов и контента

            # 2. Табы-переключатели (вверху)
            '<div class="view-tabs">',
            '<button type="button" id="visual-tab" class="tab-btn active">Визуальный редактор</button>',
            '<button type="button" id="json-tab" class="tab-btn">JSON</button>',
            '</div>',

            # 3. Визуальный контейнер (Содержимое таба 1)
            '<div id="visual-widget-wrapper" class="tab-content active">',
            # ! steps-container будет Sortable. Добавляем класс drag-handle для перетаскивания.
            '<div id="steps-container" class="sortable-list">', 
        ]
        
        # 4. Рендеринг существующих шагов
        for i, step in enumerate(value):
            if "action" in step or "expected_result" in step:
                html.append(f"""
                    <div class="step-row" data-index="{i}">
                        <div class="step-fields">
                            <span class="drag-handle">::</span>
                            <input type="text" placeholder="Action" value="{step.get('action', '')}" />
                            <input type="text" placeholder="Expected result" value="{step.get('expected_result', '')}" />
                        </div>
                        <button type="button" class="remove-step">×</button>
                    </div>
                """)
            elif "comment" in step:
                html.append(f"""
                    <div class="step-row comment-row" data-index="{i}">
                        <div class="step-fields">
                            <span class="drag-handle">::</span>
                            <input type="text" placeholder="Comment" value="{step.get('comment', '')}" />
                        </div>
                        <button type="button" class="remove-step">×</button>
                    </div>
                """)
                
        html.append("</div>") # steps-container
        html.append("</div>") # visual-widget-wrapper

        # 5. JSON-редактор (textarea) (Содержимое таба 2)
        html.append(f"""
            <textarea name="{name}" id="id_{name}" rows="15" class="tab-content">{json_value}</textarea>
        """)

        # 6. Кнопки добавления (рядом с табами)
        html.append('<div class="step-controls" id="add-buttons-container">')
        # Используем стандартные классы Django Admin: .button и .default
        html.append('<button type="button" id="add-action" class="button default">+ Шаг</button>') 
        html.append('<button type="button" id="add-comment" class="button">+ Комментарий</button>') 
        html.append('</div>')
        
        # Закрытие оберток
        html.append("</div>") # Обертка для табов и контента
        html.append("</div>") # form-row

        return mark_safe("".join(html))

    # ... (value_from_datadict и deconstruct остаются прежними)
    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def deconstruct(self):
        name = f"{self.__class__.__module__}.{self.__class__.__name__}" 
        return (name, [], {})