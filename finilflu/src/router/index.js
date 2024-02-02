import { createRouter, createWebHistory } from 'vue-router';
import MainDashboard from "@/views/MainDashboard.vue";
import MainAnalysis from '@/views/MainAnalysis.vue';
import MainMarkets from '@/views/MainMarkets.vue';

const routes = [
  {
    path: '/',
    name: 'MainDashboard',
    component: MainDashboard
  },
  {
    path: '/analysis',
    name: 'MainAnalysis',
    component: MainAnalysis
  },
  {
    path: '/markets',
    name: 'MainMarkets',
    component: MainMarkets
  },
  // Możesz dodać więcej ścieżek tutaj
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;