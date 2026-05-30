<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

import { Carousel } from 'bootstrap'

import Navbar from './Navar.vue'
import FooterPag from './FooterPag.vue'

const router = useRouter()

function showMediaDetails(obj) {
  localStorage.setItem('obj', JSON.stringify(obj))
  router.push('/movie')
}

const apiKey = '0a5fdb3d67479033813279d6d5550f58'
const sessionId = localStorage.getItem('sessionId')

const topPeliculas = ref([])
const backdrops = ref([])
const imgPATH = ref('')
const tieneImagen = ref(false)

const cine = ref([])

const logout = ref(false)
const estaLogeado = ref(false)

const peliculasCarrusel = ref([])

function mostrarBotonCerrar() {
  logout.value = !logout.value
}

function cerrarSession() {
  localStorage.clear()
  window.location.href = '/'
}

function verificarSesion() {
  estaLogeado.value = sessionId !== null
}

async function obtenerCine() {
  const url = `https://api.themoviedb.org/3/movie/now_playing?api_key=${apiKey}&language=es-ES&page=1&region=MX`
  const response = await fetch(url)
  const data = await response.json()

  cine.value = data.results || []

  peliculasCarrusel.value = cine.value
    .filter(pelicula => pelicula.backdrop_path)
    .slice(0, 5)

  console.log('carrusel:', peliculasCarrusel.value.length)
}

async function obtenerPerfilUsuario() {
  if (!sessionId) return

  const url = `https://api.themoviedb.org/3/account?session_id=${sessionId}&api_key=${apiKey}`
  const response = await fetch(url)
  const data = await response.json()

  if (data?.avatar?.gravatar?.hash) {
    imgPATH.value = `https://secure.gravatar.com/avatar/${data.avatar.gravatar.hash}.jpg?s=64`
    tieneImagen.value = true
  } else {
    tieneImagen.value = false
  }
}

onMounted(async () => {
  verificarSesion()
  await obtenerCine()
  await obtenerPerfilUsuario()

  await nextTick()

  const carouselElement = document.getElementById('carouselExampleSlidesOnly')

  if (carouselElement) {
    const carousel = new Carousel(carouselElement, {
      interval: 6000,
      ride: 'carousel',
      pause: false,
      wrap: true,
      touch: true
    })

    carousel.cycle()
  }

  const navbar = document.querySelector('.contenedor-navbar')

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scroll')
    } else {
      navbar.classList.remove('scroll')
    }
  })
})
</script>

<template>
  <div>
    <div class="contenedor-principal">
      <!-- Navbar -->
      <Navbar />

      <!-- Banner -->
      <div class="banner-cont">

        <div v-if="peliculasCarrusel.length > 0" class="banner">
          <div
            id="carouselExampleSlidesOnly"
            class="carousel slide"
            data-bs-ride="carousel"
            data-bs-interval="2000"
          >
            <div class="carousel-inner">
              <div
                v-for="(pelicula, index) in peliculasCarrusel"
                :key="pelicula.id"
                class="carousel-item"
                :class="{ active: index === 0 }"
              >
                <img
                  :src="`https://image.tmdb.org/t/p/w1280${pelicula.backdrop_path}`"
                  class="d-block w-100"
                  alt="Imagen de la película"
                >

                <div class="overlay">
                  <div class="banner-titulo">
                    <p class="fw-bold">{{ pelicula.original_title }}</p>
                    <p class="fs-6">{{ pelicula.overview }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- <button
              class="carousel-control-prev"
              type="button"
              data-bs-target="#carouselExampleSlidesOnly"
              data-bs-slide="prev"
            >
              <span class="carousel-control-prev-icon"></span>
            </button>

            <button
              class="carousel-control-next"
              type="button"
              data-bs-target="#carouselExampleSlidesOnly"
              data-bs-slide="next"
            >
              <span class="carousel-control-next-icon"></span>
            </button> -->
          </div>
        </div>

        <div v-else class="banner">
          <div class="loading">
            <div class="spinner-border text-light" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Categorías -->
      <div class="categorias">

        <div class="categoria">
          <p class="h3">Cartelera</p>

          <div class="contenido-categoria" v-if="cine.length > 0">
            <div
              v-for="peliculaCine in cine"
              :key="peliculaCine.id"
              class="card"
              @click="showMediaDetails(peliculaCine)"
            >
              <img :src="`https://image.tmdb.org/t/p/w500${peliculaCine.poster_path}`" alt="Poster" class="card-img-top">
            </div>
          </div>
        </div>
      </div>
    </div>

    <FooterPag />

  </div>
</template>