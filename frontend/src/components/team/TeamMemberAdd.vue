<script setup>
import { ref, watch } from 'vue'
import UserSelectList from './UserSelectList.vue'
const props = defineProps({ team: Object })
const emit = defineEmits(['added'])

const selectedUserIds = ref([])

watch(
  () => props.team.members,
  () => { selectedUserIds.value = [] }
)

async function handleAdd() {
  for (const userId of selectedUserIds.value) {
    emit('added', userId)
  }
  selectedUserIds.value = []
}
</script>

<template>
  <div class="w-full min-h-80 mx-auto bg-gray-50 p-8 rounded-2xl border shadow-xl max-w-2xl">
    <label class="block font-bold text-xl text-gray-700 mb-4 tracking-tight">Add Member to Team</label>
    <div class="flex flex-col md:flex-row gap-4 items-stretch">
      <div class="flex-1">
        <UserSelectList
          v-model="selectedUserIds"
          :exclude-ids="[...props.team.members.map(m => m.id), props.team.owner.id]"
        />
      </div>
      <div class="flex items-end">
        <button
          @click="handleAdd"
          :disabled="!selectedUserIds.length"
          class="bg-gray-600 hover:bg-gray-700 disabled:bg-gray-300 transition px-7 py-3 rounded-xl text-white font-semibold shadow text-lg w-full md:w-auto"
        >
          <span class="inline-flex items-center gap-2">
            <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="inline-block">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 4v16m8-8H4" />
            </svg>
            Add
          </span>
        </button>
      </div>
    </div>
  </div>
</template>
