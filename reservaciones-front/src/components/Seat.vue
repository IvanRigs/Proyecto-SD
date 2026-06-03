<script setup>
import { ref, computed, onMounted } from 'vue'

import '../assets/seat.css'

var number = 0

console.log(number);

</script>

<template>

    <div class="seat">

        <div class="number-seat">{{number}}</div>

    </div>

</template>