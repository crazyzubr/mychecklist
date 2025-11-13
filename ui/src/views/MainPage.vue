<template>
  <div class="container">
    <div v-for="group in checklist" :key="group.priority.id" class="priority-group"
         @dragover="onDragOver" @drop="onDrop($event, group)">
      <div class="header">
        <AddChecklistItem
          :priorityId="group.priority.id"
          @itemAdded="item => group.items.unshift(item)"
        />
        <h2>{{ group.priority.name }} ({{ group.items.length }})</h2>
      </div>

      <ul class="checklist">
        <li
          v-for="item in group.items"
          :key="item.id"
          :class="{ completed: item.completed }"
          class="checklist-item"
          :data-id="item.id"
          draggable="true"
          @dragstart="onDragStart($event, item)"
        >
          <ChecklistCheckbox
            :itemId="item.id"
            v-model="item.completed"
            @toggled="handleToggle(item)"
          />
          <span>
            {{ item.text }}
            <em style="margin-left: 0.5rem;">{{ item.planned_date }}</em>
            <span v-if="item.percentage !== 0 && item.percentage !== 100" class="percentage">
              ({{ item.percentage }}%)
            </span>
          </span>
          <ChecklistEditButton :item="item" @updated="onItemUpdated" />
          <ChecklistArchivedButton :itemId="item.id" :itemName="item.text" @archived="onItemArchived" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AddChecklistItem from '../components/buttons/AddChecklistItemForm.vue'
import ChecklistCheckbox from '../components/buttons/ChecklistToggled.vue'
import ChecklistArchivedButton from '../components/buttons/ChecklistArchived.vue'
import ChecklistEditButton from '../components/buttons/ChecklistEdit.vue'

const checklist = ref([])

async function fetchChecklist() {
  try {
    const res = await fetch('/api/v1/checklist')
    if (res.ok) {
      const data = await res.json()
      console.log('Загруженные данные:', data)
      checklist.value = data
    }
  } catch (error) {
    console.error('Ошибка запроса чеклиста', error)
  }
}

onMounted(fetchChecklist)

function handleToggle(item) {
  // Логика обновления позиции item в списке в зависимости от item.completed
  const group = checklist.value.find(g => g.priority.id === item.priority)
  if (!group) return

  // Удаляем item из старой позиции
  group.items = group.items.filter(i => i.id !== item.id)

  if (item.completed) {
    // Перемещаем отмеченный элемент вниз (в конец массива)
    group.items.push(item)
  } else {
    // Если снят — наверх (начало массива)
    group.items.unshift(item)
  }
}

function onItemArchived(archivedItemId) {
  for (const group of checklist.value) {
    const index = group.items.findIndex(i => i.id === archivedItemId)
    if (index !== -1) {
      group.items.splice(index, 1)
      break
    }
  }
}

function onItemUpdated(updatedItem) {
  for (const group of checklist.value) {
    const index = group.items.findIndex(item => item.id === updatedItem.id)
    if (index !== -1) {
      // В Vue 3 достаточно заменить элемент по индексу - реактивность сохранится
      group.items[index] = updatedItem
      break
    }
  }
}

async function onDragEnd(evt) {
  try {
    const { item, to } = evt;
    if (!item || !to) return;

    // Получаем id элемента из dataset или reactive объекта, например:
    const draggedElementId = item.getAttribute('data-id');

    // Получаем приоритет колонки, куда положили элемент:
    const newPriorityId = to.getAttribute('data-priority-id');

    if (!draggedElementId || !newPriorityId) return;

    const res = await fetch('/api/v1/checklist/item/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: draggedElementId,
        priority: newPriorityId,
      }),
    });

    if (!res.ok) throw new Error('Ошибка перемещения');
  } catch (e) {
    console.error(e);
    alert('Ошибка перемещения');
  }
}

let draggedItem = null

function onDragStart(event, item) {
  draggedItem = item
  event.dataTransfer.setData('text/plain', item.id)
  event.dataTransfer.effectAllowed = 'move'
}

function onDragOver(event) {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
}

function onDrop(event, targetGroup) {
  event.preventDefault()
  if (!draggedItem) return

  const itemId = parseInt(event.dataTransfer.getData('text/plain'))
  const sourceGroup = checklist.value.find(g =>
    g.items.some(item => item.id === itemId)
  )

  if (sourceGroup && sourceGroup.priority.id !== targetGroup.priority.id) {
    const itemIndex = sourceGroup.items.findIndex(item => item.id === itemId)
    if (itemIndex !== -1) {
      const [movedItem] = sourceGroup.items.splice(itemIndex, 1)
      targetGroup.items.push(movedItem)

      // Вызываем API для сохранения
      onDragEnd({
        item: { getAttribute: () => movedItem.id.toString() },
        to: { getAttribute: () => targetGroup.priority.id.toString() }
      })
    }
  }

  draggedItem = null
}

</script>

<style scoped>
.container {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 0.5rem;
}
.priority-group {
  flex: 1 1 300px;
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.checklist {
  padding-inline-start: 0.25rem;
}
.draggable-item {
  display: inline;
}
.checklist-item {
  list-style: none;
  margin: 0.5rem 0;
  color: black;
  padding-left: 0;
  text-align: left;
}
.percentage {
  color: #747bff;
  margin-left: 0.5rem;
}
.checklist-item.completed {
  color: gray;
  text-decoration: line-through;
}

.checklist-item label {
  cursor: pointer;
}
.priority-columns {
  display: flex;
  gap: 1rem;
}
.priority-group {
  flex: 1;
  border: 1px solid #ccc;
  padding: 1rem;
}
.drag-handle {
  cursor: grab;
  margin-right: 0.5rem;
  font-style: italic;
  color: #555;
}
</style>