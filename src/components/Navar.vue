<script setup>
import { ref, computed, onMounted } from 'vue'
import verImg from '../assets/ver.png'

const sessionId = localStorage.getItem('sessionId')

const imgPATH = ref('')
const tieneImagen = ref(false)

function goToHome() {
  window.location.href = '/'
}

</script>

<template>
  <div class="contenedor-navbar">
        <div class="contenedor-nombre-navbar">
          <p @click="goToHome" class="fw-bold">r i s k l e i s.</p>
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
</template>