<script setup>
import { ref, onMounted } from 'vue'
import { useProjectStore } from '../../store/projectStore.js'
import { useUserStore } from '../../store/userStore.js'
import { useRoute } from 'vue-router'
import TaskCreateModal from '../task/TaskCreateModal.vue'
import ProjectEditForm from "./ProjectEditForm.vue";
import TaskProjectList from "../task/TaskProjectList.vue";

const projectStore = useProjectStore()
const userStore = useUserStore()
const route = useRoute()
const projectId = route.params.id

const showEditModal = ref(false)
const showAddTaskModal = ref(false)

onMounted(async () => {
  projectStore.selectedProject = null
  await projectStore.loadProjectDetail(projectId)
  console.log(projectStore.selectedProject.id)
})

function openEditModal() {
  showEditModal.value = true
}

function openAddTaskModal() {
  showAddTaskModal.value = true
}

function handleTaskAdded() {
  showAddTaskModal.value = false
  projectStore.loadProjectDetail(projectId)
}

function handleProjectUpdated() {
  showEditModal.value = false
  projectStore.loadProjectDetail(projectId)
}
</script>

<template>
  <div
    v-if="projectStore.selectedProject"
    class="w-full max-w-7xl mx-auto py-8 px-4 md:px-8 flex flex-col md:flex-row gap-8 bg-white rounded-2xl shadow-lg border"
  >
    <!-- Left: Project Details -->
    <div class="w-full md:w-2/3 min-h-[790px] flex flex-col gap-8">
      <div>
        <div class="flex items-center gap-3">
          <h2 class="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
            <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-600">
              <rect x="3" y="5" width="18" height="14" rx="2" stroke-width="2" />
            </svg>
            {{ projectStore.selectedProject.title }}
          </h2>
        </div>
        <p class="text-gray-500 mb-1">
          <span class="font-medium text-gray-700">Owner:</span>
          <span class="inline-flex items-center gap-1 bg-indigo-50 px-2 py-1 rounded text-gray-600 font-semibold">
            <svg width="16" height="16" fill="currentColor" class="inline"><circle cx="8" cy="8" r="8" /></svg>
            {{ projectStore.selectedProject.team_owner }}
          </span>
        </p>
        <p class="text-sm text-gray-400">
          Created: {{ new Date(projectStore.selectedProject.created_at).toLocaleDateString('en-US') }}
        </p>
        <div class="relative">
          <h3 class="text-lg font-semibold text-gray-700 mb-3 flex items-center justify-between">
            Description:
            <button
              v-if="userStore.user.id === projectStore.selectedProject.owner_id"
              @click="openEditModal"
              class="bg-gray-700 w-20 h-9 hover:bg-gray-900 text-white px-4 py-1.5 rounded-xl text-sm font-semibold shadow"
            >
              Edit
            </button>
          </h3>
        </div>
        <div class="flex flex-col gap-3 min-h-[614px] overflow-y-auto pr-2 border rounded-xl bg-gray-50 p-3">
          <p class="text-md text-gray-700 mt-4" v-if="projectStore.selectedProject.description">
            {{ projectStore.selectedProject.description }}
          </p>
        </div>
      </div>
      <!-- You can add more project-related info or dashboard sections here -->
    </div>

    <!-- Right: Task List -->
    <div class="w-full md:w-1/3">
      <div class="min-h-[790px] max-h-[790px] overflow-y-auto bg-gray-50 pr-2 border rounded-xl">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-semibold text-gray-700 mt-3 ml-2">Tasks</h3>
          <button
            v-if="userStore.user.id === projectStore.selectedProject.owner_id"
            @click="openAddTaskModal"
            class="mr-2 mt-3 bg-gray-700 hover:bg-gray-900 text-white px-4 py-1.5 rounded-xl shadow text-sm font-semibold flex items-center gap-1"
          >
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="inline-block mr-1 -mt-0.5">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Task
          </button>
        </div>
        <TaskProjectList :project-id="projectStore.selectedProject.id" />
      </div>
    </div>

    <!-- Edit Modal -->
    <transition name="fade">
      <div
        v-if="showEditModal"
        class="fixed inset-0 z-30 flex items-center justify-center bg-gradient-to-br from-gray-800/90 via-gray-900/80 to-gray-700/80 backdrop-blur-sm"
      >
        <div
          class="relative rounded-2xl border border-gray-700 shadow-2xl w-[95vw] max-w-lg min-w-[340px] min-h-[320px]
          bg-gradient-to-br from-gray-800 via-gray-900 to-gray-800
          flex flex-col justify-center items-center p-8
          ring-1 ring-gray-900/10"
          style="backdrop-filter: blur(8px);"
        >
          <button
            @click="showEditModal = false"
            class="absolute top-4 right-4 text-gray-400 hover:text-red-400 text-2xl font-bold focus:outline-none transition"
          >&times;</button>
          <div class="w-full">
            <ProjectEditForm
              :project="projectStore.selectedProject"
              @updated="handleProjectUpdated"
              @close="showEditModal = false"
            />
          </div>
        </div>
      </div>
    </transition>

    <!-- Add Task Modal -->
    <transition name="fade">
      <div
        v-if="showAddTaskModal"
        class="fixed inset-0 z-30 flex items-center justify-center bg-black bg-opacity-40"
      >
        <div
          class="relative bg-white rounded-2xl shadow-xl border w-[95vw] max-w-lg min-w-[340px] min-h-[280px] flex flex-col justify-center items-center p-8"
        >
          <button
            @click="showAddTaskModal = false"
            class="absolute top-4 right-4 text-gray-400 hover:text-red-600 text-2xl font-bold focus:outline-none"
          >&times;</button>
          <TaskCreateModal
            :project-id="projectStore.selectedProject.id"
            @created="handleTaskAdded"
            @close="showAddTaskModal = false"
          />
        </div>
      </div>
    </transition>
  </div>
</template>
