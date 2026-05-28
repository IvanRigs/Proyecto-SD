<script setup>
import { ref, computed, onMounted } from 'vue'
import verImg from '../assets/ver.png'
import likeImg from '../assets/como.png'

const apiKey = '0a5fdb3d67479033813279d6d5550f58'
const sessionId = localStorage.getItem('sessionId')

const imgPATH = ref('')
const tieneImagen = ref(false)

const movie = ref(JSON.parse(localStorage.getItem('obj')))
const generos = ref([])
const plataformas = ref([])
const reparto = ref([])
const genreData = ref([])
const puntuacionPromedio = ref(0)

const rate = ref(0)
const ratingsUsuario = ref([])
const accountId = ref(null)
const mostrarRange = ref(false)

const fecha = computed(() => {
  if (!movie.value) return ''

  return movie.value.release_date == null
    ? new Date(movie.value.first_air_date).getFullYear()
    : new Date(movie.value.release_date).getFullYear()
})

function goToHome() {
  window.location.href = '/'
}

function mediaType() {
  return movie.value?.name == null ? 'movie' : 'tv'
}

function showMediaDetails(obj) {
  localStorage.setItem('obj', JSON.stringify(obj))
  window.location.reload()
}

function ocultarImagen(event) {
  event.target.style.display = 'none'
}

function rateMenu() {
  mostrarRange.value = !mostrarRange.value
}

function goToActor(actorId) {
  localStorage.setItem('artistaId', actorId)
  console.log('Ir a actor:', actorId)
}

async function obtenerPlataformas() {
  if (!movie.value?.id) return

  const url = `https://api.themoviedb.org/3/${mediaType()}/${movie.value.id}/watch/providers?api_key=${apiKey}`

  const response = await fetch(url)
  const data = await response.json()

  const providers = data.results?.ES

  if (providers?.flatrate) plataformas.value = providers.flatrate
  else if (providers?.rent) plataformas.value = providers.rent
  else if (providers?.buy) plataformas.value = providers.buy
}

async function obtenerReparto() {
  const url = `https://api.themoviedb.org/3/${mediaType()}/${movie.value.id}/credits?api_key=${apiKey}&language=es-ES`

  const response = await fetch(url)
  const data = await response.json()

  reparto.value = data.cast || []
}

async function obtenerTrailer() {
  const url = `https://api.themoviedb.org/3/${mediaType()}/${movie.value.id}/videos?api_key=${apiKey}&language=es-ES`

  const response = await fetch(url)
  const data = await response.json()

  let trailers = data.results.filter(
    video => video.type === 'Trailer' && video.site === 'YouTube'
  )

  if (trailers.length === 0) {
    trailers = data.results.filter(
      video =>
        video.site === 'YouTube' &&
        ['Teaser', 'Clip', 'Featurette'].includes(video.type)
    )
  }

  if (trailers.length === 0) {
    alert('No se encontró ningún tráiler o video promocional.')
    return
  }

  window.open(`https://www.youtube.com/watch?v=${trailers[0].key}`, '_blank')
}

async function obtenerGenero() {
  const url = `https://api.themoviedb.org/3/genre/${mediaType()}/list?api_key=${apiKey}&language=es-ES`

  const response = await fetch(url)
  const data = await response.json()

  const genres = data.genres || []

  generos.value = movie.value.genre_ids
    .map(idGenero => genres.find(genre => genre.id === idGenero)?.name)
    .filter(Boolean)
}

async function obtenerPerfilUsuario() {
  if (!sessionId) return

  const url = `https://api.themoviedb.org/3/account?session_id=${sessionId}&api_key=${apiKey}`

  const response = await fetch(url)
  const data = await response.json()

  if (data?.avatar?.gravatar?.hash) {
    imgPATH.value = `https://secure.gravatar.com/avatar/${data.avatar.gravatar.hash}.jpg?s=64`
    tieneImagen.value = true
  }
}

async function obtenerPeliculasMismoGenero() {
  const primerGenero = movie.value.genre_ids?.[0]
  if (!primerGenero) return

  const url = `https://api.themoviedb.org/3/discover/${mediaType()}?api_key=${apiKey}&language=es-ES&with_genres=${primerGenero}&page=1`

  const response = await fetch(url)
  const data = await response.json()

  genreData.value = data.results || []
}

async function obtenerPuntuacionPromedio() {
  const url = `https://api.themoviedb.org/3/${mediaType()}/${movie.value.id}?api_key=${apiKey}&language=es-ES`

  const response = await fetch(url)
  const movieData = await response.json()

  puntuacionPromedio.value = parseInt(movieData.vote_average * 10)
}

async function addRate(rater) {
  rater = rater === '0' ? '0.5' : rater

  if (!sessionId) {
    alert('Debes iniciar sesión para calificar una película.')
    return
  }

  const url = `https://api.themoviedb.org/3/${mediaType()}/${movie.value.id}/rating?api_key=${apiKey}&session_id=${sessionId}`

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ value: Number(rater) })
  })

  if (!response.ok) {
    const errorData = await response.json()
    alert(errorData.status_message || 'Error al enviar la calificación.')
    return
  }

  rate.value = rater * 10
  mostrarRange.value = false
}

async function verificarSession() {
  if (!sessionId) return

  const url = `https://api.themoviedb.org/3/account?session_id=${sessionId}&api_key=${apiKey}`

  const response = await fetch(url)
  const data = await response.json()

  accountId.value = data.id
}

async function obtenerSeriesValoradasUsuario() {
  if (!sessionId || !accountId.value) return

  const tipoRated = mediaType() === 'movie' ? 'movies' : 'tv'
  const url = `https://api.themoviedb.org/3/account/${accountId.value}/rated/${tipoRated}?api_key=${apiKey}&session_id=${sessionId}`

  const response = await fetch(url)
  const data = await response.json()

  ratingsUsuario.value = data.results || []

  const encontrada = ratingsUsuario.value.find(item => item.id === movie.value.id)

  if (encontrada) {
    rate.value = encontrada.rating * 10
  }
}

onMounted(async () => {
  const navbar = document.querySelector('.contenedor-navbar')

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) navbar.classList.add('scroll')
    else navbar.classList.remove('scroll')
  })

  await obtenerPlataformas()
  await obtenerReparto()
  await obtenerGenero()
  await obtenerPerfilUsuario()
  await obtenerPeliculasMismoGenero()
  await obtenerPuntuacionPromedio()
  await verificarSession()
  await obtenerSeriesValoradasUsuario()
})
</script>

<template>
  <div>
    <div class="contenedor-principal">
      <div class="contenedor-navbar">
        <div class="contenedor-nombre-navbar">
          <p @click="goToHome" class="fw-bold">r i s k l e i s.</p>
        </div>

        <div class="opciones-navbar">
          <p @click="goToHome" class="fs-6" id="inicio">Inicio</p>
          <p class="fs-6">Series</p>
          <p class="fs-6">Películas</p>
          <p class="fs-6">Novedades</p>
        </div>

        <div class="perfil-navbar">
          <img v-if="tieneImagen" :src="imgPATH" alt="img" class="foto-perfil">
          <div v-else class="contenedor-foto-perfil"></div>
          <img :src="verImg" alt="ver" class="ver">
        </div>
      </div>

      <div class="banner-cont">
        <div class="banner">
          <img
            v-if="movie"
            :src="`https://image.tmdb.org/t/p/w1280${movie.backdrop_path}`"
            class="d-block w-100"
            alt="Imagen de la película"
          >

          <div class="overlay" v-if="movie">
            <div class="banner-titulo">
              <p class="fw-bold">{{ movie.original_title || movie.name }}</p>

              <div class="info-movie">
                <p class="fs-6">{{ fecha }}</p>
                <p class="fs-5">|</p>

                <p v-for="genero in generos" :key="genero" id="generos" class="fs-5">
                  {{ genero }}
                </p>

                <p class="fs-5">|</p>
                <p class="fs-5">{{ puntuacionPromedio }} %</p>
              </div>

              <div class="info-movie">
                <img class="like" :src="likeImg" alt="like">

                <button @click="rateMenu" class="btn btn-primary" id="promedio">
                  {{ rate }} %
                </button>

                <input
                  v-if="mostrarRange"
                  type="range"
                  class="form-range"
                  min="0"
                  max="10"
                  v-model="rate"
                  @change="addRate(rate / 10)"
                >
              </div>

              <p class="fs-6">{{ movie.overview }}</p>

              <div class="mb-3">
                <button @click="obtenerTrailer" class="btn btn-primary">
                  Ver trailer
                </button>
              </div>

              <div v-if="plataformas.length > 0" class="plataformas">
                <img
                  v-for="plataforma in plataformas"
                  :key="plataforma.provider_id"
                  class="img-plataforma"
                  :src="`https://image.tmdb.org/t/p/original/${plataforma.logo_path}`"
                  alt="plataforma"
                >
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
      </div>

      <div class="cont-segundo">
        <div class="categorias">
          <div class="categoria">
            <p class="fw-medium">Reparto</p>

            <div class="contenido-categoria" v-if="reparto.length > 0">
              <div
                v-for="actor in reparto"
                :key="actor.id"
                class="card"
                id="cartaReparto"
                @click="goToActor(actor.id)"
              >
                <img
                  v-if="actor.profile_path"
                  :src="`https://image.tmdb.org/t/p/w500/${actor.profile_path}`"
                  alt="Poster"
                  class="card-img-top"
                  @error="ocultarImagen"
                >

                <h5 class="card-title">{{ actor.name }}</h5>
              </div>
            </div>
          </div>

          <div class="categoria">
            <p class="fw-medium">Recomendaciones</p>

            <div class="contenido-categoria" v-if="genreData.length > 0">
              <div
                v-for="movieItem in genreData"
                :key="movieItem.id"
                class="card"
                @click="showMediaDetails(movieItem)"
              >
                <img
                  :src="`https://image.tmdb.org/t/p/w500/${movieItem.poster_path}`"
                  alt="Poster"
                  class="card-img-top"
                >
              </div>
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