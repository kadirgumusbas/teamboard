<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useTaskStore } from '../../store/taskStore.js'
import { useRouter } from 'vue-router'

const props = defineProps({
  projectId: { type: [String, Number], required: false }
})
const taskStore = useTaskStore()
const router = useRouter()

// Hangi kartta inline edit açık? id'sini tutalım
const editingTaskId = ref(null)
const editingStatus = ref(null)

const filteredTasks = computed(() =>
  props.projectId
    ? taskStore.tasks.filter(task => task.project === props.projectId)
    : taskStore.tasks
)

onMounted(() => {
  taskStore.loadUserTasks()
})

watch(() => props.projectId, (newId) => {
  if (newId) taskStore.loadUserTasks()
})

function statusBadge(status) {
  switch (status) {
    case 'todo': return 'bg-gray-300 text-gray-700 border-gray-400'
    case 'in_progress': return 'bg-yellow-200 text-yellow-800 border-yellow-400'
    case 'done': return 'bg-green-200 text-green-800 border-green-500'
    default: return 'bg-gray-100 text-gray-500 border-gray-200'
  }
}
function statusText(status) {
  switch (status) {
    case 'todo': return 'To Do'
    case 'in_progress': return 'In Progress'
    case 'done': return 'Done'
    default: return status
  }
}

function openStatusEdit(task) {
  editingTaskId.value = task.id
  editingStatus.value = task.status
}

async function saveStatus(task) {
  if (editingStatus.value !== task.status) {
    await taskStore.updateTask(task.id, { status: editingStatus.value })
    await taskStore.loadUserTasks() // Güncel taskları çek
  }
  editingTaskId.value = null
}

// Detaya yönlendir
function goToDetail(taskId) {
  router.push({ name: 'TaskDetail', params: { id: taskId } })
}
</script>

<template>
  <div class="flex justify-center">
    <div class="w-full max-w-5xl mx-auto flex flex-col gap-5 py-8">
      <h2 class="text-2xl font-bold text-white text-center mb-2 tracking-tight">My Tasks</h2>
      <div class="flex flex-col gap-4 min-h-[260px]">
        <div v-if="taskStore.loading" class="text-gray-400 text-center">Loading...</div>
        <div v-else-if="!filteredTasks.length" class="text-gray-500 italic text-center">No missions yet.</div>
        <div v-else>
          <div
            v-for="task in filteredTasks"
            :key="task.id"
            class="mb-3 rounded-2xl bg-white border flex items-center px-6 py-5 shadow group hover:shadow-2xl hover:border-gray-400 hover:bg-indigo-50/40 transition-all cursor-pointer relative gap-5"
            style="min-height:78px"
            @click="goToDetail(task.id)"
          >
            <!-- Güncelle butonu sağ üstte -->
            <button
              @click.stop="openStatusEdit(task)"
              class="absolute top-3 right-4 px-3 py-1 rounded-lg bg-gray-200 hover:bg-gray-400 text-gray-700 font-semibold text-xs shadow transition z-10"
              title="Update task status"
            >
              Durum
            </button>

            <div class="flex-1 pr-4">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-lg font-semibold text-gray-800">
                  {{ task.title.length > 30 ? task.title.slice(0, 30) + '…' : task.title }}
                </span>
                <span
                  :class="[
                    'ml-2 px-2 py-0.5 text-xs font-bold rounded-full border',
                    statusBadge(task.status)
                  ]"
                >{{ statusText(task.status) }}</span>
              </div>
              <div class="text-sm text-gray-500">
                {{ task.description?.length > 108 ? task.description.slice(0, 108) + '…' : (task.description || 'No description') }}
              </div>
            </div>
            <div class="flex flex-col items-end justify-between min-w-[85px] h-full pt-2">
              <div class="text-xs text-gray-400">
                {{ new Date(task.created_at).toLocaleDateString('tr-TR') }}
              </div>
            </div>
            <!-- Inline status update -->
            <transition name="fade">
              <div
                v-if="editingTaskId === task.id"
                class="absolute top-12 right-8 bg-white border rounded-xl shadow-lg p-4 z-20 flex flex-col gap-2 min-w-[160px]"
                @click.stop
              >
                <label class="text-xs font-semibold text-gray-700 mb-1">Select Status:</label>
                <select
                  v-model="editingStatus"
                  class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-gray-200 text-gray-700"
                >
                  <option value="todo">To Do</option>
                  <option value="in_progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
                <div class="flex justify-end gap-2 mt-2">
                  <button
                    @click.stop="editingTaskId = null"
                    class="px-3 py-1 bg-gray-100 rounded-lg hover:bg-gray-200 text-gray-700 text-xs font-semibold"
                  >Cancel</button>
                  <button
                    @click.stop="saveStatus(task)"
                    class="px-4 py-1 bg-gray-500 hover:bg-gray-600 text-white rounded-lg text-xs font-semibold transition"
                  >Save</button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
``
