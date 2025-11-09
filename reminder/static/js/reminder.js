// Переменная для текущего перетаскиваемого элемента
    let draggedItem = null;

    function renderChecklistItem(data){
      return `
            <span class="item-index"></span>
            <input type="checkbox" class="complete-checkbox" ${data.completed ? 'checked' : ''}>
            <span class="item-text">${data.text}</span>
            <span class="item-date" data-date="${data.planned_date}">${new Date(data.planned_date).toLocaleDateString('ru-RU', {day: 'numeric', month: 'long', year: 'numeric'})}</span>
            <span class="item-percentage item-percentage-${data.percentage}" data-percentage="${data.percentage}">(${data.percentage}%)</span>
            <span class="edit-btn" title="Редактировать">✏️</span>
            <span class="remove-btn" title="Удалить">✖</span>
          `;
    }

    function attachDragAndDropListeners(itemDiv) {
      itemDiv.addEventListener('dragstart', e => {
        draggedItem = itemDiv;
        itemDiv.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', itemDiv.dataset.id);
        setTimeout(() => itemDiv.style.display = 'none', 0);
      });

      itemDiv.addEventListener('dragend', e => {
        if(draggedItem) {
          draggedItem.classList.remove('dragging');
          draggedItem.style.display = 'flex';
          draggedItem = null;
        }
      });
    }

    document.querySelectorAll('.items').forEach(container => {
      container.addEventListener('dragover', e => {
        e.preventDefault();
        container.classList.add('drop-target');
      });

      container.addEventListener('dragleave', () => {
        container.classList.remove('drop-target');
      });

        container.addEventListener('drop', e => {
          e.preventDefault();
          container.classList.remove('drop-target');

          const draggedId = e.dataTransfer.getData('text/plain');
          const draggedElem = document.querySelector(`.item[data-id='${draggedId}']`);
          if (!draggedElem) return;

          const oldContainer = draggedElem.parentNode;

          container.appendChild(draggedElem);
          sortItemsByCompleted(container);
          sortItemsByCompleted(oldContainer);
          updateIndices();
          updateEmptyMessage(container);
          updateEmptyMessage(oldContainer);

          const newPriorityId = container.closest('.column').dataset.priorityId;
          const newOrder = Array.from(container.children).indexOf(draggedElem);

          fetch('/api/checklist/item/move', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ id: draggedId, priority: newPriorityId, order: newOrder }),
          });
        });
    });

    function sortItemsByCompleted(container) {
      const itemsArray = Array.from(container.querySelectorAll('.item'));
      itemsArray.sort((a, b) => {
        const aCompleted = a.classList.contains('completed') ? 1 : 0;
        const bCompleted = b.classList.contains('completed') ? 1 : 0;
        return aCompleted - bCompleted;  // 0 (false) идет перед 1 (true)
      });
      itemsArray.forEach(item => container.appendChild(item));
    }


    function updateEmptyMessage(container) {
      if (!container) return;
      const emptyMsg = container.querySelector('.empty-message');
      if (!emptyMsg) return;
      const itemsCount = container.querySelectorAll('.item').length;
      emptyMsg.style.display = itemsCount === 0 ? 'block' : 'none';
    }

    function updateIndices() {
      document.querySelectorAll('.column').forEach(column => {
        const items = column.querySelectorAll('.item');
        items.forEach((item, i) => {
          const indexSpan = item.querySelector('.item-index');
          if (indexSpan) indexSpan.textContent = (i + 1) + '.';
        });
      });
    }

    // Инициализация после загрузки
    window.addEventListener('load', () => {
      document.querySelectorAll('.items').forEach(updateEmptyMessage);
      updateIndices();
    });

document.querySelectorAll('.add-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const col = btn.closest('.column');
    const priorityLevel = parseInt(col.dataset.priorityLevel, 10);

    // Получаем поле дата в форме
    const dateInput = col.querySelector('.date-input');

    // Заполняем поле даты по уровню
    if (priorityLevel === 0) {
        // Получаем сегодняшнюю дату в формате yyyy-mm-dd
        const today = new Date();
        const todayStr = today.toISOString().split('T')[0];
      dateInput.value = todayStr;
    } else if (priorityLevel === 1) {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const tomorrowStr = tomorrow.toISOString().split('T')[0];
      dateInput.value = tomorrowStr;
    } else {
      dateInput.value = ''; // Оставляем пустым
    }

    btn.style.display = 'none';
    col.querySelector('.add-form').style.display = 'block';
  });
});


document.querySelectorAll('.cancel-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const col = btn.closest('.column');
    col.querySelector('.add-form').style.display = 'none';
    col.querySelector('.add-btn').style.display = 'inline-block';
  });
});

document.querySelectorAll('.save-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const col = btn.closest('.column');
    const priorityId = col.dataset.priorityId;
    const textInput = col.querySelector('.text-input');
    const dateInput = col.querySelector('.date-input');
    const percentageInput = col.querySelector('.progress-input');
    const text = textInput.value.trim();
    const planned_date = dateInput.value;
    const percentage = percentageInput.value || 0;
    if (!text || !planned_date) {
      alert('Заполните все поля');
      return;
    }

    fetch('/api/checklist/item', {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({text, planned_date, priority: priorityId, percentage: percentage})
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      addItemToColumn(col, data);
      textInput.value = '';
      dateInput.value = '';
      col.querySelector('.add-form').style.display = 'none';
      col.querySelector('.add-btn').style.display = 'inline-block';
        updateIndices();
    });
  });
});

function addItemToColumn(column, item) {
  const itemsDiv = column.querySelector('.items');
  const div = document.createElement('div');

  // Добавляем класс 'item' и, если выполнено, добавляем 'completed'
  div.classList.add('item');
  if (item.completed) {
    div.classList.add('completed');
  }

  div.setAttribute('draggable', 'true');
  div.dataset.id = item.id;

  div.innerHTML = renderChecklistItem(item)

  // Вставляем в начало списка, как и раньше (можно по необходимости менять на append)
  itemsDiv.prepend(div);

  attachItemEventListeners(div);
}


function attachItemEventListeners(itemDiv) {
  const checkbox = itemDiv.querySelector('.complete-checkbox');
  checkbox.addEventListener('change', () => {
    const id = itemDiv.dataset.id;
    fetch(`/api/checklist/item/${id}/toggle_completed`, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')}
    })
    .then(response => response.json())
    .then(data => {
      if (data.completed) {
        itemDiv.classList.add('completed');
      } else {
        itemDiv.classList.remove('completed');
      }
      moveItemWithinColumn(itemDiv);
        updateIndices();
    });
  });

  const removeBtn = itemDiv.querySelector('.remove-btn');
  removeBtn.addEventListener('click', () => {
    if (!confirm('Вы уверены, что хотите удалить элемент?')) return;
    const id = itemDiv.dataset.id;
    fetch(`/api/checklist/item/${id}/archive`, {
      method: 'POST',
      headers: {'X-CSRFToken': getCookie('csrftoken')}
    }).then(response => response.json())
      .then(data => {
        if (data.archived) {
          itemDiv.remove();
            updateIndices();
        }
      });
  });

  const editBtn = itemDiv.querySelector('.edit-btn');
    editBtn.addEventListener('click', () => {
     startEditingItem(itemDiv);
    });
}

function startEditingItem(itemDiv) {
  // Отключаем перетаскивание
    itemDiv.removeAttribute('draggable');
    itemDiv.ondragstart = e => e.preventDefault();

    const text = itemDiv.querySelector('.item-text').textContent.trim();
    const date = itemDiv.querySelector('.item-date').dataset.date; // ISO
    const percentage = itemDiv.querySelector('.item-percentage').dataset.percentage;

    itemDiv.innerHTML = `
    <span class="item-index"></span>
    <input type="text" class="edit-text-input" value="${text}" style="flex:1;">
    <input type="date" class="edit-date-input" value="${date}">
    <input type="number" class="edit-progress-input" value="${percentage}">
    <button class="edit-save-btn">Сохранить</button>
    <button class="edit-cancel-btn">Отмена</button>
    `;

    updateIndices();

  itemDiv.querySelector('.edit-save-btn').addEventListener('click', () => {
    const newText = itemDiv.querySelector('.edit-text-input').value.trim();
    const newDate = itemDiv.querySelector('.edit-date-input').value;
    const newPercentage = itemDiv.querySelector('.edit-progress-input').value;

    if (!newText || !newDate) {
      alert('Пожалуйста, заполните оба поля');
      return;
    }

    const id = itemDiv.dataset.id;
    fetch(`/api/checklist/item/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({text: newText, planned_date: newDate, percentage: newPercentage})
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      // Восстанавливаем draggable и drag события
      itemDiv.setAttribute('draggable', 'true');
      itemDiv.ondragstart = null;
      itemDiv.innerHTML = renderChecklistItem(data)
      attachItemEventListeners(itemDiv);
      attachDragAndDropListeners(itemDiv);
      updateIndices();
    });
  });

  itemDiv.querySelector('.edit-cancel-btn').addEventListener('click', () => {
    const id = itemDiv.dataset.id;
    fetch(`/api/checklist/item/${id}`, {
      headers: {'X-CSRFToken': getCookie('csrftoken')}
    })
    .then(response => response.json())
    .then(data => {
      itemDiv.setAttribute('draggable', 'true');
      itemDiv.ondragstart = null;
    itemDiv.innerHTML = renderChecklistItem(data)
      attachItemEventListeners(itemDiv);
      attachDragAndDropListeners(itemDiv);
      updateIndices();
    });
  });
}
function moveItemWithinColumn(itemDiv) {
  const column = itemDiv.closest('.column');
  const itemsDiv = column.querySelector('.items');
  itemDiv.remove();
  if (itemDiv.classList.contains('completed')) {
    itemsDiv.appendChild(itemDiv);
  } else {
    itemsDiv.prepend(itemDiv);
  }
}

document.querySelectorAll('.item').forEach(item => {
  attachItemEventListeners(item);
  attachDragAndDropListeners(item);
});
// Получить CSRF токен
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}