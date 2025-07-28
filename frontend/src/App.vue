<script setup>
import TopNavbar from "./components/navbar/TopNavbar.vue";
import { useUserStore } from "./store/userStore.js";
import { computed, ref } from "vue";
import LeftNavbar from "./components/navbar/LeftNavbar.vue";

const userStore = useUserStore();
const isLogin = computed(() => userStore.accessToken || userStore.refreshToken);
const showLeftNav = ref(false);

function toggleLeftNav() {
  showLeftNav.value = !showLeftNav.value;
}
</script>

<template>
  <div class="flex flex-col bg-gray-900 min-h-screen relative">
    <TopNavbar v-if="isLogin" @toggle-left-nav="toggleLeftNav" />
    <LeftNavbar v-if="isLogin" :open="showLeftNav" @close="toggleLeftNav" />
    <main class="flex-1 bg-gray-900">
      <router-view/>
    </main>
  </div>
</template>
