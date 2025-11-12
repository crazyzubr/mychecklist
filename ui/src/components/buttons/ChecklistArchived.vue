<template>
  <div class="archive-container">
    <button class="archive-btn" @click="showConfirm = true" title="Архивировать">
      ✖
    </button>

    <div v-if="showConfirm" class="popup-overlay" @click.self="showConfirm = false">
      <div class="popup">
        <p>Вы уверены, что хотите архивировать пункт &laquo;{{ itemName }}&raquo;?</p>
        <div class="buttons">
          <button @click="archiveItem" class="confirm-btn">Да</button>
          <button @click="showConfirm = false" class="cancel-btn">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  itemId: {
    type: Number,
    required: true,
  },
  itemName: {
    type: String,
    required: true,
  }
})

const emit = defineEmits(['archived'])

const showConfirm = ref(false)

async function archiveItem() {
  try {
    const res = await fetch(`/api/v1/checklist/item/${props.itemId}/archive`, { method: 'POST' })
    if (!res.ok) throw new Error('Ошибка архивирования')
    emit('archived', props.itemId)
    showConfirm.value = false
  } catch {
    alert('Ошибка при архивации. Попробуйте позже.')
  }
}
</script>

<style scoped>
.archive-container {
  display: inline;
}
.archive-btn {
  background: transparent;
  border: none;
  color: #999;
  font-size: 1.2em;
  cursor: pointer;
  transition: color 0.3s;
  padding: 0 0.2rem;
}
.archive-btn:hover {
  color: #666;
}

.popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.popup {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 6px;
  max-width: 300px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}

.buttons {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

.confirm-btn {
  background-color: #e53e3e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #eee;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.cancel-btn:hover {
  background-color: #ddd;
}
</style>
