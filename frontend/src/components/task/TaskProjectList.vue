<script setup>
import { ref, onMounted, watch } from 'vue'
import { useTaskStore } from '../../store/taskStore.js'
import router from "../../router/index.js";

const props = defineProps({
  projectId: { type: [String, Number], required: false, default: null },
})

const taskStore = useTaskStore()
const loading = ref(false)

onMounted(async () => {
  if (props.projectId) {
    loading.value = true
    await taskStore.loadTasks(props.projectId)
    loading.value = false
  }
})

// Duruma göre renk döndüren yardımcı fonksiyon
function statusColor(status) {
  if (status === 'todo') return 'bg-gray-300 text-gray-700'
  if (status === 'in_progress') return 'bg-yellow-200 text-yellow-800'
  if (status === 'done') return 'bg-green-200 text-green-800'
  return 'bg-gray-100 text-gray-500'
}

function truncate(text, limit = 40) {
  if (!text) return ''
  return text.length > limit ? text.slice(0, limit) + '…' : text
}
function goToDetail(taskId) {
  router.push({ name: 'TaskDetail', params: { id: taskId } })
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-if="loading" class="text-gray-400 text-center">Loading...</div>
    <div v-else-if="!taskStore.tasks.length" class="text-gray-500 italic text-center">No missions yet.</div>
    <div v-else>
      <div
        v-for="task in taskStore.tasks.filter(task => task.project === props.projectId)"
        :key="task.id"
        class="m-2 bg-white rounded-2xl shadow-md border border-gray-200 px-5 py-4 flex flex-col gap-2 group hover:shadow-xl transition"
        @click="goToDetail(task.id)"
      >
        <div class="flex items-center justify-between">
          <h4 class="text-lg font-bold text-gray-800">{{ truncate(task.title) }}</h4>
          <!-- Status Badge -->
          <span
            :class="[
              'px-3 py-1 rounded-full text-xs font-semibold select-none border',
              statusColor(task.status)
            ]"
          >
            {{ task.status === 'todo' ? 'To Do'
              : task.status === 'in_progress' ? 'In Progress'
              : task.status === 'done' ? 'Done' : task.status }}
          </span>
        </div>
        <div class="text-gray-600 text-sm">{{ truncate(task.description) || 'Açıklama yok' }}</div>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-xs text-gray-400">Assigned:</span>
          <span class="text-sm font-medium text-gray-700">
            {{ task.assignee_username || 'Atanan yok' }}
          </span>
        </div>
        <div class="flex justify-end mt-1">
          <span class="text-xs text-gray-400">{{ new Date(task.created_at).toLocaleDateString('tr-TR') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
