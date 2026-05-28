import { createRouter, createWebHistory } from 'vue-router'

import Home from '../components/Home.vue'
import MovieDetails from '../components/MovieDetails.vue'

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/movie',
    component: MovieDetails
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})