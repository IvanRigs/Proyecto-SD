import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './assets/home.css'
import './assets/detallePelicula.css'
import './assets/navbar.css'

createApp(App)
  .use(router)
  .mount('#app')