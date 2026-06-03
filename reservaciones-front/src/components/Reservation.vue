<script setup>
import { ref, computed, onMounted } from 'vue'

import Navbar from './Navar.vue'
import FooterPag from './FooterPag.vue'
import '../assets/reservacion.css'
import Seat from './Seat.vue'

</script>

<template>
    <div>
        <Navbar />
        <div class="contenedor-cine">
            <div class="pantalla-cine">
                 <!-- <p class="texto-pantalla">PANTALLA</p> -->
            </div>

            <div class="contenedor-seat ">
                <Seat v-for="number in 155" :key="number" :number="number" />
            </div>

        </div>
    </div>

    <FooterPag />
</template>