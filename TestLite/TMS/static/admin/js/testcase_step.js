document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("steps-container");
    const visualWrapper = document.getElementById("visual-widget-wrapper");
    const textareaInput = document.getElementById("id_inner_content"); 
    
    // Элементы табов
    const visualTabBtn = document.getElementById("visual-tab");
    const jsonTabBtn = document.getElementById("json-tab");
    
    // Элементы управления
    const addButtonsContainer = document.getElementById("add-buttons-container"); 
    // Кнопки добавления не нужно искать, они будут созданы в Python, 
    // но нужно изменить их класс в HTML/CSS, чтобы они выглядели как .button
    const addStepBtn = document.getElementById("add-action");
    const addCommentBtn = document.getElementById("add-comment");

    // --- ВАЖНОЕ ИЗМЕНЕНИЕ: Добавляем классы Django Admin к кнопкам, 
    //     если они не были добавлены в Python (для безопасности)
    if (addStepBtn) {
        addStepBtn.classList.add('button', 'default'); 
        addStepBtn.classList.remove('add-btn'); 
    }
    if (addCommentBtn) {
        addCommentBtn.classList.add('button'); 
        addCommentBtn.classList.remove('add-btn'); 
    }

    if (!container || !textareaInput) return;

    let isVisualMode = true;

    // --- 1. СИНХРОНИЗАЦИЯ: Визуал -> JSON (TextArea)
    // ... (остается прежней)
    function syncVisualToTextarea() {
        if (!isVisualMode) return;
        const data = [];
        container.querySelectorAll(".step-row").forEach(row => {
            const action = row.querySelector("input[placeholder='Action']");
            const expected = row.querySelector("input[placeholder='Expected result']");
            const comment = row.querySelector("input[placeholder='Comment']");
            
            if (comment) {
                if (comment.value.trim() !== "") {
                    data.push({ comment: comment.value.trim() });
                }
            } else if (action && expected) {
                if (action.value.trim() !== "" || expected.value.trim() !== "") {
                    data.push({
                        action: action.value.trim(),
                        expected_result: expected.value.trim()
                    });
                }
            }
        });
        textareaInput.value = JSON.stringify(data, null, 2); 
    }

    // --- 2. СИНХРОНИЗАЦИЯ: JSON (TextArea) -> Визуал
    // ... (остается прежней)
    function syncTextareaToVisual() {
        try {
            const jsonValue = textareaInput.value.trim();
            const data = jsonValue ? JSON.parse(jsonValue) : []; 
            
            container.innerHTML = ""; 
            
            data.forEach(step => {
                if (step.comment !== undefined) {
                    createComment(step.comment);
                } else if (step.action !== undefined || step.expected_result !== undefined) {
                    createStep(step.action || "", step.expected_result || "");
                }
            });
            return true; 
        } catch (e) {
            console.error("Некорректный JSON:", e);
            alert("Ошибка: Некорректный JSON формат. Исправьте в JSON-редакторе перед переключением.");
            return false; 
        }
    }

    // --- 3. УПРАВЛЕНИЕ ТАБАМИ
    // ... (остается прежней)
    function activateVisualMode() {
        if (isVisualMode) return;
        
        const success = syncTextareaToVisual(); 
        if (success) {
            isVisualMode = true;
            visualTabBtn.classList.add("active");
            jsonTabBtn.classList.remove("active");
            visualWrapper.classList.add("active");
            textareaInput.classList.remove("active");
            addButtonsContainer.style.display = "block"; 
        }
    }

    function activateJsonMode() {
        if (!isVisualMode) return;
        
        syncVisualToTextarea(); 
        isVisualMode = false;
        jsonTabBtn.classList.add("active");
        visualTabBtn.classList.remove("active");
        visualWrapper.classList.remove("active");
        textareaInput.classList.add("active");
        addButtonsContainer.style.display = "none"; 
    }

    // --- 4. Вспомогательные функции (создание шагов)
    // ... (остаются прежними)
    function createStep(action = "", expected = "") {
        const row = document.createElement("div");
        row.className = "step-row";
        row.innerHTML = `
            <div class="step-fields">
                <span class="drag-handle">::</span>
                <input type="text" placeholder="Action" value="${action}" />
                <input type="text" placeholder="Expected result" value="${expected}" />
            </div>
            <button type="button" class="remove-step">×</button>
        `;
        container.appendChild(row);
    }

    function createComment(comment = "") {
        const row = document.createElement("div");
        row.className = "step-row comment-row";
        row.innerHTML = `
            <div class="step-fields">
                <span class="drag-handle">::</span>
                <input type="text" placeholder="Comment" value="${comment}" />
            </div>
            <button type="button" class="remove-step">×</button>
        `;
        container.appendChild(row);
    }

    // --- 5. ОБРАБОТЧИКИ СОБЫТИЙ И DRAG & DROP
    
    // Инициализация Drag and Drop
    if (typeof Sortable !== 'undefined') {
        new Sortable(container, {
            animation: 150,
            handle: '.drag-handle', 
            ghostClass: 'sortable-ghost',
            onEnd: function (evt) {
                syncVisualToTextarea(); 
            },
        });
    } else {
        console.warn("SortableJS не загружен. Drag & Drop не будет работать.");
    }
    
    // Обработчики табов
    visualTabBtn?.addEventListener("click", activateVisualMode);
    jsonTabBtn?.addEventListener("click", activateJsonMode);
    
    // Добавление новых шагов
    addStepBtn?.addEventListener("click", () => {
        createStep();
        syncVisualToTextarea();
    });
    addCommentBtn?.addEventListener("click", () => {
        createComment();
        syncVisualToTextarea();
    });

    // Изменение в визуальном режиме
    container.addEventListener("input", syncVisualToTextarea);
    
    // Удаление шагов
    container.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-step")) {
            e.target.closest(".step-row").remove();
            syncVisualToTextarea();
        }
    });

    // --- 6. ИНИЦИАЛИЗАЦИЯ
    syncTextareaToVisual(); 
    isVisualMode = true; 
    visualWrapper.classList.add("active");
    addButtonsContainer.style.display = "block"; 
});