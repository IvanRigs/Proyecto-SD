import { createRouter, createWebHistory } from 'vue-router'

import Home from '../components/Home.vue'
import MovieDetails from '../components/MovieDetails.vue'
import Reservation from '../components/Reservation.vue'

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/movie',
    component: MovieDetails
  },
  {
    path: '/reservation',
    component: Reservation
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})