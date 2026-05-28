<script setup>
import { ref, onMounted } from 'vue'
import verImg from '../assets/ver.png'
import { useRouter } from 'vue-router'

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

const tendencias = ref([])
const populares = ref([])
const peliculasGratis = ref([])
const series = ref([])

const logout = ref(false)
const estaLogeado = ref(false)

function goToHome() {
  window.location.href = '/'
}

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

async function obtenerTendencias() {
  const url = `https://api.themoviedb.org/3/trending/all/week?api_key=${apiKey}&language=es-ES&page=1`
  const response = await fetch(url)
  const data = await response.json()
  tendencias.value = data.results || []
}

async function obtenerPopulares() {
  const url = `https://api.themoviedb.org/3/movie/popular?api_key=${apiKey}&language=es-ES&page=1`
  const response = await fetch(url)
  const data = await response.json()
  populares.value = data.results || []
}

async function obtenerSeries() {
  const url = `https://api.themoviedb.org/3/tv/popular?api_key=${apiKey}&language=es-ES&page=1`
  const response = await fetch(url)
  const data = await response.json()
  series.value = data.results || []
}

async function obtenerPeliculasGratis() {
  const url = `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&language=es-ES&watch_region=US&with_watch_monetization_types=free`
  const response = await fetch(url)
  const data = await response.json()
  peliculasGratis.value = data.results || []
}

async function obtenerTopPeliculas() {
  const url = `https://api.themoviedb.org/3/movie/top_rated?api_key=${apiKey}&language=es-ES&page=1`
  const response = await fetch(url)
  const data = await response.json()

  if (data.results?.length > 0) {
    topPeliculas.value = data.results.slice(0, 3)

    backdrops.value = topPeliculas.value
      .filter(pelicula => pelicula.backdrop_path)
      .map(pelicula => `https://image.tmdb.org/t/p/w1280${pelicula.backdrop_path}`)
  }
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

onMounted(() => {
  const navbar = document.querySelector('.contenedor-navbar')

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scroll')
    } else {
      navbar.classList.remove('scroll')
    }
  })

  verificarSesion()
  obtenerTopPeliculas()
  obtenerTendencias()
  obtenerPerfilUsuario()
  obtenerPopulares()
  obtenerSeries()
  obtenerPeliculasGratis()
})
</script>

<template>
  <div>
    <div class="contenedor-principal">
      <!-- Navbar -->
      <div class="contenedor-navbar">
        <div class="contenedor-nombre-navbar">
          <p @click="goToHome" class="fw-bold">r i s k l e i s.</p>
        </div>

        <div class="opciones-navbar">
          <p @click="goToHome" class="fw-bold">Inicio</p>
          <p class="fs-6">Series</p>
          <p class="fs-6">Películas</p>
          <p class="fs-6">Novedades</p>
        </div>

        <div class="perfil-navbar">
          <img v-if="tieneImagen" :src="imgPATH" alt="img" class="foto-perfil">
          <div v-else class="contenedor-foto-perfil"></div>

          <img @click="mostrarBotonCerrar" :src="verImg" alt="ver" class="ver">

          <div v-if="logout">
            <button v-if="estaLogeado" @click="cerrarSession" class="btn btn-secondary">
              Cerrar sesión
            </button>

            <a v-else href="#" class="btn btn-secondary">
              Iniciar sesión
            </a>
          </div>
        </div>
      </div>

      <!-- Banner -->
      <div class="banner-cont">
        <div v-if="backdrops.length > 0" class="banner">
          <div id="carouselExampleSlidesOnly" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
              <div
                v-for="(backdrop, index) in backdrops"
                :key="index"
                class="carousel-item"
                :class="{ active: index === 0 }"
              >
                <img :src="backdrop" class="d-block w-100" alt="Imagen de la película">

                <div class="overlay" v-if="topPeliculas.length > index">
                  <div class="banner-titulo">
                    <p class="fw-bold">{{ topPeliculas[index].original_title }}</p>
                    <p class="fs-6">{{ topPeliculas[index].overview }}</p>
                  </div>
                </div>
              </div>
            </div>
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
          <p class="fw-medium">Tendencias</p>

          <div class="contenido-categoria" v-if="tendencias.length > 0">
            <div
              v-for="tendencia in tendencias"
              :key="tendencia.id"
              class="card"
              @click="showMediaDetails(tendencia)"
            >
              <img :src="`https://image.tmdb.org/t/p/w500${tendencia.poster_path}`" alt="Poster" class="card-img-top">
            </div>
          </div>
        </div>

        <div class="categoria">
          <p class="fw-medium">Lo más popular</p>

          <div class="contenido-categoria" v-if="populares.length > 0">
            <div
              v-for="popular in populares"
              :key="popular.id"
              class="card"
              @click="showMediaDetails(popular)"
            >
              <img :src="`https://image.tmdb.org/t/p/w500${popular.poster_path}`" alt="Poster" class="card-img-top">
            </div>
          </div>
        </div>

        <div class="categoria">
          <p class="fw-medium">Ver gratis</p>

          <div class="contenido-categoria" v-if="peliculasGratis.length > 0">
            <div
              v-for="peliculaGratis in peliculasGratis"
              :key="peliculaGratis.id"
              class="card"
              @click="showMediaDetails(peliculaGratis)"
            >
              <img :src="`https://image.tmdb.org/t/p/w500${peliculaGratis.poster_path}`" alt="Poster" class="card-img-top">
            </div>
          </div>
        </div>

        <div class="categoria">
          <p class="fw-medium">Series</p>

          <div class="contenido-categoria" v-if="series.length > 0">
            <div
              v-for="serie in series"
              :key="serie.id"
              class="card"
              @click="showMediaDetails(serie)"
            >
              <img :src="`https://image.tmdb.org/t/p/w500${serie.poster_path}`" alt="Poster" class="card-img-top">
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer id="pie">
      <div style="margin-top: 16px">
        <div class="contenidoUno">
          <p class="fs-3">r i s k l e i s</p>
          <p class="fs-6">Contáctanos</p>
          <p class="fs-6">Ayuda</p>
          <p class="fs-6">Redes</p>
        </div>
      </div>
    </footer>
  </div>
</template>