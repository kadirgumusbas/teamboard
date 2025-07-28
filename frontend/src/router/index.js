// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/user/ProfilePage.vue'),
    meta: { breadcrumb: 'Anasayfa' }
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../pages/project/ProjectPage.vue'),
    meta: { breadcrumb: 'Projeler' }
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: () => import('../components/project/ProjectDetail.vue'),
    meta: {
      breadcrumb: route => `Proje #${route.params.id}`  // ister sabit, ister dinamik!
    }
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../pages/task/TaskPage.vue'),
    meta: { breadcrumb: 'Görevler' }
  },
  {
    path: '/tasks/:id',
    name: 'TaskDetail',
    component: () => import('../components/task/TaskDetail.vue'),
    meta: {
      breadcrumb: route => `Görev #${route.params.id}`
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/user/LoginPage.vue'),
    meta: { breadcrumb: 'Giriş Yap' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/user/RegisterPage.vue'),
    meta: { breadcrumb: 'Kayıt Ol' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../pages/user/ProfilePage.vue'),
    meta: { breadcrumb: 'Profilim' }
  },
  {
    path: '/teams',
    name: 'Teams',
    component: () => import('../pages/team/TeamPage.vue'),
    meta: { breadcrumb: 'Takımlar' }
  },
  {
    path: '/teams/:id',
    name: 'TeamDetail',
    component: () => import('../pages/team/TeamDetailPage.vue'),
    meta: {
      breadcrumb: route => `Takım #${route.params.id}`
    }
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
