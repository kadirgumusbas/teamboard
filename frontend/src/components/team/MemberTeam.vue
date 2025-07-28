<script setup>
import { onMounted } from 'vue'
import { useTeamStore } from '../../store/teamStore.js'
import { useUserStore } from '../../store/userStore.js'

const teamStore = useTeamStore()
const userStore = useUserStore()

onMounted(() => {
  teamStore.loadTeams()
})
</script>

<template>
  <div class="max-w-4xl mx-auto mt-10">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">My Teams</h2>
    <div v-if="teamStore.teams.length" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="team in teamStore.teams.filter(t => t.members.some(m => m.id === userStore.user.id))"
        :key="team.id"
        class="bg-white rounded-xl shadow-md p-5"
      >
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 bg-indigo-200 text-indigo-700 rounded-full flex items-center justify-center font-bold text-xl">
            {{ team.name[0] }}
          </div>
          <div>
            <div class="text-lg font-semibold text-gray-700">{{ team.name }}</div>
            <div class="text-xs text-gray-500">Owner: {{ team.owner.username }}</div>
          </div>
        </div>
        <div class="flex flex-wrap gap-2 mt-2">
          <span v-for="member in team.members" :key="member.id" class="text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full">
            {{ member.username }}
          </span>
        </div>
      </div>
    </div>
    <div v-else class="text-gray-500 italic">You have no team.</div>
  </div>
</template>
