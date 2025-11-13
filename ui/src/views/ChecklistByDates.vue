<template>
  <div class="checklist-by-dates">
    <h1>Чеклист по датам</h1>
    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <div v-for="groupBlock in checklistByDates" :key="groupBlock.group.id" class="group-block">
        <h2>{{ groupBlock.group.name }}</h2>
        <div class="columns">
          <template v-for="column in groupBlock.columns" :key="column.priority.id">
            <div v-if="column.items.length" class="column">
              <h3>{{ column.priority.name }}</h3>
              <ul>
                <li v-for="item in column.items" :key="item.id" class="checklist-item">
                  <div>
                    {{ item.text }}
                    <em style="margin-left: 0.5rem;">{{ item.planned_date }}</em>
                    <span v-if="item.percentage !== 0 && item.percentage !== 100" class="percentage">
                      ({{ item.percentage }}%)
                    </span>
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
// import AddChecklistItem from '../components/buttons/AddChecklistItemForm.vue'
// import ChecklistCheckbox from '../components/buttons/ChecklistToggled.vue'
// import ChecklistArchivedButton from '../components/buttons/ChecklistArchived.vue'
// import ChecklistEditButton from '../components/buttons/ChecklistEdit.vue'

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
</script>

<style scoped>
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
}
.column ul {
  list-style: none;
  text-align: left;
}
.checklist-item {
  margin-bottom: 0.5rem;
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
