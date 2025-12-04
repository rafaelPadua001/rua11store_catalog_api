<template>
  <div>
    <v-btn icon @click="toggleNotifications">
      <v-badge :content="unreadCount" color="red" v-if="unreadCount > 0">
        <v-icon>mdi-bell</v-icon>
      </v-badge>
      <v-icon v-else>mdi-bell-outline</v-icon>
    </v-btn>

    <v-snackbar v-model="show" :timeout="5000" color="info">
      {{ message }}
      <template #actions>
        <v-btn icon @click="show = false"><v-icon>mdi-close</v-icon></v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { io } from 'socket.io-client'

export default {
  data() {
    return {
      socket: null,
      show: false,
      message: '',
      userId: 1, // normalmente viria da autenticação
      unreadCount: 0
    }
  },
  methods: {
    async fetchUnread() {
      const res = await fetch(`https://rua11store-catalog-api-lbp7.onrender.com/notifications/${this.userId}`)
      const data = await res.json()
      this.unreadCount = data.length
    },
    toggleNotifications() {
      this.fetchUnread()
      // Aqui você poderia abrir uma modal com a lista de notificações
    }
  },
  mounted() {
    this.socket = io('https://rua11store-catalog-api-lbp7.onrender.com', {
      transports: ['polling'],
      query: {user_id: this.userId}
    });

    this.socket.on('connect', () => {
      console.log('Socket connected, id=', this.socket.id);
      // envie auth após conectar
     this.socket.emit("auth", { user_id: this.userId }); 
     this.socket.emit('notification', {user_id: this.userId});
      console.log("AUTH enviado:", this.userId);
    });


    this.socket.on(`notification`, (data) => {
      console.log('notification received', data);
      this.message = data.message;
      this.show = true;
      this.unreadCount++;
    });
    this.socket.on('connect_error', (err) => {
      console.error('connect_error', err);
    });
    this.socket.on('disconnect', (reason) => {
      console.log('socket disconnected', reason);
    });
    this.fetchUnread();
  }

}
</script>
