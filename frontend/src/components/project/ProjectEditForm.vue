<script setup>
import { ref } from 'vue'
import { useProjectStore } from '../../store/projectStore.js'

const props = defineProps({
  project: { type: Object, required: true }
})
const emit = defineEmits(['updated', 'close'])
const projectStore = useProjectStore()

const title = ref(props.project.title)
const description = ref(props.project.description || '')
const loading = ref(false)
const error = ref(null)

async function handleUpdate() {
  loading.value = true
  error.value = null
  try {
    await projectStore.updateProject(props.project.id, {
      title: title.value,
      description: description.value
    })
    emit('updated')
  } catch (err) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleUpdate" class="w-full flex flex-col gap-4">
    <h3 class="text-xl font-semibold mb-3 text-gray-200">Edit Project</h3>

    <input
      v-model="title"
      type="text"
      class="w-full px-3 py-2 rounded-xl bg-gray-800 text-gray-100 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 transition"
      placeholder="Project title"
      required
    />

    <textarea
      v-model="description"
      class="w-full px-3 py-2 rounded-xl bg-gray-800 text-gray-100 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600 transition"
      placeholder="Description"
      rows="4"
    />

    <div class="flex justify-end gap-2">
      <button
        type="button"
        @click="$emit('close')"
        class="px-4 py-2 rounded-xl border border-gray-600 text-gray-300 bg-gray-700 hover:bg-gray-600 transition font-medium"
      >
        Cancel
      </button>
      <button
        :disabled="loading"
        type="submit"
        class="px-4 py-2 rounded-xl border border-gray-700 bg-gray-700 text-gray-200 hover:bg-gray-600 hover:text-white transition font-semibold disabled:opacity-70 disabled:cursor-not-allowed"
      >
        Save
      </button>
    </div>

    <div v-if="error" class="text-red-400 text-sm">{{ error }}</div>
  </form>
</template>
