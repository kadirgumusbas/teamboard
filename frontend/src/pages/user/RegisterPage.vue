<script setup>
import {ref} from 'vue'
import {postRegister} from '../../services/userApi.js'
import {useRouter} from 'vue-router'

const form = ref({
  username: "",
  email: "",
  first_name: "",
  last_name: "",
  password: "",
  confirm_password: "",
  role:"guest",
})

const error = ref('')
const loading = ref(false)
const success = ref('')
const router = useRouter()

async function register() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    // Backend endpoint'ini kendi API'na göre düzenle
    const res = await postRegister(form.value)
    if (res.data) {
      success.value = 'Registration successful! You are being redirected to the login page...'
      setTimeout(() => {
        router.push('/login')
      }, 1000)
    } else {
      error.value = 'Unknown error! Try again.'
    }
  } catch (e) {
    // Backend'den gelen hata detayı varsa onu yaz, yoksa genel mesaj ver
    error.value = e.response?.data?.detail || 'Registration failed!'
  }
  loading.value = false
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
      <div class="flex">
        <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink">
          <rect width="40" height="40" fill="url(#pattern0_1_5993)"/>
          <defs>
            <pattern id="pattern0_1_5993" patternContentUnits="objectBoundingBox" width="1" height="1">
              <use xlink:href="#image0_1_5993" transform="scale(0.0113636)"/>
            </pattern>
            <image id="image0_1_5993" width="88" height="88" preserveAspectRatio="none"
                   xlink:href="data:image/png;base64,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"/>
          </defs>
        </svg>
        <h1 class="text-2xl font-bold mb-6 mt-1 ml-3 text-gray-800 dark:text-gray-100">TeamBoard</h1>
      </div>
      <form @submit.prevent="register" class="space-y-4">
        <input
            v-model="form.username"
            type="text"
            placeholder="Username"
            class="w-full px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
            required
        />
        <input
            v-model="form.email"
            type="email"
            placeholder="Email"
            class="w-full px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
            required
        />
        <div class="flex">
          <input
              v-model="form.first_name"
              type="text"
              placeholder="Name"
              class="w-full px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
              required
          />
          <input
              v-model="form.last_name"
              type="text"
              placeholder="Surname"
              class="w-full px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
              required
          />
        </div>
        <input
            v-model="form.password"
            type="password"
            placeholder="Password"
            class="w-full px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
            required
        />
        <input
            v-model="form.confirm_password"
            type="password"
            placeholder="Confirm Password"
            class="w-full px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
            required
        />
        <button
            type="submit"
            :disabled="loading"
            class="w-full py-2 rounded bg-gray-800 hover:bg-gray-900 text-white font-semibold transition disabled:opacity-50"
        >
          <span v-if="!loading">Register</span>
          <span v-else>Loading...</span>
        </button>
      </form>
      <div v-if="error" class="mt-4 text-red-500 text-center">{{ error }}</div>
      <div v-if="success" class="mt-4 text-green-500 text-center">{{ success }}</div>
      <div class="flex justify-between mt-6 text-sm">
        <router-link to="/login" class="text-gray-800 dark:text-gray-200 hover:underline">Login</router-link>
        <router-link to="/forgot-password" class="text-gray-800 dark:text-gray-200 hover:underline">I forgot my password
        </router-link>
      </div>
    </div>
  </div>
</template>
