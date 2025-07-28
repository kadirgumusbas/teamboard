<script setup>
import { ref } from 'vue'
import { useProjectStore } from '../../store/projectStore.js'

const props = defineProps({
  teamId: Number, // Passed as a prop because we are creating a project for a specific team
})
const emit = defineEmits(['created', 'close'])

const title = ref('')
const description = ref('')
const loading = ref(false)
const error = ref(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  try {
    await useProjectStore().createProject({
      title: title.value,
      description: description.value,
      is_active: true, // Default active; you can add a checkbox if you want to control it
      team: props.teamId,
    })
    emit('created')
  } catch (e) {
    error.value = 'Project could not be created!'
  }
  loading.value = false
}
</script>

<template>
  <div class="w-full max-w-md mx-auto bg-white rounded-xl shadow-xl p-6">
    <h2 class="text-xl font-bold mb-4">Add New Project</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label class="block text-gray-700 mb-1">Project Title</label>
        <input v-model="title" required class="border px-3 py-2 rounded w-full" />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 mb-1">Description</label>
        <textarea v-model="description" rows="3" class="border px-3 py-2 rounded w-full" />
      </div>
      <button
        type="submit"
        :disabled="loading"
        class="bg-gray-600 hover:bg-gray-700 disabled:bg-gray-300 transition px-7 py-3 rounded-xl text-white font-semibold shadow text-lg w-full md:w-auto"
      >
        {{ loading ? 'Creating...' : 'Create Project' }}
      </button>
      <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
    </form>
  </div>
</template>
