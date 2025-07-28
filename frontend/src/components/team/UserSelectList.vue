<script setup>
import {ref, computed, onMounted} from 'vue'
import axios from 'axios'

const props = defineProps({
  modelValue: Array,
  excludeIds: {type: Array, default: () => []},
})
const emit = defineEmits(['update:modelValue'])

const users = ref([])
const search = ref('')

onMounted(async () => {
  const token = localStorage.getItem('accessToken')
  const res = await axios.get('http://localhost:8000/users/', {
    headers: {Authorization: `Bearer ${token}`}
  })
  users.value = res.data
})

const filteredUsers = computed(() => {
  const query = search.value.toLowerCase()
  return users.value
      .filter(user => !props.excludeIds.includes(user.id))
      .filter(
          user =>
              user.first_name.toLowerCase().includes(query) ||
              user.last_name.toLowerCase().includes(query) ||
              user.username.toLowerCase().includes(query)
      )
})

function toggleUser(id) {
  let selected = [...(props.modelValue || [])]
  if (selected.includes(id)) {
    selected = selected.filter(uid => uid !== id)
  } else {
    selected.push(id)
  }
  emit('update:modelValue', selected)
}

function getInitials(user) {
  if (user.first_name && user.last_name)
    return (user.first_name[0] + user.last_name[0]).toUpperCase()
  if (user.username)
    return user.username.slice(0, 2).toUpperCase()
  return "U"
}
</script>

<template>
  <div>
    <input
        v-model="search"
        type="text"
        placeholder="Search for users..."
        class="border px-4 py-2 rounded-xl mb-3 w-full outline-none focus:border-gray-500 transition bg-gray-50 shadow-sm"
    />
    <div class="max-h-72 overflow-y-auto border rounded-2xl p-2 bg-white shadow-inner">
      <div v-if="filteredUsers.length">
        <div
            v-for="user in filteredUsers"
            :key="user.id"
            @click="toggleUser(user.id)"
            class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer group transition hover:bg-gray-50 mb-1
    border border-transparent"
            :class="props.modelValue && props.modelValue.includes(user.id)
    ? 'bg-gray-100 border-gray-400 shadow'
    : ''"
        >
          <!-- Avatar/Initials -->
          <div class="w-10 h-10 rounded-full bg-gray-500 flex items-center justify-center font-bold text-white text-xl">
            {{ getInitials(user) }}
          </div>
          <div class="flex flex-col">
    <span class="font-semibold text-gray-800 text-base">
      {{ user.first_name }} {{ user.last_name }}
    </span>
            <span class="text-xs text-gray-500">@{{ user.username }}</span>
          </div>
          <div class="ml-auto flex items-center">
            <input
                type="checkbox"
                class="accent-gray-600 w-5 h-5 rounded border border-gray-300 focus:ring-2 focus:ring-gray-500"
                :checked="props.modelValue && props.modelValue.includes(user.id)"
                @click.stop="toggleUser(user.id)"
            />
          </div>
        </div>
      </div>
      <div v-else class="flex flex-col items-center py-6 text-gray-400 select-none">
        <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24" class="mb-2">
          <circle cx="12" cy="12" r="10" stroke-width="1.5"/>
          <path stroke-width="1.5"
                d="M8 10h.01M16 10h.01M9 16c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3z"/>
        </svg>
        User not found
      </div>
    </div>
  </div>
</template>
