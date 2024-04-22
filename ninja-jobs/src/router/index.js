import { createRouter, createWebHistory } from 'vue-router'

import MainDashboard from '../views/MainDashboard.vue'
import MainDescription from '../views/MainDescription.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainDashboard
  },
 
  {
    path: '/description',
    name: 'description',
    component: MainDescription
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
