<script setup>
import {ref} from 'vue'
import {useTeamStore} from '../../store/teamStore.js'
import UserSelectList from './UserSelectList.vue'
import {useUserStore} from '../../store/userStore.js'

const userStore = useUserStore()
const teamStore = useTeamStore()
const name = ref('')
const selectedUserIds = ref([])
const loading = ref(false)
const error = ref(null)
const emit = defineEmits(['created', 'cancel'])

async function handleSubmit() {
  loading.value = true
  error.value = null
  try {
    const teamData = {
      name: name.value,
      member_ids: selectedUserIds.value,
    }
    await teamStore.createTeam(teamData)
    emit('created')
  } catch (e) {
    error.value = 'Failed to create team!'
  }
  loading.value = false
}
</script>

<template>
  <div class="bg-white p-6 rounded shadow max-w-md mx-auto">
    <h2 class="text-xl font-bold mb-4">Create Team</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label class="block text-gray-700">Team Name</label>
        <input v-model="name" required class="border p-2 rounded w-full"/>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">Members</label>
        <UserSelectList v-model="selectedUserIds"
                        :exclude-ids="[userStore.user?.id]"/>
      </div>
      <button type="submit" :disabled="loading" class="bg-gray-800 text-white px-4 py-2 rounded">
        {{ loading ? 'Creating...' : 'Create' }}
      </button>
      <button type="button" @click="$emit('cancel')" class="ml-2 px-4 py-2 rounded border">
        Cancel
      </button>
      <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
    </form>
  </div>
</template>
