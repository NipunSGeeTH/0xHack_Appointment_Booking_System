import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles.css'  // your global styles

const app = createApp(App)

app.use(createPinia()) // for state management
app.use(router)        // for routing

app.mount('#app')
