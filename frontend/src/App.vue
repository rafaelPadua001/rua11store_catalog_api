<template>
  <v-app>
    <router-view />

    <div class="snackbar-container">
      <v-snackbar
        v-for="(notification, index) in notifications"
        :key="index"
        v-model="notification.show"
        timeout="5000"
        color="success"
        elevation="2"
        location="bottom right"
        @update:model-value="(val) => onSnackbarClose(index, val)"
      >
        {{ notification.message }}
        <template #actions>
          <v-icon color="white" text @click="notification.show = false">mdi-close</v-icon>
        </template>
      </v-snackbar>
    </div>
  </v-app>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { io, type Socket } from 'socket.io-client'

interface Notification {
  message: string
  show: boolean
}

const notifications = ref<Notification[]>([])


let socket: Socket

function onSnackbarClose(index: number, isVisible: boolean) {
  if (!isVisible) {
    notifications.value.splice(index, 1)
  }
}
const hasNewNotifications = ref(false)

provide('hasNewNotifications', hasNewNotifications)
provide('notifications', notifications) // ← aqui

onMounted(() => {
  socket = io('https://rua11store-catalog-api-lbp7.onrender.com', { transports: ['websocket', 'polling'] })

  socket.on('connect', () => {
 //   console.log('Socket conectado:', socket.id)
  })

  socket.on('notification', (data) => {
  //  console.log('Notificação recebida:', data)
    notifications.value.push({ message: data.message, show: true })
    hasNewNotifications.value = true
  })

  socket.on('disconnect', () => {
    //console.log('Socket desconectado')
  })
})
</script>

<style scoped>
.snackbar-container {
  position: fixed;
  bottom: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px; /* Espaço entre snackbars */
  z-index: 9999;
  width: 320px; /* Pode ajustar para o tamanho desejado */
}
</style>
