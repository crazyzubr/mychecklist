import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import ChecklistByDatesPage from '../views/ChecklistByDates.vue'

const routes = [
  { path: '/', name: 'Main', component: MainPage },
  { path: '/by-dates', name: 'ChecklistByDatesPage', component: ChecklistByDatesPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
