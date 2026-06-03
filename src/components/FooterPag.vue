<script setup>
import { ref, computed, onMounted } from 'vue'
const sessionId = localStorage.getItem('sessionId')

const imgPATH = ref('')
const tieneImagen = ref(false)

</script>

<template>
  <footer id="pie">
      <div style="margin-top: 16px">
        <div class="contenidoUno">
          <p class="fs-3">r i s k l e i s</p>
          <p class="fs-6">Contáctanos</p>
          <p class="fs-6">Ayuda</p>
          <p class="fs-6">Redes</p>
          <p class="fs-6">Hecho por Ivan Rios</p>
        </div>
      </div>
    </footer>
</template>