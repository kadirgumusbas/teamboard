<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTaskStore } from '../../store/taskStore'
import { useUserStore } from '../../store/userStore'
import { teamMembers } from '../../services/projectApi'

const route = useRoute()
const props = defineProps({
  taskId: String,
})
let taskId = route.params.id

const taskStore = useTaskStore()
const userStore = useUserStore()

const loading = ref(false)
const members = ref([])
const editMode = ref(false)
const error = ref(null)
const updateLoading = ref(false)

// Editable fields for update
const editTitle = ref('')
const editDesc = ref('')
const editStatus = ref('')
const editAssignee = ref(null)
const editDueDate = ref('')

const task = computed(() => taskStore.selectedTask)

// Fetch task details on mount
onMounted(async () => {
  if (props.value) {
    taskId = props.taskId
  }

  loading.value = true
  try {
    await taskStore.loadTaskDetail(taskId)
    // Do not set task.value directly here!
    // Fill editable fields below
    editTitle.value = task.value?.title || ''
    editDesc.value = task.value?.description || ''
    editStatus.value = task.value?.status || 'todo'
    editAssignee.value = task.value?.assignee || null
    editDueDate.value = task.value?.due_date || ''
    if (isOwnerOrAdmin.value && task.value?.project) {
      const res = await teamMembers(task.value.project)
      members.value = res.data
    }
  } catch (e) {
    error.value = 'Task not found.'
  } finally {
    loading.value = false
  }
})

// Authorization check (admin or team owner?)
const isOwnerOrAdmin = computed(() =>
  userStore.user?.role === 'admin' || userStore.user?.id === task.value?.owner_id
)

const assigneeUsername = computed(() => {
  if (!task.value?.assignee_username) return 'Unassigned'
  return task.value.assignee_username
})

async function handleUpdate() {
  updateLoading.value = true
  error.value = null
  try {
    await taskStore.updateTask(task.value.id, {
      title: editTitle.value,
      description: editDesc.value,
      status: editStatus.value,
      assignee: editAssignee.value,
      due_date: editDueDate.value,
    })
    editMode.value = false
    await taskStore.loadTaskDetail(taskId)
    task.value = taskStore.selectedTask
  } catch (err) {
    error.value = 'Update failed.'
  } finally {
    updateLoading.value = false
  }
}
</script>

<template>
  <div class="w-full max-w-2xl mx-auto mt-10 bg-white rounded-2xl shadow-2xl border px-8 py-8">
    <div v-if="loading" class="text-center text-gray-400">Loading...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-2xl font-bold text-gray-800">Task Detail</h2>
        <button
          v-if="isOwnerOrAdmin && !editMode"
          @click="editMode = true"
          class="px-4 py-1.5 bg-gray-200 hover:bg-gray-300 rounded-xl text-gray-700 font-semibold text-sm transition"
        >
          Edit
        </button>
        <button
          v-if="editMode"
          @click="editMode = false"
          class="px-4 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-xl text-gray-500 font-semibold text-sm ml-2 transition"
        >
          Cancel
        </button>
      </div>

      <!-- Edit Mode (Only Admin/Owner) -->
      <form v-if="editMode && isOwnerOrAdmin" @submit.prevent="handleUpdate" class="flex flex-col gap-5 mt-2">
        <div>
          <label class="text-sm font-semibold text-gray-700 mb-1 block">Title</label>
          <input
            v-model="editTitle"
            type="text"
            class="w-full px-3 py-2 rounded-xl border border-gray-300 bg-gray-50 focus:bg-white text-gray-800 shadow-sm"
          />
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 mb-1 block">Description</label>
          <textarea
            v-model="editDesc"
            rows="2"
            class="w-full px-3 py-2 rounded-xl border border-gray-300 bg-gray-50 focus:bg-white text-gray-800 shadow-sm"
          ></textarea>
        </div>
        <div class="flex gap-3">
          <div class="flex-1">
            <label class="text-sm font-semibold text-gray-700 mb-1 block">Status</label>
            <select
              v-model="editStatus"
              class="w-full px-3 py-2 rounded-xl border border-gray-300 bg-gray-50 text-gray-800"
            >
              <option value="todo">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="text-sm font-semibold text-gray-700 mb-1 block">Assignee</label>
            <select
              v-model="editAssignee"
              class="w-full px-3 py-2 rounded-xl border border-gray-300 bg-gray-50 text-gray-800"
            >
              <option disabled value="">Select</option>
              <option v-for="user in members" :key="user.id" :value="user.id">
                {{ user.first_name }} {{ user.last_name }} ({{ user.username }})
              </option>
            </select>
          </div>
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 mb-1 block">Due Date</label>
          <input
            v-model="editDueDate"
            type="date"
            class="w-full px-3 py-2 rounded-xl border border-gray-300 bg-gray-50 text-gray-800"
          />
        </div>
        <div class="flex justify-end gap-3">
          <button
            type="submit"
            :disabled="updateLoading"
            class="px-6 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition disabled:opacity-60"
          >
            {{ updateLoading ? 'Saving...' : 'Save' }}
          </button>
        </div>
        <div v-if="error" class="text-red-400 text-sm mt-1">{{ error }}</div>
      </form>

      <!-- Read-Only Mode (Member) -->
      <div v-else class="mt-1 flex flex-col gap-5">
        <div>
          <div class="text-sm text-gray-500 mb-1">Title</div>
          <div class="text-lg font-bold text-gray-800">{{ task?.title }}</div>
        </div>
        <div>
          <div class="text-sm text-gray-500 mb-1">Description</div>
          <div class="text-base text-gray-700">{{ task?.description || 'No description' }}</div>
        </div>
        <div class="flex gap-8 mt-2">
          <div>
            <div class="text-xs text-gray-400 mb-1">Status</div>
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-semibold select-none border',
                task?.status === 'todo'
                  ? 'bg-gray-200 text-gray-700 border-gray-400'
                  : task?.status === 'in_progress'
                  ? 'bg-yellow-100 text-yellow-800 border-yellow-400'
                  : task?.status === 'done'
                  ? 'bg-green-100 text-green-800 border-green-500'
                  : 'bg-gray-100 text-gray-500 border-gray-200'
              ]"
            >
              {{
                task?.status === 'todo'
                  ? 'To Do'
                  : task?.status === 'in_progress'
                  ? 'In Progress'
                  : task?.status === 'done'
                  ? 'Done'
                  : task?.status
              }}
            </span>
          </div>
          <div>
            <div class="text-xs text-gray-400 mb-1">Assignee</div>
            <div class="text-sm font-medium text-gray-700">
              {{ assigneeUsername }}
            </div>
          </div>
          <div>
            <div class="text-xs text-gray-400 mb-1">Due Date</div>
            <div class="text-sm text-gray-600">
              {{ task?.due_date ? new Date(task.due_date).toLocaleDateString('en-US') : '-' }}
            </div>
          </div>
        </div>
        <div class="text-xs text-gray-400 mt-4 text-right">
          Created at: {{ new Date(task?.created_at).toLocaleString('en-US') }}
        </div>
      </div>
    </div>
  </div>
</template>
