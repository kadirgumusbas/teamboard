<script setup>
import { ref, onMounted } from 'vue'
import { useTaskStore } from '../../store/taskStore.js'
import { teamMembers } from "../../services/projectApi.js"

const props = defineProps({
  projectId: { type: Number, required: true },
})
const emit = defineEmits(['created', 'close'])

const title = ref('')
const description = ref('')
const assignee = ref(null)
const taskStore = useTaskStore()
const loading = ref(false)
const error = ref(null)
const members = ref([])

async function handleCreate() {
  loading.value = true
  error.value = null
  try {
    await taskStore.createTask(props.projectId, {
      title: title.value,
      description: description.value,
      assignee: assignee.value  // Pay attention to this!
    })
    emit('created')
    title.value = ''
    description.value = ''
    assignee.value = null
  } catch (err) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const res = await teamMembers(props.projectId)
  console.log('res', res)
  members.value = res.data
})
</script>

<template>
  <form
    @submit.prevent="handleCreate"
    class="w-full flex flex-col gap-5 rounded-2xl bg-gray-100 border border-gray-200 shadow-lg p-6"
  >
    <h3 class="text-xl font-semibold text-gray-800 mb-1">Add Task</h3>

    <input
      v-model="title"
      type="text"
      class="w-full px-4 py-3 rounded-xl bg-gray-200 focus:bg-white text-gray-800 border-none shadow-sm outline-none placeholder-gray-400 focus:ring-2 focus:ring-indigo-300 transition"
      placeholder="Task title"
      required
      autocomplete="off"
    />

    <textarea
      v-model="description"
      rows="3"
      class="w-full px-4 py-3 rounded-xl bg-gray-200 focus:bg-white text-gray-800 border-none shadow-sm outline-none placeholder-gray-400 focus:ring-2 focus:ring-indigo-300 transition"
      placeholder="Description (optional)"
      autocomplete="off"
    />

    <!-- Assignee Selection -->
    <div>
      <label for="assignee" class="block text-gray-700 font-medium mb-1">Assignee</label>
      <select
        v-model="assignee"
        id="assignee"
        class="w-full px-4 py-2 rounded-xl bg-gray-200 focus:bg-white text-gray-800 border-none shadow-sm outline-none focus:ring-2 focus:ring-indigo-300 transition"
        required
      >
        <option disabled value="">Select a member</option>
        <option
          v-for="member in members"
          :key="member.id"
          :value="member.id"
        >
          {{ member?.first_name }} {{ member.last_name }} ({{ member.username }})
        </option>
      </select>
    </div>

    <div class="flex justify-end gap-2 mt-2">
      <button
        type="button"
        @click="$emit('close')"
        class="px-5 py-2 rounded-xl bg-gray-300 hover:bg-gray-400 text-gray-700 font-semibold transition shadow-sm"
      >
        Cancel
      </button>
      <button
        :disabled="loading"
        type="submit"
        class="px-6 py-2 rounded-xl bg-gray-500 hover:bg-gray-600 text-white font-semibold transition shadow-md disabled:opacity-50"
      >
        {{ loading ? 'Adding...' : 'Add' }}
      </button>
    </div>

    <div v-if="error" class="text-red-500 text-sm mt-1 text-center">{{ error }}</div>
  </form>
</template>
