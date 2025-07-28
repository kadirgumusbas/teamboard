<script setup>
import {ref, onMounted} from 'vue'
import {useTeamStore} from '../../store/teamStore.js'
import {useUserStore} from '../../store/userStore.js'
import {useRoute} from 'vue-router'
import TeamMemberAdd from './TeamMemberAdd.vue'
import ProjectCreateModal from '../project/ProjectCreateModal.vue'
import ProjectList from "../project/ProjectList.vue";

const teamStore = useTeamStore()
const userStore = useUserStore()
const route = useRoute()
const teamId = route.params.id
const showAddModal = ref(false)
const addMode = ref('member') // veya 'project'

function openAddModal(mode = 'member') {
  addMode.value = mode
  showAddModal.value = true
}

onMounted(() => {
  teamStore.selectedTeam = null
  teamStore.loadTeamDetail(teamId)
})

function getInitials(user) {
  if (user.first_name && user.last_name)
    return (user.first_name[0] + user.last_name[0]).toUpperCase()
  if (user.username)
    return user.username.slice(0, 2).toUpperCase()
  return "U"
}

async function handleRemove(memberId) {
  await teamStore.removeMember(teamStore.selectedTeam.id, memberId)
  await teamStore.loadTeamDetail(teamId)
}

async function handleAdd(userId) {
  await teamStore.addMember(teamStore.selectedTeam.id, userId)
  await teamStore.loadTeamDetail(teamId)
  showAddModal.value = false
}


</script>

<template>
  <div
      v-if="teamStore.selectedTeam"
      class="w-full max-h-[850px] max-w-7xl mx-auto py-8 px-4 md:px-8 flex flex-col md:flex-row gap-8 bg-white rounded-2xl shadow-lg border">
    <div class="w-full md:w-2/3 min-h-[400px] flex flex-col gap-8">
      <!-- Takım Bilgisi -->
      <div>
        <h2 class="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-2">
          <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-600">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a4 4 0 00-3-3.87M9 20h6M5 20h1a4 4 0 013-3.87M9 20V9a4 4 0 118 0v11M5 20v-2a4 4 0 013-3.87"/>
          </svg>
          {{ teamStore.selectedTeam.name }}
        </h2>
        <p class="text-gray-500 mb-1">
          <span class="font-medium text-gray-700">Owner:</span>
          <span class="inline-flex items-center gap-1 bg-indigo-50 px-2 py-1 rounded text-gray-600 font-semibold">
            <svg width="16" height="16" fill="currentColor" class="inline"><circle cx="8" cy="8" r="8"/></svg>
            {{ teamStore.selectedTeam.owner.username }}
          </span>
        </p>
        <p class="text-sm text-gray-400">
          Created: {{ new Date(teamStore.selectedTeam.created_at).toLocaleDateString('tr-TR') }}
        </p>
      </div>
      <!-- Üye Listesi -->
      <div class="relative">
        <h3 class="text-lg font-semibold text-gray-700 mb-3 flex items-center justify-between">
          Team Members
          <button
              v-if="userStore.user?.id === teamStore.selectedTeam.owner?.id"
              @click="openAddModal()"
              class="bg-gray-700 hover:bg-gray-900 text-white px-4 py-1.5 rounded-xl shadow text-sm font-semibold"
          >
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                 class="inline-block mr-1 -mt-0.5">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 4v16m8-8H4"/>
            </svg>
            Add
          </button>
        </h3>
        <div
            v-if="teamStore.selectedTeam.members.length"
            class=" max-h-[614px] flex flex-col gap-3 min-h-[614px] overflow-y-auto pr-2 border rounded-xl bg-gray-50 p-3"
            style="scrollbar-gutter: stable;"
        >
          <div
              v-for="member in teamStore.selectedTeam.members"
              :key="member.id"
              class="flex items-center gap-3 p-3 bg-white rounded-xl shadow-sm"
              :class="member.id === teamStore.selectedTeam.owner.id ? 'border border-gray-400 bg-gray-200' : ''"
          >
            <div
                class="w-10 h-10 rounded-full bg-gray-500 flex items-center justify-center font-bold text-white text-xl"
            >
              {{ getInitials(member) }}
            </div>
            <div>
              <div class="font-medium text-gray-800">{{ member.first_name }} {{ member.last_name }}</div>
              <div class="text-xs text-gray-500">{{ member.username }}</div>
            </div>
            <span
                v-if="member.id === teamStore.selectedTeam.owner.id"
                class="text-xs bg-gray-500 text-white px-2 py-0.5 rounded-md ml-auto"
            >
              Owner
            </span>
            <button
                v-else-if="userStore.user?.id === teamStore.selectedTeam.owner?.id"
                @click="handleRemove(member.id)"
                class="ml-auto bg-red-100 hover:bg-red-600 hover:text-white text-red-600 px-3 py-1 rounded-md text-xs font-semibold shadow transition"
            >
              <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                   class="inline-block align-middle -mt-1">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"/>
              </svg>
              Remove
            </button>
          </div>
        </div>
        <div v-else class="text-gray-400 text-sm italic">There are no members yet.</div>
      </div>
    </div>
    <div class="w-full md:w-1/3">
      <div class="max-h-[790px] overflow-y-auto bg-gray-50 pr-2 border rounded-xl">
        <ProjectList :teamId="teamStore.selectedTeam.id" :fullWidth="true" :showCreate="false"/>
      </div>
    </div>
    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-30 flex items-center justify-center bg-black bg-opacity-40">
        <div
            class="relative bg-white rounded-2xl shadow-xl border w-[95vw] max-w-2xl min-w-[340px] min-h-[500px] flex flex-col justify-center items-center p-8">
          <button
              @click="showAddModal = false"
              class="absolute top-4 right-4 text-gray-400 hover:text-red-600 text-2xl font-bold focus:outline-none"
          >&times;
          </button>
          <!-- Tab veya başlık -->
          <div class="flex gap-2 mb-4">
            <button
                :class="addMode === 'member' ? 'bg-gray-600 text-white' : 'bg-gray-100 text-gray-700'"
                class="px-4 py-1 rounded"
                @click="addMode = 'member'">
              Add Member
            </button>
            <button
                :class="addMode === 'project' ? 'bg-gray-600 text-white' : 'bg-gray-100 text-gray-700'"
                class="px-4 py-1 rounded"
                @click="addMode = 'project'">
              Add Project
            </button>
          </div>
          <TeamMemberAdd
              v-if="addMode === 'member'"
              :team="teamStore.selectedTeam"
              @added="handleAdd"
          />
          <ProjectCreateModal
              v-else
              :team-id="teamStore.selectedTeam.id"
              @created="() => { showAddModal = false; /* Proje listesini yenile */ }"
              @close="showAddModal = false"
          />
        </div>
      </div>
    </transition>


  </div>
</template>

<style scoped>
</style>
