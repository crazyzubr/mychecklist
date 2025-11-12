<template>
  <div class="add-button-container">
    <button class="plus-btn" @click="showModal = true">+</button>

    <div v-if="showModal" class="popup-overlay" @click.self="close">
      <div class="popup">
        <form @submit.prevent="submit">
          <h3>Новый пункт</h3>
          <input v-model="text" placeholder="Текст пункта" required />
          <input type="date" v-model="planned_date" required />
          <input type="number" v-model.number="percentage" min="0" max="100" required />
          <button type="submit">Добавить</button>
          <button type="button" @click="close">Отмена</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  priorityId: Number
})
const emit = defineEmits(['itemAdded'])

const showModal = ref(false)
const text = ref('')
const planned_date = ref('')
const percentage = ref(0)

const close = () => {
  showModal.value = false
  // очистка данных
  text.value = ''
  planned_date.value = ''
  percentage.value = 0
}

const submit = async () => {
  const body = {
    text: text.value,
    planned_date: planned_date.value,
    percentage: percentage.value,
    priority: props.priorityId
  }

  const response = await fetch('/api/v1/checklist/item', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })

  if (response.ok) {
    const newItem = await response.json()
    emit('itemAdded', newItem)
    close()
  } else {
    alert('Ошибка при добавлении')
  }
}
</script>

<style scoped>
.plus-btn {
  background: #42b883;
  color: white;
  border: none;
  border-radius: 10%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  text-align: center;
  padding: 0;
}

.popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup {
  background: white;
  padding: 20px;
  border-radius: 4px;
}
</style>
