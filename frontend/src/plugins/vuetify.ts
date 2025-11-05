/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'
import { VMaskInput } from 'vuetify/labs/VMaskInput'

//Vpie
import { VPie } from 'vuetify/labs/VPie'

import { pt } from 'vuetify/locale';

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
  },
  components: {
    VMaskInput,
    VPie,
  },
  locale: {
    locale: 'pt',
    messages: { pt },
  },
})
