<script setup>
import { ref, watch, onMounted } from 'vue'
import { useProjectStore } from '../../store/projectStore.js'
import { useRouter } from 'vue-router'

const props = defineProps({
  open: Boolean,
})
const emit = defineEmits(['close'])

const projectStore = useProjectStore()
const router = useRouter()
const expandedTeamIds = ref([])

onMounted(async () => {
  await projectStore.loadMyTeamsWithProjects()
})

function toggleTeam(teamId) {
  expandedTeamIds.value.includes(teamId)
      ? expandedTeamIds.value = expandedTeamIds.value.filter(id => id !== teamId)
      : expandedTeamIds.value.push(teamId)
}

function goToTeam(teamId) {
  emit('close')
  router.push({ name: 'TeamDetail', params: { id: teamId } })
}
function goToProject(projectId) {
  emit('close')
  router.push({ name: 'ProjectDetail', params: { id: projectId } })
}
function goToTask(taskId) {
  emit('close')
  router.push({ name: 'TaskDetail', params: { id: taskId } })
}
</script>

<template>
  <transition name="slide">
    <aside
      v-if="open"
      class="fixed top-0 left-0 z-40 h-screen w-[260px] bg-gray-900 shadow-2xl border-r border-gray-800 transition-all duration-300
        flex flex-col gap-4"
      style="will-change: transform"
    >
      <!-- Kapat tuşu -->
      <button
        @click="emit('close')"
        class="absolute top-4 right-4 text-gray-400 hover:text-red-400 text-2xl font-bold"
        aria-label="Kapat"
      >&times;</button>
      <h2 class="text-lg font-bold text-white mt-6 mb-3 px-6 tracking-wide">Teams & Projects</h2>
      <ul class="flex-1 overflow-y-auto pr-2">
        <li
          v-for="team in projectStore.teamsWithProjects"
          :key="team.id"
          class="mb-2"
        >
          <div
            class="flex items-center justify-between cursor-pointer px-3 py-2 rounded hover:bg-gray-800 font-semibold text-gray-100"
          >
            <div
              class="flex items-center gap-2 flex-1"
              @click="goToTeam(team.id)"
              title="Go to team"
            >
              <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-400">
                <circle cx="12" cy="12" r="10" stroke-width="2"/>
              </svg>
              <span>{{ team.name }}</span>
            </div>
            <button @click="toggleTeam(team.id)" class="ml-2">
              <svg :class="{ 'rotate-90': expandedTeamIds.includes(team.id) }"
                   class="w-5 h-5 text-gray-400 transition-transform"
                   fill="none" stroke="currentColor" stroke-width="2"
                   viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
          <ul
            v-if="expandedTeamIds.includes(team.id)"
            class="ml-6 mt-1 border-l-2 border-gray-700 pl-2"
          >
            <li
              v-for="project in team.projects"
              :key="project.id"
              class="flex items-center justify-between cursor-pointer text-sm text-gray-200 hover:bg-gray-800 rounded px-2 py-1"
            >
              <span @click="goToProject(project.id)" class="flex-1">{{ project.title }}</span>
              <button @click="goToProject(project.id)" class="ml-1">
                <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-400">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </button>
            </li>
            <li v-if="!team.projects.length" class="text-gray-500 italic text-xs pl-2 py-1">No projects</li>
          </ul>
        </li>
      </ul>
    </aside>
  </transition>
</template>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s cubic-bezier(.4,2,.3,1), opacity 0.2s;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
.slide-enter-to, .slide-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>
