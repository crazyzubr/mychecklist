<template>
  <div class="checklist-by-dates">
    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <div v-for="groupBlock in checklistByDates" :key="groupBlock.group.id" class="group-block">
        <h2>{{ groupBlock.group.name }}</h2>
        <div class="columns">
          <template v-for="column in groupBlock.columns" :key="column.priority.id">
            <div v-if="column.items.length" class="column">
              <div class="header">
                <AddChecklistItem
                  :priorityId="column.priority.id"
                  @itemAdded="item => column.items.unshift(item)"
                />
                <h3>{{ column.priority.name }} ({{ column.items.length }})</h3>
              </div>
              <ul>
                <li v-for="item in column.items" :key="item.id" class="checklist-item" :class="{ completed: item.completed }">
                  <div>
                    <ChecklistCheckbox
                      :itemId="item.id"
                      v-model="item.completed"
                      @toggled="handleToggle(item)"
                    />
                    {{ item.text }}
                    <em style="margin-left: 0.5rem;">{{ item.planned_date }}</em>
                    <span v-if="item.percentage !== 0 && item.percentage !== 100" class="percentage">
                      ({{ item.percentage }}%)
                    </span>
                    <ChecklistEditButton :item="item" @updated="onItemUpdated" />
                    <ChecklistArchivedButton :itemId="item.id" :itemName="item.text" @archived="onItemArchived" />
                  </div>
                </li>
              </ul>
            </div>
          </template>
        </div>
      </div>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AddChecklistItem from '../components/buttons/AddChecklistItemForm.vue'
import ChecklistCheckbox from '../components/buttons/ChecklistToggled.vue'
import ChecklistArchivedButton from "../components/buttons/ChecklistArchived.vue";
import ChecklistEditButton from '../components/buttons/ChecklistEdit.vue'

const checklistByDates = ref([])
const loading = ref(false)
const error = ref(null)

async function fetchChecklistByDates() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch('/api/v1/checklist/by-dates')
    if (!res.ok) throw new Error('Ошибка при загрузке данных')
    checklistByDates.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchChecklistByDates()
})


function handleToggle(item) {
  for (const groupBlock of checklistByDates.value) {
    for (const column of groupBlock.columns) {
      const itemIndex = column.items.findIndex(i => i.id === item.id);
      if (itemIndex !== -1) {
        const completed = column.items[itemIndex].completed
        column.items = column.items.filter(i => i.id !== item.id)
        if (completed) {
          column.items.push(item)
        } else {
          column.items.unshift(item)
        }
        return;
      }
    }
  }
}

function onItemUpdated(updatedItem) {
  for (const groupBlock of checklistByDates.value) {
    for (const column of groupBlock.columns) {
      const itemIndex = column.items.findIndex(i => i.id === updatedItem.id);
      if (itemIndex !== -1) {
        column.items[itemIndex] = updatedItem
        return;
      }
    }
  }
}

function onItemArchived(archivedItemId) {
  for (const groupBlock of checklistByDates.value) {
    for (const column of groupBlock.columns) {
      const itemIndex = column.items.findIndex(i => i.id === archivedItemId);
      if (itemIndex !== -1) {
        column.items.splice(itemIndex, 1)
        return;
      }
    }
  }
}

</script>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 0.5rem;
}

.checklist-by-dates {
  padding: 1rem;
  min-width: 1920px;
}

.group-block {
  margin-bottom: 2rem;
}

.columns {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.column {
  flex: 1 1 200px;
  border: 1px solid #ccc;
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #fafafa;
  max-width: 600px;

  ul {
    list-style: none;
    text-align: left;
  }
}

.checklist-item {
  margin-bottom: 0.5rem;

  &.completed {
    color: gray;
    text-decoration: line-through;
  }
}

.percentage {
  color: #666;
  margin-left: 0.3rem;
  font-style: italic;
}

.error {
  color: red;
  margin-top: 1rem;
}

</style>
