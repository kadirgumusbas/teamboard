<script setup>
import {ref, onMounted} from 'vue'
import {getProfile} from '../../services/userApi.js'
import * as api from "../../services/userApi.js";
import ProfileField from "../../components/user/ProfileField.vue";

const profile = ref({
  username: '',
  email: '',
  created_at: '',
  first_name: '',
  last_name: '',
  role: '',
})
const editing = ref({}) // alan bazlı edit state
const message = ref('')

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await getProfile()
    Object.assign(profile.value, res.data)
  } catch (e) {
    error.value = 'Profile information could not be retrieved!'
  }
  loading.value = false
})

function editField(field) {
  editing.value[field] = true
}

// Editi kapatmak
function cancelEdit(field) {
  editing.value[field] = false
}

// Kaydetmek
async function saveField(field) {
  try {
    const data = {[field]: profile.value[field]}
    const res = await api.postProfiles(data)
    Object.assign(profile.value, res.data)
    message.value = 'Updated'
    setTimeout(() => message.value = '', 1200)
    editing.value[field] = false
  } catch (e) {
    error.value = 'Could not save'
    setTimeout(() => error.value = '', 1200)
  }
}
</script>

<template>
  <div class="min-h-screen mt-8">
    <div class="max-w-xl mx-auto dark:bg-gray-700 rounded-2xl shadow-lg p-8">
      <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">Profile Information</h2>

      <div class="space-y-4">
        <!-- Username (readonly) -->
        <ProfileField
            label="Username"
            v-model="profile.username"
            readonly
            icon="user"
        />

        <!-- Email (readonly) -->
        <ProfileField
            label="Email"
            v-model="profile.email"
            readonly
            icon="mail"
        />

        <!-- Created at (readonly) -->
        <ProfileField
            label="Created Date"
            v-model="profile.created_at"
            readonly
            icon="calendar"
        />

        <!-- First Name -->
        <ProfileField
            label="Name"
            v-model="profile.first_name"
            :editing="editing.first_name"
            @edit="editField('first_name')"
            @cancel="cancelEdit('first_name')"
            @save="saveField('first_name')"
            icon="user"
        />

        <!-- Last Name -->
        <ProfileField
            label="Surname"
            v-model="profile.last_name"
            :editing="editing.last_name"
            @edit="editField('last_name')"
            @cancel="cancelEdit('last_name')"
            @save="saveField('last_name')"
            icon="user"
        />

        <!-- Ekstra alanlar eklenebilir -->
      </div>

      <!-- Bildirimler -->
      <div v-if="message" class="mt-4 text-green-600 font-bold">{{ message }}</div>
      <div v-if="error" class="mt-4 text-red-600 font-bold">{{ error }}</div>
    </div>
  </div>
</template>
