<template>
  <input
    type="checkbox"
    :checked="modelValue"
    @change="onChange"
  />
</template>

<script setup>
const props = defineProps({
  modelValue: Boolean,
  itemId: Number,
})

const emit = defineEmits(['update:modelValue', 'toggled'])

async function onChange(event) {
  const checked = event.target.checked
  emit('update:modelValue', checked)
  try {
    const res = await fetch(`/api/v1/checklist/item/${props.itemId}/toggle_completed`, {
      method: 'POST',
    })
    if (!res.ok) throw new Error(`Ошибка ${res.status}`)
    emit('toggled', checked)
  } catch (e) {
    console.error(e)
    // можно откатить изменение состояния, если нужно
    emit('update:modelValue', !checked)
    alert('Ошибка при переключении статуса')
  }
}
</script>
