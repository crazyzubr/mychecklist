<template>
  <div class="edit-container">
    <button class="edit-btn" @click="openForm" title="Редактировать">
      ✏️
    </button>

    <div v-if="showForm" class="popup-overlay" @click.self="closeForm">
      <div class="popup">
        <h3>Редактирование пункта</h3>
        <form @submit.prevent="submitEdit">
          <div>
            <label>Текст пункта</label>
            <input v-model="form.text" required />
          </div>
          <div>
            <label>Дата планирования</label>
            <input type="date" v-model="form.planned_date" required />
          </div>
          <div>
            <label>Процент выполнения</label>
            <input type="number" v-model.number="form.percentage" min="0" max="100" required />
          </div>
          <div>
            <button type="submit">Сохранить</button>
            <button type="button" @click="closeForm">Отмена</button>
          </div>
        </form>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  }
})

const emit = defineEmits(['updated'])

const showForm = ref(false)
const errorMessage = ref('')
const form = ref({
  text: '',
  planned_date: '',
  percentage: 0,
})

function openForm() {
  form.value = {
    text: props.item.text,
    planned_date: props.item.planned_date,
    percentage: props.item.percentage,
  }
  errorMessage.value = ''
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  errorMessage.value = ''
}

async function submitEdit() {
  try {
    const response = await fetch(`/api/v1/checklist/item/${props.item.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form.value, priority: props.item.priority }),
    })
    if (!response.ok) {
      const err = await response.text()
      errorMessage.value = 'Ошибка: ' + err
      return
    }
    const updatedItem = await response.json()
    emit('updated', updatedItem)
    closeForm()
  } catch (e) {
    errorMessage.value = 'Ошибка сети: ' + e.message
  }
}
</script>

<style scoped>
.edit-container {
  display: inline;
}
.edit-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #666;
  transition: color 0.3s;
  padding: 0 0.3rem;
}
.edit-btn:hover {
  color: #333;
}

.popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 6px;
  min-width: 600px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

.popup form div {
  margin-bottom: 1rem;
}

.popup label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.popup input {
  width: 100%;
  padding: 0.3rem 0.5rem;
  box-sizing: border-box;
}

.error {
  color: red;
  margin-top: 0.5rem;
}
</style>
