<script setup>
import {onMounted, ref} from 'vue'
import TeamCreateForm from './TeamCreateForm.vue'
import {useTeamStore} from '../../store/teamStore.js'
import {useRouter} from 'vue-router'

const teamStore = useTeamStore()
const router = useRouter()
const showCreate = ref(false)
try {
  onMounted(() => {
    teamStore.loadTeams()
  })
} catch (error) {
  console.log(error)
}

function goToDetail(teamId) {
  router.push({name: 'TeamDetail', params: {id: teamId}})
}

function handleCreated() {
  showCreate.value = false
  teamStore.loadTeams()
}
</script>

<template>
  <div class="max-w-5xl mx-auto max-h-[800px] overflow-auto mt-10">
    <div class="flex items-center justify-between mb-8">
      <h2 class="text-3xl text-white font-bold">My Teams</h2>
      <button
          @click="showCreate = true"
          class="bg-gray-700 hover:bg-gray-900 px-5 py-2 rounded-xl text-white font-semibold shadow transition"
      >
        + Create Team
      </button>
    </div>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
          v-for="team in teamStore.teams"
          :key="team.id"
          @click="goToDetail(team.id)"
          class="cursor-pointer group bg-white rounded-2xl shadow-lg border border-gray-100 p-6 flex flex-col transition hover:-translate-y-1 hover:shadow-2xl"
      >
        <div class="flex items-center gap-3 mb-3">
          <div
              class="bg-gray-500 w-12 h-12 rounded-full flex items-center justify-center text-2xl font-bold text-white group-hover:bg-gray-900 group-hover:text-white transition">
            {{ team?.name[0] }}
          </div>
          <div>
            <div class="text-lg font-bold text-gray-600 group-hover:text-gray-900 transition">{{ team.name }}</div>
            <div class="text-xs text-gray-500">
              Owner:
              <span class="font-semibold text-black">{{ team.owner.username }}</span>
            </div>
          </div>
        </div>
        <div class="flex-1"></div>
        <div class="mt-4 flex flex-wrap gap-2">
          <span
              v-for="member in team.members?.slice(0, 3) || []"
              :key="member.id"
              class="inline-flex items-center bg-indigo-50 text-gray-600 px-2 py-1 rounded-full text-xs font-medium"
          >
            <svg class="w-3 h-3 mr-1 text-gray-700" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10"
                                                                                                      r="10"/></svg>
            {{ member.username }}
          </span>
          <span v-if="team.members && team.members.length > 3"
                class="text-xs text-gray-400 ml-2">+{{ team.members.length - 3 }} other</span>
        </div>
      </div>
    </div>
    <!-- Modal (takım oluşturma) -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-lg relative">
        <button @click="showCreate = false"
                class="absolute right-4 top-4 text-gray-400 hover:text-red-500 text-2xl font-bold">&times;
        </button>
        <TeamCreateForm @created="handleCreated" @cancel="showCreate = false"/>
      </div>
    </div>
  </div>
</template>
