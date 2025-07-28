<script setup>
import { ref, onMounted, computed } from 'vue'
import { useProjectStore } from '../../store/projectStore.js'
import { useRouter } from 'vue-router'

const props = defineProps({
  fullWidth: { type: Boolean, default: false },  // Will be true in TeamDetail
  showCreate: { type: Boolean, default: true },  // Will be false in TeamDetail
  teamId: { type: Number, default: -1 },
})

const projectStore = useProjectStore()
const router = useRouter()
const loading = ref(false)
const search = ref('')

// Projects filtered by search
const filteredProjects = computed(() => {
  const list = (props.fullWidth && props.teamId && projectStore.teamProjects.length)
    ? projectStore.teamProjects
    : projectStore.projects;
  return list.filter(project =>
    project.title?.toLowerCase().includes(search.value.toLowerCase()) ||
    project.description?.toLowerCase().includes(search.value.toLowerCase()) ||
    project.team_name?.toLowerCase().includes(search.value.toLowerCase())
  )
})

// The list of projects to display based on view mode
const displayedProjects = computed(() => {
  if (props.fullWidth && props.teamId && projectStore.teamProjects.length) {
    return projectStore.teamProjects
  }
  // If in general "Projects" page
  return projectStore.projects
})

onMounted(async () => {
  if (props.fullWidth && props.teamId > 0) {
    loading.value = true
    await projectStore.fetchProjectsByTeam(props.teamId)
    loading.value = false
  } else {
    loading.value = true
    await projectStore.fetchMyProjects()
    loading.value = false
  }
})

function goToDetail(projectId) {
  router.push({ name: 'ProjectDetail', params: { id: projectId } })
}

function getInitial(project) {
  return project.title ? project.title[0].toUpperCase() : 'P'
}
</script>

<template>
  <div :class="fullWidth ? 'w-full mx-auto min-h-[775px]' : 'max-w-5xl mx-auto max-h-[800px] mt-10 overflow-auto my-auto'">
    <div class="flex items-center justify-between mb-8 mt-3">
      <h2 :class="fullWidth ? 'text-3xl text-gray-700 font-bold' : 'text-3xl text-white font-bold'">Projects</h2>

      <input
        v-model="search"
        type="text"
        placeholder="Search projects..."
        class="px-3 py-2 rounded-xl border border-gray-300 text-gray-800 focus:outline-none"
      />
    </div>

    <div :class="fullWidth ? 'flex flex-col gap-4' : 'grid gap-6 sm:grid-cols-2 lg:grid-cols-3'">
      <div
        v-for="project in (search ? filteredProjects : displayedProjects)"
        :key="project.id"
        @click="goToDetail(project.id)"
        :class="[
          'cursor-pointer group bg-white rounded-2xl shadow-lg border border-gray-100 p-6 ml-2 flex flex-col transition hover:-translate-y-1 hover:shadow-2xl',
          fullWidth ? 'w-full' : ''
        ]"
      >
        <div class="flex items-center gap-3 mb-3">
          <div class="bg-gray-500 w-12 h-12 rounded-full flex items-center justify-center text-2xl font-bold text-white group-hover:bg-gray-900 group-hover:text-white transition">
            {{ getInitial(project) }}
          </div>
          <div>
            <div class="text-lg font-bold text-gray-600 group-hover:text-gray-900 transition">{{ project.title }}</div>
            <div class="text-xs text-gray-500">
              Team:
              <span class="font-semibold text-black">{{ project.team_name || '-' }}</span>
            </div>
          </div>
        </div>
        <div class="text-xs text-gray-400 mb-2 line-clamp-2">{{ project.description }}</div>
        <div class="flex-1"></div>
        <div class="mt-4 flex flex-wrap gap-2">
          <span class="inline-flex items-center bg-indigo-50 text-gray-600 px-2 py-1 rounded-full text-xs font-medium">
            <svg class="w-3 h-3 mr-1 text-gray-700" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10"/></svg>
            {{ project.task_count ?? 0 }} Tasks
          </span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-gray-400">Loading...</div>
    <div v-else-if="!filteredProjects.length && search" class="text-gray-400 italic mt-4">No projects found.</div>
  </div>
</template>
