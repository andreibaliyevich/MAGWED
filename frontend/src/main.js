import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import i18n from './i18n'

import componentsUI from './components/UI'
import directives from './directives'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

componentsUI.forEach(component => {
  app.component(component.name, component)
})

directives.forEach(directive => {
  app.directive(directive.name, directive)
})

app.mount('#app')
